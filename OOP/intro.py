# Object Oriented Programming in Python

# Create a class:

class Dog: # name the class, use upper case
    
    
    # init method will be called whenever we write a new Dog() instance,  
    # and pass any arguments we put in Dog(arg1, arg2) to the init method
    # dont need to explicitly call init method
    def __init__(self, name, age): # instantiates the object right when it is created
        
        
        # name is a parameter in init method --> when ex Dog("Tim") is called, the name needs to be stored in the Dog object
        # stored permanently for each spesific object
        self.name = name # define an attribute of the class Dog called name, which is equal to the name passed in
        self.age = age

    # define methods and operations that can be performed by the object
    def bark(self): # method
        print("bark")
    
    def add_one(self, x): # method can contain several arguments
        return x + 1
    
    def get_name(self):
        return self.name
    
    def get_age(self):
        return self.age
    
    def set_age(self, age):
        self.age = age

d = Dog("Tim", 34) # creates a new instance of the class Dog which passes in the name Tim and age 34

d.bark() # call method bark() on the Dog object d

#print(d.get_name())

d.set_age(23) # changes age to 24
print(d.get_age())



