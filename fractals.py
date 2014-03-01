usage="""
general
========
creates fractal gifs using the L system

what you need
=============
- linux operating system ( I'm using Lubuntu)
- python3
- matplotlib installed

currently supported fractals:
============================
- dragon curve
- sierpinski triangle
- c curve

usage
=====
$ python3 fractals.py <name>
<name> is either dragon_curve or sierpinski or ccurve

this command will create a few temporary png images in your current directory
and then create a gif from them

example
=======
$ python3 fractals.py dragon_curve

"""

import matplotlib.pyplot as plt
import math
import os
import sys

class Drawer:
    """Implements turtle graphics"""
    def __init__(self):
        """(Drawer, float, float) -> None
        creates a drawer object"""
        self.reset()
    def reset(self):
        """(Drawer) -> None
        resets all attributes"""
        self.x=0
        self.y=0
        self.allx=[self.x]
        self.ally=[self.y]
        self.dir=[-1,0]
        self.clear()
    def draw(self,steps):
        """(Drawer, int) -> None
        draws a line from current position
        to new position determined by direction and number of steps"""
        newx=self.x+steps*self.dir[0]
        newy=self.y+steps*self.dir[1]
        self.x=newx
        self.y=newy
        self.allx.append(self.x)
        self.ally.append(self.y)
    def turn(self,degrees):
        """(Drawer, float) -> None
        rotates the drawer object clockwise a given number of degrees"""
        rad=degrees/180*math.pi
        #rotation tranformation
        self.dir=[self.dir[0]*math.cos(rad)-self.dir[1]*math.sin(rad),
                  self.dir[0]*math.sin(rad)+self.dir[1]*math.cos(rad)]
    def adjust_limits(self):
        """(Drawer) -> None
        adjusts the limits of the drawing"""
        rangex=[min(self.allx),max(self.allx)]
        rangey=[min(self.ally),max(self.ally)]
        distx=(abs(rangex[1]-rangex[0]))**0.5
        disty=(abs(rangey[1]-rangey[0]))**0.5
        plt.xlim([rangex[0]-distx, rangex[1]+distx])
        plt.ylim([rangey[0]-disty, rangey[1]+disty])
    def setup_drawing(self):
        self.adjust_limits()
        plt.axis('off')
        plt.plot(self.allx,self.ally)
    def display(self):
        """(Drawer) -> None
        displays the drawing"""
        self.setup_drawing()
        plt.show()
    def clear(self):
        """(Drawer) -> None
        clears the entire drawing"""
        plt.clf()
    def save(self,file_name):
        """(Drawer, string) -> None
        saves the current figure to a file"""
        self.setup_drawing()
        plt.savefig(file_name)

class Generator:
    """class for generating L system style fractals"""
    def __init__(self,start,rules):
        """(Generator, list of strings, string, dictionary) -> None
        initializes a generator object
        start- the first string
        rules- update rules. a dictinary mapping variables to their update"""
        self.rules=rules
        self.total=start
    def update(self):
        """(Generator) -> None
        updates the string once
        
        >>> g=Generator("F",{"F": "+F−−F+"})
        >>> g.update()
        >>> g.get_final()
        '+F−−F+'
        """
        self.total="".join([self.rules[c] if c in self.rules else c for c in self.total])
        
    def run(self,n):
        """(Generator, int) -> None
        runs update n times
        >>> g=Generator("F",{"F": "+F−−F+"})
        >>> g.run(2)
        >>> g.get_final()
        '++F−−F+−−+F−−F++'
        """
        for i in range(n):
            self.update()
    def get_final(self):
        """(Generator) -> string
        returns the final string"""
        return self.total

def parse(string,methods):
    """(string, dictionary) -> None
    Parses a L system string
    string- the string to parse
    methods- a dictionary mapping each character in 
    string to a function"""
    for c in string:
        methods[c]()

def fractal(start,rules,methods,n):
    """(string, dictionary, dictionary, int) -> None
    creates a fractal"""
    g=Generator(start,rules)
    g.run(n)
    s=g.get_final()
    parse(s, methods)

def fractal_gif(start,rules,methods,n,d,name):
    """(string, dictionary, dictionary, int, Drawer, string) -> None
    creates a fractal picture for every stage"""
    g=Generator(start,rules)
    all_files=''
    for i in range(n):
        g.run(1)
        s=g.get_final()
        parse(s, methods)
        file_name=name+str(i)+".png"
        all_files+=" "+file_name
        d.save(file_name)
        d.reset()
    os.system('convert -delay 100 -loop 0 '+all_files+' '+ name+'.gif')
    os.system('rm '+all_files)

def ccurve():
    start="F"
    rules={"F": "+F--F+"}
    n=12
    d=Drawer()
    methods={"F": lambda : d.draw(1), 
              "+": lambda : d.turn(45),
              "-": lambda : d.turn(315)}
    fractal_gif(start,rules,methods,n,d,"ccurve")

def sierpinski():
    start="A"
    rules={"A": "B-A-B", "B": "A+B+A"}
    n=9
    d=Drawer()
    methods={ "A": lambda : d.draw(1), 
              "B": lambda : d.draw(1), 
              "+": lambda : d.turn(60),
              "-": lambda : d.turn(300)}
    fractal_gif(start,rules,methods,n,d,"sierpinski")

def dragon_curve():
    start="FX"
    rules={"X": "X+YF+", "Y": "-FX-Y"}
    n=15
    d=Drawer()
    methods={ "F": lambda : d.draw(1), 
              "-": lambda : d.turn(360-90), 
              "+": lambda : d.turn(90),
              "X": lambda : None,
              "Y": lambda : None}
    fractal_gif(start,rules,methods,n,d,"dragon_curve")

if __name__=="__main__":
    if len(sys.argv)!=2:
        print(usage)
    elif sys.argv[1]=="test":
        import doctest
        doctest.testmod()
    elif sys.argv[1] == 'dragon_curve':
        dragon_curve()
    elif sys.argv[1] == 'sierpinski':
        sierpinski()
    elif sys.argv[1] == 'ccurve':
        ccurve()
    else:
        print(usage)
        
    

