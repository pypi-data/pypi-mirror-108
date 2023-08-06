import colored, os
def cls(): os.system('cls' if os.name=='nt' else 'clear') # Cross Platform Clearing
def newGrid(w:int, h:int, default:str="white"):
    usergrid = []
    for i in range(w):
        g = []
        for i in range(h):
            g.append(colored.bg(default)+"  ")
        usergrid.append(g)
    gridobj = Grid
    gridobj.default=default
    gridobj.grid=usergrid
    return gridobj()
class Grid:
    default = "white"
    grid = []
    def __init__(self):
        print("init ran")
    def plot(self, x:int, y:int, color:str="default"):
        self.grid[x][y]=colored.bg(self.default if color=='default' else color)+"  "
    def show(self, clear=True):
        for i in self.grid:
            floor = ""
            for i1 in i:
                floor += i1
            print(floor, end="\n")