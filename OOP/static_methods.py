# Classes that organize functions together
# Static method: want to use methods without making an instance - be able to call them at any point
# Static methods do something but do not change anything as they do not have access to instances
# Acts as a functions to do something inside the class

class Math:
  
  @staticmethod
  def add5(x): # does not contain cls because the method is not accessing anything, 
      return x + 5 

print(Math.add5(5))