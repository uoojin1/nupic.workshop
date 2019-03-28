import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from matplotlib import style
import sys
import numpy as np

style.use('fivethirtyeight')
fig = plt.figure(figsize=(10,1))

# SDR color
cmap = colors.ListedColormap(['black', 'lightgreen'])
bounds = [0,0.5,1]
norm = colors.BoundaryNorm(bounds, cmap.N)
ax1 = plt.subplot(1,1,1)
ax1.tick_params(
    axis='x',
    bottom=False,
    top=False,
    left=False,
    right=False,
    labelbottom=False
)

def animate(i):
    encoding_data = open('./out/encoding2.csv','r').read()
    totalLines = encoding_data.split('\n')
    line = totalLines[-2]
    last_line = line.split(" ")[:-1]
    # last_line.append('0.0')
    two_dimensional_form = np.array(map(lambda x: float(x), last_line))
    two_d_cpu_encoding = two_dimensional_form.reshape((1,-1))
    ax1.clear()
    ax1.set_title("Feature 3 Encoding: timestamp_weekend")
    ax1.grid(which='major',linewidth='1')
    ax1.set_xticks([])
    ax1.set_yticks([])  
    ax1.imshow(two_d_cpu_encoding, cmap=cmap, norm=norm)

if __name__ == "__main__":
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()