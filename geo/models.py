import sys

import requests
from django.conf import settings
from django.db import models
from geopy.distance import distance


class Location(models.Model):
    address = models.CharField(
        verbose_name='адрес',
        max_length=150,
        unique=True,
    )

    latitude = models.FloatField(verbose_name='широта',)
    longitude = models.FloatField(verbose_name='долгота',)
    changed_at = models.DateTimeField(
        verbose_name='изменена в',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'локация'
        verbose_name_plural = 'локации'

    def __str__(self):
        return f'Локация № {self.id} {self.address}'

    @classmethod
    def save_location(cls, address):
        coordinates = cls.fetch_coordinates(
            settings.YA_API_KEY,
            address
        )
        if coordinates:
            latitude, longitude = coordinates
            cls.objects.update_or_create(
                address=address,
                defaults={'latitude': latitude, 'longitude': longitude}
            )

    @classmethod
    def get_locations(cls, addresses):
        locations = cls.objects.filter(address__in=addresses).values(
            'address',
            'latitude',
            'longitude',
        )
        locations_catalog = {}
        for location in locations:
            locations_catalog[location['address']] = {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
            }

        return locations_catalog

    @staticmethod
    def fetch_coordinates(apikey, address):
        base_url = "https://geocode-maps.yandex.ru/1.x"
        response = requests.get(base_url,
                                params={
                                    "geocode": address,
                                    "apikey": apikey,
                                    "format": "json",
                                })
        response.raise_for_status()
        found_response = response.json()['response']
        found_places = found_response['GeoObjectCollection']['featureMember']

        if not found_places:
            return None

        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lat, lon

    @staticmethod
    def get_distance(order_location, restaurant_address, locations):
        if not order_location:
            return True, sys.maxsize

        restaurant_location = locations.get(restaurant_address, None)
        if not restaurant_location:
            return True, sys.maxsize

        distance_km = distance(
            (order_location['latitude'], order_location['longitude']),
            (restaurant_location['latitude'], restaurant_location['longitude'])
        ).km
        return False, distance_km

    @staticmethod
    def get_distance_from_restaurant(restaurant):
        return restaurant['distance']

    @staticmethod
    def get_addresses(order_cards):
        addresses = set()
        for order_card in order_cards:
            if order_card['order'].cooking_restaurant:
                continue
            if not order_card['possible_restaurants']:
                continue

            addresses.add(order_card['order'].address)

            for restaurant in order_card['possible_restaurants']:
                addresses.add(restaurant['address'])

        return addresses
