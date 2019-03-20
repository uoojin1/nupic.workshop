import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('./out/realtime_prediction.csv','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys1 = []
    ys2 = []
    for line in lines:
        if len(line) > 1:
            timestamp, prediction, actual = line.split(',')
            if prediction == '' or prediction == None:
                prediction = 0;
            xs.append(timestamp)
            ys1.append(float(prediction))
            ys2.append(float(actual))
    ax1.clear()
    ax1.plot(xs, ys1, 'go--', linewidth=1, markersize=2)
    ax1.plot(xs, ys2, 'rx--', linewidth=1, markersize=2)
    plt.title('Actual CPU vs Predicted CPU')
    plt.xlabel('datetime', fontsize=12)
    plt.ylabel('cpu usage', fontsize=12)

    plt.tick_params(
        axis='x',
        bottom=False,
        labelbottom=False
    )

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()