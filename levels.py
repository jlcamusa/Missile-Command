#Levels


#Class for level storage:
## self.lvl    Que nivel es
## self.time   Tiempo de juego
## self.qnt    Cantidad de misiles
class Level:
    def __init__(self, lvl, time, qnt):
        self.lvl = lvl
        self.time = time
        self.qnt = qnt

lvl1 = Level(1, 60000, 12)
lvl2 = Level(2, 60000, 18)
lvl3 = Level(3, 60000, 24)
lvl4 = Level(4, 60000, 30)
lvl5 = Level(5, 60000, 36)
lvl6 = Level(6, 60000, 42)
lvl7 = Level(7, 60000, 48)
lvl8 = Level(8, 60000, 54)
lvl9 = Level(9, 60000, 60)
lvl10 = Level(10, 60000, 66)
lvl11 = Level(11, 60000, 72)
lvl12 = Level(12, 60000, 78)
lvl13 = Level(13, 60000, 84)
lvl14 = Level(14, 60000, 90)
lvl15 = Level(15, 60000, 96)
lvl16 = Level(16, 60000, 102)
lvl17 = Level(17, 60000, 108)
lvl18 = Level(18, 60000, 114)
lvl19 = Level(19, 60000, 120)
lvl20= Level(20, 60000, 126)

#Add every level to the levels list
levels = [lvl1, lvl2, lvl3, lvl4, lvl5, lvl6, lvl7, lvl8, lvl9, lvl10, lvl11, lvl12, lvl13, lvl14, lvl15, lvl16, lvl17, lvl18, lvl19, lvl20]