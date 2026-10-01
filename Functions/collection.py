# This file will take the inputs for the weight csv.

# Imports
from Functions.classes import Measures
import time

def collect():
    print("Hello! Welcome to your weigh-in application!")
    print("Below, you will input your information.")
    w = float(input("In pounds (lbs), please input today's weight: "))
    m = input("Separated like (Mo/Day/Yr), please input today's date: ")
    cr = int(input("Carbohydrate count consumed: "))
    f = int(input("Fat count consumed: "))
    p = int(input("Protein count consumed: "))
    ca = int(input("Calorie count consumed: "))
    s = int(input("Steps taken: "))
    a = int(input("Calories burned: "))
    print("\n")
    
    counter = 0
    while counter != 3:
        print(".")
        time.sleep(1)
        counter += 1
    
    print(f"Weight: {w}\nDate: {m}\nCarbs: {cr}\nFats: {f}\nProtein: {p}\nTotal Calories: {ca}\nTotal Steps: {s}\nTotal Calories Burned: {a}")
    
    print("\nOne moment while your information is saved...")
    
    
    
    counter = 0
    while counter != 3:
        print(".")
        time.sleep(1)
        counter += 1
    
    x = Measures(w,m,cr,f,p,ca,s,a)
    
    x.record()