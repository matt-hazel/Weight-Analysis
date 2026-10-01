# This file will take the inputs for the weight csv.

# Imports
from Functions.classes import Measures
import time

def collect():
    print("\nBelow, you will input your information.\n")
    w = float(input("In pounds (lbs), please input today's weight: "))
    m = input("\nSeparated like (Mo/Day/Yr), please input today's date: ")
    cr = int(input("\nCarbohydrate count consumed: "))
    f = int(input("\nFat count consumed: "))
    p = int(input("\nProtein count consumed: "))
    ca = int(input("\nCalorie count consumed: "))
    s = int(input("\nSteps taken: "))
    a = int(input("\nCalories burned: "))
    
    counter = 0
    while counter != 3:
        print(".")
        time.sleep(1)
        counter += 1
    
    print(f"\nWeight: {w}\nDate: {m}\nCarbs: {cr}\nFats: {f}\nProtein: {p}\nTotal Calories: {ca}\nTotal Steps: {s}\nTotal Calories Burned: {a}")
    
    print("\nOne moment while your information is saved...")
    
    
    
    counter = 0
    while counter != 3:
        print(".")
        time.sleep(1)
        counter += 1
    
    x = Measures(w,m,cr,f,p,ca,s,a)
    
    x.record()