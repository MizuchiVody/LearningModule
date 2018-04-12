from tkinter import*
import numpy as np 

fields = ('heading', 'ascent airspeed', 'ascent rate', 'Engine failure', 'decsent airspeed', 'decsent rate', 'wind','a', 'b', 'c')

def g1 (): 
	global AscentMovement
	def AscentMovement (entries):
		h = float(entries['heading'].get())
		aas = float(entries['ascent airspeed'].get())
		t = float(entries['engine failure'].get())
		ycomp = aas * t * np.cos(h)
		xcomp = aas * t * np.sin(h)
		print ("ascent movement: ")
		if (xcomp > 0):
			print (xcomp) 
			print ("(east)")
		elif (xcomp < 0):
			print (xcomp) 
			print ("(west)")
		else: print ("0")
		if (ycomp > 0):
			print (ycomp) 
			print ("(north)")
		elif (ycomp < 0):
			print (xcomp) 
			print ("(south)")
		else: print ("0")

def g2 ():
	global DescentMovement 
	def DescentMovement(entries):
		aar = float(entries['ascent rate'].get()) 
		h = float(entries['heading'].get())
		das = float(entries['descent airspeed'].get())
		t = float(entries['engine failure'].get())
		t2 = (t * aar) / 6
		adr = float(entries['decsent rate'].get())
		Ycomp = das * t2 * np.cos(h)
		Xcomp = das * t2 * np.sin(h)				
		print ("descent movement: ")
		if (Xcomp > 0):
			print (Xcomp) 
			print ("(east)")
		elif (Xcomp < 0):
			print (Xcomp) 
			print ("(west)")
		else: print ("0")
		if (Ycomp > 0):
			print (Ycomp) 
			print ("(north)")
		elif (Ycomp < 0):
			print (Xcomp) 
			print ("(south)")
		else: print ("0")

def g3 ():
	global WindMovement
	def WindMovement(entries):
		aar = float(entries['ascent rate'].get()) 
		h = float(entries['heading'].get())
		das = float(entries['descent airspeed'].get())
		t = float(entries['engine failure'].get())
		t2 = (t * aar) / 6
		adr = float(entries['decsent rate'].get())
		A = float(entries['a'].get())
		B = float(entries['b'].get())
		C = float(entries['c'].get())
		w = float(entries['wind'].get())
		xpos = (1/3 * A * t2**3 + 1/2 * B * t2**2 + C * t2) * cos(w)
		ypos = (1/3 * A * t2**3 + 1/2 * B * t2**2 + C * t2) * sin(w)
		print ("wind movement: ")
		if (Xpos > 0):
			print (Xcomp) 
			print ("(east)")
		elif (Xcomp < 0):
			print (Xcomp) 
			print ("(west)")
		else: print ("0")
		if (Ycomp > 0):
			print (Ycomp) 
			print ("(north)")
		elif (Ycomp < 0):
			print (Xcomp) 
			print ("(south)")
		else: print ("0")

def g4 ():
	global totMovement
	def totMovement(entries):
		xtot = xcomp + Xcomp + xpos
		ytot = ycomp + Ycomp + ypos
		print ("total movement:" + xtot, ytot)

#def degree (entries):							arctan (sum (sines) / sum (cosines))

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
	b1 = Button(root, text = 'validate', command = g4())			
	#command=(lambda e=ents: g4(e))
	b1.pack(side=LEFT, padx=5, pady=5)
	b3 = Button(root, text='Quit', command=root.quit)
	b3.pack(side=LEFT, padx=5, pady=5)
	root.mainloop()