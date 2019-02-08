# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

annual_salary = float(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))

portion_down_payment = 0.25
current_savings = 0
r = 0.04

down_payment = total_cost * portion_down_payment
num_month = 0

while current_savings < down_payment:
    current_savings += current_savings * r / 12 + annual_salary * portion_saved /12
    num_month += 1
print('Number of months:​', num_month)