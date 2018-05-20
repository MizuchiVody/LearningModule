from tkinter import*
import numpy as np 
import sympy as sp

fields_1 = ('heading', 'ascent airspeed', 'ascent rate', 'engine failure time', 'decsent airspeed', 'decsent rate', 'wind','a','b','c')
fields_3 = ('number of turbines', 'water density', 'turbine radius', 'velocity in water', 'turbine efficiency')

#functions for mission 1

def AscentMovement (entries):
	h = float(entries['heading'].get())
	aas = float(entries['ascent airspeed'].get())
	t = float(entries['engine failure time'].get())
	global ycomp
	ycomp = aas * t * np.cos(np.deg2rad(h))	
	global xcomp 
	xcomp = aas * t * np.sin(np.deg2rad(h))
	print ("ascent movement: ")
	print (xcomp)
	print (ycomp)

def DescentMovement(entries):
	aar = float(entries['ascent rate'].get()) 
	h = float(entries['heading'].get())
	das = float(entries['decsent airspeed'].get())
	t = float(entries['engine failure time'].get())
	t2 = (t * aar) / 6
	adr = float(entries['decsent rate'].get())
	global Ycomp 
	Ycomp = das * t2 * np.cos(np.deg2rad(h))
	global Xcomp
	Xcomp = das * t2 * np.sin(np.deg2rad(h))				
	print ("descent movement: ")
	print (Xcomp)
	print (Ycomp)

def WindMovement(entries):
	aar = float(entries['ascent rate'].get()) 
	global h
	h = float(entries['heading'].get())
	das = float(entries['decsent airspeed'].get())
	t = float(entries['engine failure time'].get())
	t2 = (t * aar) / 6
	adr = float(entries['decsent rate'].get())
	A = float(entries['a'].get())
	B = float(entries['b'].get())
	C = float(entries['c'].get())
	w = float(entries['wind'].get())
	global ypos
	ypos = (1/3 * A * t2**3 + 1/2 * B * t2**2 + C * t2) * (np.cos(np.deg2rad(w - 180)))
	global xpos
	xpos = (1/3 * A * t2**3 + 1/2 * B * t2**2 + C * t2) * np.sin(np.deg2rad(w - 180))
	print ("wind movement: ")
	print (xpos)
	print (ypos)

def totMovement(entries):

	global xtot
	xtot = xcomp + Xcomp + xpos
	global ytot
	ytot = ycomp + Ycomp + ypos
	print ("total movement:") 
	print (xtot) 
	print (ytot)

#def degree (entries):							arctan (sum (sines) / sum (cosines))
def result(entries):
	dist = np.sqrt(xtot**2 + ytot**2)
	kaka = xtot / ytot
	direction = np.rad2deg(np.arctan(np.abs(kaka)))
	print ('reported search zone :')
	print (dist)
	#print (direction)
	if (xtot > 0 and ytot < 0):
		#direction+=180
		direction = 180 - direction 

	elif (xtot > 0 and ytot > 0):
		#direction+=90
		direction = 90 - direction

	elif (xtot < 0 and ytot > 0):
		#direction-=360
		direction = 360 - direction

	elif (xtot < 0 and ytot < 0):
		#direction-=270
		direction = 270 - direction

	print (direction)

#functions for mission 3

def doval(entries):
   N = float(entries['number of turbines'].get())
   d = float(entries['water density'].get())
   r = float(entries['turbine radius'].get())
   v = float(entries['velocity in water'].get())
   e = float(entries['turbine efficiency'].get())
   global P
   P = 0.5*(N*d*np.pi*(r**2)*(v**3))
   rt1 = Tk()
   Label(rt1, text = 'Maximum power that could be generated is:')
   rt1.mainloop
   #print("Maximum Power: %f" % float(P))

def makeform_for_1(root, fields):
	entries = {}
	for field in fields_1:
		row = Frame(root)
		lab = Label(row, width=22, text=field+": ", anchor='w')
		ent = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT, expand=YES, fill=X)
		entries[field] = ent
	return entries

def makeform_for_3(root, fields):
	entries = {}
	for field in fields_3:
		row = Frame(root)
		lab = Label(row, width=22, text=field+": ", anchor='w')
		ent = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT, expand=YES, fill=X)
		entries[field] = ent
	return entries


def prompt1 ():
	ents = makeform_for_1(root, fields_1)
	b1 = Button(root, text = 'validate', command = lambda: [AscentMovement(ents), DescentMovement(ents), WindMovement(ents), 
		totMovement(ents), result(ents)]).pack(side=LEFT, padx=5, pady=5)
	b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=5, pady=5)
	root.mainloop()
def prompt3 ():
	ents = makeform_for_3(root, fields_3)
	b1 = Button(root, text = 'validate', command = lambda: [doval(ents)]).pack(side=LEFT, padx=3, pady=3)
	b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=3, pady=3)
	root.mainloop()


root = Tk()
zebi = Label(root, text = "which mission do you wish to complete?", padx = 2, pady = 2, anchor = 'n', height = 3, width = 70)
zebi.pack()
btn1 = Button(root, text = "Mission 1", command = prompt1)
btn1.config(height = 3, width = 20)
btn1.pack()
btn3 = Button(root, text = "Mission 3", command = prompt3)
btn3.config(height = 3, width = 20)
btn3.pack()
root.mainloop()
