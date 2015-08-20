from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter as tk
import im2glib as im2g
import turtle

FONT = "Trebuchet"

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(row = 0, column = 0)
        self.createWidgets()
        
        self.paths = []
        self.filename = ""

    def createWidgets(self):
        self.imInput = Entry(self, width = 54, font = (FONT, 12))
        self.imInput.delete(0, END)
        self.imInput.insert(0, "Enter the name of your image file")
        self.imInput.grid(row = 0, column = 0, padx = 0, pady = 10,\
                          columnspan = 2)

        self.browseButton = tk.Button(self, width = 20, font = (FONT, 12))
        self.browseButton["text"] = "Browse"
        self.browseButton["command"] = self.browse
        self.browseButton.grid(row = 1, column = 0)
        
        self.plotButton = tk.Button(self, width = 20, font = (FONT, 12))
        self.plotButton["text"] = "Show Path"
        self.plotButton["command"] = self.plot
        self.plotButton.grid(row = 1, column = 1)
        
        self.turtlePlot = tk.Canvas(self, width = 480, height = 480)
        self.turtlePlot.grid(row = 2, column = 0, columnspan = 2, padx = 5,\
                             pady = 10)
        
        self.turtleSheet = turtle.TurtleScreen(self.turtlePlot)
        self.turtleSheet.setworldcoordinates(0, 0, im2g.IMDIM, im2g.IMDIM)
        
        self.router = turtle.RawTurtle(self.turtleSheet)
        self.router.shape("circle")
        self.router.setx(0)
        self.router.sety(0)

        self.fileButton = tk.Button(self, width = 20, font = (FONT, 12))
        self.fileButton["text"] = "Send to Text File"
        self.fileButton["command"] = self.toText
        self.fileButton.grid(row = 3, column = 0, pady = 10)

        self.serialButton = tk.Button(self, width = 20, font = (FONT, 12))
        self.serialButton["text"] = "Send to Serial Port"
        self.serialButton["command"] = self.toSerial
        self.serialButton.grid(row = 3, column = 1, pady = 10)        

    def browse(self):
        self.imInput.delete(0, END)
        self.imInput.insert(0, askopenfilename())
        self.paths = []
    
    def turtleDraw(self):
        self.router.speed(1)
        self.router.clear()
        
        for path in self.paths:
            firstCoord = True

            for coord in path:
                if firstCoord:
                    self.router.penup()
                    firstCoord = False
                else: self.router.pendown()

                self.router.goto(coord)
        
        self.router.penup()
        self.router.goto((0, 0))
    
    def plot(self):
        self.filename = self.imInput.get()
        if self.paths == []: self.paths = im2g.imToPaths(self.filename)
        
        self.turtleDraw()

    def toText(self):
        self.filename = self.imInput.get()
        if self.paths == []: self.paths = im2g.imToPaths(self.filename)
        
        outfile = self.filename.rsplit(".", 1)[0] + ".gcode"
        im2g.toTextFile(outfile, self.paths)
    
    def toSerial(self):
        self.filename = self.imInput.get()
        if self.paths == []: self.paths = im2g.imToPaths(self.filename)
        
        im2g.toSerial(self.paths)

root = tk.Tk()
root.wm_title("Image to G Code")
app = Application(master=root)
app.mainloop()
