# This is where the classes will be held.

#Imports
import csv


class Measures:
    def __init__(self,weight,modayr,carb,fat,prot,cal,steps,activ):
        self.weight = weight
        self.modayr = modayr
        self.carb = carb
        self.fat = fat
        self.prot = prot
        self.cal = cal
        self.steps = steps
        self.activ = activ
        
        
        if not weight:
            raise ValueError("Not Valid weight count")
        if not modayr:
            raise ValueError("Not a valid Mo/Da/Yr format")
        if not carb:
            raise ValueError("Not a Valid carb count")
        if not fat:
            raise ValueError("Not a Valid fat count")
        if not prot:
            raise ValueError("Not a Valid protein count")
        if not cal:
            raise ValueError("Not a Valid calorie count")
        if not steps:
            raise ValueError("Not a Valid step count")
        if not activ:
            raise ValueError("Not a valid acitivity count")
        
    #Getter for weight
    @property
    def weight(self):
        return self._weight
    
    @weight.setter
    def weight(self, weight):
        if not isinstance(weight, float):
            raise ValueError("This is not an float value.")
        self._weight = weight
        
    #Getter and Setter for Month Day Year
    @property
    def modayr(self):
        return self._modayr
    
    @modayr.setter
    def modayr(self, modayr):
        if not modayr:
            raise ValueError("Not a valid Mo/Da/Yr format")
        self._modayr = modayr
        
    #Getter and Setter for carb
    @property
    def carb(self):
        return self._carb
    
    @carb.setter
    def carb(self, carb):
        if not isinstance(carb, int):
            raise ValueError("This is not an int value.")
        self._carb = carb
    
    #Getter and Setter for fat
    @property
    def fat(self):
        return self._fat
    
    @fat.setter
    def fat(self, fat):
        if not isinstance(fat, int):
            raise ValueError("This is not an int value.")
        self._fat = fat
        
    #Getter and Setter for protein
    @property
    def prot(self):
        return self._prot
    
    @prot.setter
    def prot(self, prot):
        if not isinstance(prot, int):
            raise ValueError("This is not an int value.")
        self._prot = prot
    
    #Getter and Setter for calories
    @property
    def cal(self):
        return self._cal
    
    @cal.setter
    def cal(self, cal):
        if not isinstance(cal, int):
            raise ValueError("This is not an int value.")
        self._cal = cal
        
    #Getter and Setter for steps
    @property
    def steps(self):
        return self._steps
    
    @steps.setter
    def steps(self, steps):
        if not isinstance(steps, int):
            raise ValueError("This is not an int value.")
        self._steps = steps
    
    #Getter and Setter for activity
    @property
    def activ(self):
        return self._activ
    
    @activ.setter
    def activ(self, activ):
        if not isinstance(activ, int):
            raise ValueError("This is not an int value.")
        self._activ = activ    
        
    def record(self):
        with open("weight.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["weight","modayr","carb","fat","prot","cal","steps","activ"])
            writer.writerow({"weight":self.weight,"modayr":self.modayr,"carb":self.carb,"fat":self.fat,"prot":self.prot,"cal":self.cal,"steps":self.steps,"activ":self.activ})
        print(f"Weigh in recorded. {self.weight}lbs on {self.modayr}, on which {self.carb}, {self.fat}, {self.prot}, {self.cal} were consumed, had {self.steps} steps, and burned {self.activ} calories.")
        
