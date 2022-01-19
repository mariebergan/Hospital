# Class attributes are attributes that are specific to the class, not to an instance or an object of that class
# Class attributes are different from regular attributes. 
# Because they do not use self and are not defined insisde any method and do not have access to an instance of the class,
# it is defined for the entire class.  

class Person:
    number_of_people = 0 # class attribute - is the same for each instance (p1, p2 etc.) of the Person class
    
    def __init__(self, name):
        self.name = name # regular attribute - is different for each instance (p1, p2 etc.) of the Person class
        Person.number_of_people += 1 # keeps track of the number of people created

p1 = Person("Tim")
p2 = Person("Jill")
print(Person.number_of_people) # prints number of people created

print(p1.number_of_people) # the same as using Person.number_of_people as it is not specifict for p1
print(Person.number_of_people) # can therefore access with Person as it is a class attribute
Person.number_of_people = 8 # can change the attribute using the class as well
print(p2.number_of_people) # changes the attribute for p2 as well as it is an instance of Person
