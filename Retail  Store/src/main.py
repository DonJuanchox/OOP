# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:02:10 2024

@author: juann
"""
from item import Item
from phone import Phone

Item.instantiate_from_csv()

print(Item.all)
print(Phone.all) # still receives object and append # --repeat and understand

item1 = Item('MyItem', 750)
print(item1.name)

item1.name = 'Juanih'
print(item1.name)