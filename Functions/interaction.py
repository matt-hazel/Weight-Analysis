# This is temp functionality, as I wish to, for end of product, make a gui to go for this project.
# This is to create interactions within the terminal to interact with the program.
# I want this to be where I can interact with analysis (once completed), inputting info, and reading current information in the csv,

#Imports

from Functions.collection import collect
import time
import sys

def menu():
    print("------------------------------------------")
    print("  Hello! Welcome to the Weigh-In-Station!")
    
    while True:
        print("------------------------------------------")
        choice = int(input("\nWhat would you like to do?\n\t1. Weigh-in\n\t2. View recent Weigh-ins\n\t3. Scientific Analysis\n\t4. Exit Program\n\n(1, 2, 3, 4?) Choice: "))
        time.sleep(1)
        if choice == 1:
            print("------------------------------------------")
            collect()
        elif choice == 2:
            print("------------------------------------------")
            print("This option has not yet been added.")
        elif choice == 3:
            print("------------------------------------------")
            choice = input("Are you looking to view raw data, cleaned data, or a summary of the data? (raw/cleaned/summary) ")
            if choice.lower() == "raw":
                print("Viewing raw data...")
            elif choice.lower() == "cleaned":
                print("Viewing cleaned data...")
            elif choice.lower() == "summary":
                print("Viewing summary of data...")
            else:
                print("Invalid choice. Please try again.")
        elif choice == 4:
            print("------------------------------------------")
            print("Exiting program...")
            print("------------------------------------------")
            sys.exit()
        else:
            print("\nThis input was invalid. Please try again.")