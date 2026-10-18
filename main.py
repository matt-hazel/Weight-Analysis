# The point of this program is to create something that can help assist my weight loss journey.
# It will hold onto data inputs in a CSV, which will also be used as a source to track trends via D.S.

"""from Functions.classes import Measures
from Functions.collection import collect
from Functions.interaction import menu"""
from Functions.packages import package_check

def main():
    print("lets see...")
    package_check()
    
    from Functions.classes import Measures
    from Functions.collection import collect
    from Functions.interaction import menu
    
    menu()
    


if __name__ == "__main__":
    main()