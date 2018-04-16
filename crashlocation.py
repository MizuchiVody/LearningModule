from tkinter import*
import numpy as np 

fields = ('heading', 'ascent airspeed', 'ascent rate', 'engine failure time', 'decsent airspeed', 'decsent rate', 'wind','a', 'b', 'c')


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
								#arctan (sum (sines) / sum (cosines))
def result(entries):
	dist = np.sqrt(xtot**2 + ytot**2)
	kaka = xtot / ytot
	direction = np.rad2deg(np.arctan(kaka))
	print ('reported search zone :')
	print (dist)
	print (direction)
	if (xtot > 0 and ytot < 0):
		direction+=180

	elif (xtot > 0 and ytot > 0):
		direction+=90

	elif (xtot < 0 and ytot > 0):
		direction-=360

	elif (xtot < 0 and ytot < 0):
		direction-=270

	print (direction)

def makeform(root, fields):
	entries = {}
	for field in fields:
		row = Frame(root)
		lab = Label(row, width=22, text=field+": ", anchor='w')
		ent = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		lab.pack(side=LEFT)
		ent.pack(side=RIGHT, expand=YES, fill=X)
		entries[field] = ent
	return entries

if __name__ == '__main__':
	root = Tk()
	ents = makeform(root, fields)
	#root.bind('<Return>', (lambda event, e=ents: daval(e)))   
	b1 = Button(root, text = 'validate', command = lambda: [AscentMovement(ents), DescentMovement(ents), WindMovement(ents), totMovement(ents), result(ents)])			
	#command=(lambda e=ents: g4(e))
	b1.pack(side=LEFT, padx=5, pady=5)
	b3 = Button(root, text='Quit', command=root.quit)
	b3.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()
