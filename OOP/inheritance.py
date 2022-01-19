# In stead of writing 2 classes that are very similar, 
# they can inherit functionality from each other and only define their differences

### only diff between Cat and Dog object is what the speak method prints
# class Cat:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
    
#     def speak(self):
#         print("Meow")

# class Dog:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def speak(self):
#         print("Bark")


# rather create an upper-level (parent) class with the functionality I want the Cat and Dog class both to have
class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
 
    def show(self):
        print(f"I am {self.name} and I am {self.age} years old")
    
    def speak(self):
        print("I don't know what to say")

# inside the Cat/Dog class I define the methods and/or attributes that is diff for this specific class
class Cat(Pet): # inheriting the upper-level class Pet
    
    # add an attribute specific to Cat - change init method
    def __init__(self, name, age, color): # define arguments from upper-level class init method and new argument color
        super().__init__(name, age) # super() references upper-level class to get the attributes from Pet -->
        self.color = color          # sets up name and age from the init method in Pet
      
    def speak(self):
        print("Meow")

class Dog(Pet): # inheriting the upper-level class Pet
    def speak(self):
        print("Bark")

class Fish(Pet):
    pass

p = Pet("Tim", 19)
p.show()
c = Cat("Bill", 34, "Brown") # argument brown as color was added to Cat
c.show() # works even though there is no show method inside Cat object because of inheritance
d = Dog("Jill", 25)
d.show()
c.speak() # diff from d.speak as they are defined in the specific classes, not the general Pet class
d.speak() # they also override the speak method in the upper-level class if they have the same method
f = Fish("Bubbles", 10)
f.speak() # prints speak method from Pet as the Fish has no speak method defined
 