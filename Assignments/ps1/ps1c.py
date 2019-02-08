#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 19:37:08 2018

@author: royckchan
"""

annual_salary = float(input('Enter the starting salary: '))
semi_annual_raise = 0.07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000

down_payment = total_cost * portion_down_payment

max_savings = 0
annual_salary_max = annual_salary
for i in range(36):
    max_savings += max_savings * r / 12 + annual_salary_max / 12
    if (i+1) % 6 == 0:
        annual_salary_max *= 1 + semi_annual_raise
        
if max_savings < down_payment:
    print('It is not possible to pay the down payment in three years.')
else:
    current_savings = 0
    lb = 0
    ub = 10000
    num_step = 0
    while abs(current_savings - down_payment) > 100:
        best_saving_rate = int((lb+ub)/2)
        temp1 = 0
        temp2 = annual_salary
        for i in range(36):
            temp1 += temp1 * r / 12 + temp2 / 12 * best_saving_rate / 10000
            if (i+1) % 6 == 0:
                temp2 *= 1 + semi_annual_raise
        current_savings = temp1
        num_step += 1
        if current_savings < down_payment:
            lb = best_saving_rate
        else:
            ub = best_saving_rate
    print('Best savings rate:', best_saving_rate / 10000)
    print('Steps in bisection search:', num_step)
        
