import numpy as np
import matplotlib.pyplot as plt
from tkinter import * 
import urllib.request
import re
from bs4 import BeautifulSoup

'''
root = Tk()
fr = Frame(root)
fr.pack()
'''

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
print (re.findall (r"[-+]?\d*\.\d+|\d+", clean(content)))

#lb = Label(root, text = clean(content))
#lb.pack()
#root.mainloop()
'''
plt.figure(figsize=(7, 5), dpi=64)

X = range(1, 17)
Y = [0, 4.4, -4.3, 0, 0, 6.8, -7, 0, 0, 1.6, -1.6, 0, 0, 6.3, -6.4, 0]	#how to load these numbers from the web browser ?

plt.xticks(np.linspace(0, 16, 17, endpoint=True))
plt.yticks(np.linspace(int(min(Y)), int(max(Y)), 14, endpoint=True))

plt.xlim(0.0, 16.0)

plt.plot(X, Y, color = 'g', linewidth = 2, linestyle = "-") 
plt.grid()
plt.show()
'''
