# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 22:32:30 2021

@author: Pc4y
"""

import requests

url = 'https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=&brand2=&price_from=&price_to=&year_from=2000&year_to=2020&flywheel=&atest=&door_num=&submit_1=&without_price=1&date_limit=&showOldNew=all&modeltxt=&engine_volume_from=&engine_volume_to=&power_from=&power_to=&mileage_from=&mileage_to=&emission_class=&seat_num=&wheel_side=&registration=&country=&country_origin=&city=&registration_price=&page=&sort='

response = requests.get(url)


from bs4 import BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)