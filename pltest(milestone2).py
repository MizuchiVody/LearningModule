import numpy as np
import matplotlib.pyplot as plt
from tkinter import * 
import urllib.request
import re
from bs4 import BeautifulSoup

root = Tk()
fr = Frame(root)
fr.pack()

def clean(html):
	soup = BeautifulSoup(html, 'html.parser') # create a new bs4 object from the html data loaded
	for script in soup(["script", "style"]): # remove all javascript and stylesheet code
		script.extract()
	text = soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	text = '\n'.join(chunk for chunk in chunks if chunk)
	return text

page = urllib.request.urlopen("file:///C:/Users/hp/Desktop/data.html", data = None)
content = page.read() 

lb = Label(root, text = clean(content))
lb.pack()
root.mainloop()