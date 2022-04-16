from tkinter import *
class Window(Tk):
	def __init__(self, width, height, title="Window"):
		super().__init__()
		self.title(title)
		self.w = width
		self.h = height
		self.minsize(width=self.w, height=self.h)
		# get screen width and height
		self.ws = self.winfo_screenwidth() # width of the screen
		self.hs = self.winfo_screenheight() # height of the screen

		# calculate x and y coordinates for the Tk window
		self.x = (self.ws/2) - (self.w/2)
		self.y = (self.hs/2) - (self.h/2)

		# set the dimensions of the screen 
		# and where it is placedz
		self.geometry(f"+{int(self.x)}+{int(self.y-50)}")
