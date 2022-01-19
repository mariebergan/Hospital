# Class methods are not specific to one instance, but acts on the class its self

class Person:
    number_of_people = 0 
    
    def __init__(self, name):
        self.name = name 
        Person.add_person()
    
    @classmethod # makes the method below a class method
    def number_of_people(cls): # cls instead of self because there is no object, but acting on the class
        return cls.number_of_people
    
    @classmethod
    def add_person(cls):
        cls.number_of_people += 1


p1 = Person("Tim")
p2 = Person("Jill")
print(Person.number_of_people())