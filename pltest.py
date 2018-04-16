import numpy as np
import matplotlib.pyplot as plt
import tkinter

#setting the initial figure
plt.figure(figsize=(7, 5), dpi=64)

#plt.subplot(1, 1, 1)

#X = np.linspace(1, 16, 256, endpoint=True)
X = range(1, 17)
Y = [0, 4.4, -4.3, 0, 0, 6.8, -7, 0, 0, 1.6, -1.6, 0, 0, 6.3, -6.4, 0]	
#Z = np.linspace(min(Y), max(Y), 256, endpoint = True)

#plt.tick_params({'x', 'y',})
plt.xticks(np.linspace(0, 16, 17, endpoint=True))
plt.yticks(np.linspace(int(min(Y)), int(max(Y)), 14, endpoint=True))
plt.xlim(0.0, 16.0)
plt.plot(X, Y, color = 'g', linewidth = 2, linestyle = "-") 
plt.grid()


# Set x ticks
#plt.xticks(np.linspace(0, 16, 9, endpoint=True))
#plt.xticks(np.arange(min(int (X)), 17), 1.0)

# Set y ticks
	#plt.yticks(np.linspace(min(Y), max(Y), 5, endpoint=True))

# Save figure using 72 dots per inch
# plt.savefig("fig.png", dpi=72)

# Show result on screen
plt.show()

'''
list = [1,2,3,5,6,4,8,10,11,16,99,-12,-89,-110]
y = min(list)
print (y)
'''
