# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:02:10 2024

@author: juann
"""
class Item:
    
    # class attribute - accessible to all objects
    pay_rate = 0.8 # pay rate after 20% discount
    def __init__(self,
                 name: str,
                 price: float,
                 quantity: float=0):
        # Run argument validations
        assert price >= 0, f'Price {price} is not greater than zero'
        assert quantity >= 0, f'Quantity {quantity} is not greater than zero'
        
        # Assign to self object
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def calculate_total_price(self):
        return self.price * self.quantity
    
    def apply_discount(self):
        self.price *= self.pay_rate
    

item1 = Item('Phone', 100, 5)
# print(item1.calculate_total_price())

# print(Item.pay_rate)
# print(Item.__dict__) # All the attributes Class Level
# print(item1.__dict__) # All the attributes Instance Level

item1.apply_discount()
print(item1.price)

# Applying different discounts
item2 = Item('Laptop', 500, 3)
item2.pay_rate = 0.7

item2.apply_discount()
print(item2.price)