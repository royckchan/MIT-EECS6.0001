#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 19:10:32 2018

@author: royckchan
"""

annual_salary = float(input('Enter your starting annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = float(input('Enter the cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-­annual raise, as a decimal: '))

portion_down_payment = 0.25
current_savings = 0
r = 0.04

down_payment = total_cost * portion_down_payment

num_month = 0

while current_savings < down_payment:
    current_savings += current_savings * r / 12 + annual_salary * portion_saved / 12
    num_month += 1
    if num_month % 6 == 0:
        annual_salary *= 1 + semi_annual_raise
print('Number of months:​', num_month)