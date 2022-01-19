# Combinations of classes

class Student:
    def __init__(self, name, age, grade): 
        # define 3 attributes:
        self.name = name
        self.age = age
        self.grade = grade # 0 - 100

    def get_grade(self):
        return self.grade


class Course: # want to be able to add students to the course
    def __init__(self, name, max_students):
        self.name = name
        self.max_stundents = max_students
        
        # store students inside Course object:
        self.students = [] # fine to define attribute that is not a passed in argument 

    def add_student(self, student): # student is an instance of the Student object
        if len(self.students) < self.max_stundents:
            self.students.append(student)
            return True # True if student was added successfully
        return False # False was not added

    def get_average_grade(self):
        value = 0
        for student in self.students:
            value += student.get_grade() # adds the grades of all students 
        
        return value / len(self.students) # gets avarage grade

# create students with the defined arguments for the Student object
s1 = Student("Tim", 19, 95)
s2 = Student("Bill", 19 , 75)
s3 = Student("Gill", 19, 65)

# make course with the defined arguments for the Course object
course = Course("Science", 2)

# call add_students method to add students to course 
course.add_student(s1)
course.add_student(s2)
print(course.students[0].name) # prints the name of the student at index 0 in the course students list
print(course.add_student(s3)) # False due to max_students = 2
print(course.get_average_grade())
