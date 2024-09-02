cityColor = (0,128,255)
ruinsColor = (63, 63, 65)

#Class for city storage:
## self.index         Index for the current city
## self.x and self.y  Coordinates for the city
## self.status        Status (alive or dead) of the city
class City:
    def __init__(self, index, x):
        self.index = index
        self.x = x
        self.y = 545
        self.status = "alive"

#Creating all of the cities objects
city1 = City(0, 50)
city2 = City(1, 150)
#Add every city in the list
cities = [city1, city2]

#Variable for city status verification
isAlive = [True, True, True, True, True, True]

##Function return boolean if every single city isn't alive
def allDead():
    for cityStatus in isAlive:
        if cityStatus is True:
            return False
    return True
