import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import sys

style.use('fivethirtyeight')
fig = plt.figure(figsize=(10,6))
ax1 = plt.subplot(2,1,1)
ax2 = plt.subplot(2,1,2)

ax1.tick_params(
    axis='x',
    bottom=False,
    labelbottom=False
)
ax2.tick_params(
    axis='x',
    bottom=False,
    labelbottom=False,
    labelsize=2
)

def animate(i):
    graph_data = open('./out/realtime_prediction.csv','r').read()
    lines = graph_data.split('\n')
    lines = lines[-60:] # only use last 60 items
    xs, ys1, ys2, acc = [], [], [], []

    for line in lines:
        if len(line) > 1:
            timestamp, prediction, actual = line.split(',')
            if prediction == '' or prediction == None:
                prediction = 0;
            xs.append(timestamp)
            ys1.append(float(prediction))
            ys2.append(float(actual))
            acc.append(float(prediction) - float(actual))

    # usage
    ax1.clear()
    ax1.set_title("{}'s {}. prediction VS actual values".format(device, resourceType), fontsize=10)
    ax1.set_ylim(-5,100)
    ax1.set_ylabel('{} usage (%)'.format(resourceType), fontsize=10)
    ax1.plot(xs, ys1, 'ro--', linewidth=1, markersize=2, label='prediction')
    ax1.plot(xs, ys2, 'black', linewidth=1, markersize=2, label='actual')
    ax1.legend(loc='upper right')

    # accuracy
    ax2.clear()
    ax2.set_title('prediction error', fontsize=10)
    ax2.plot(xs, acc, 'go--', linewidth=1, markersize=2, label='error')
    ax2.set_ylim(-100,100)
    ax2.set_ylabel('error', fontsize=10)
    ax2.legend(loc='upper right')


if __name__ == "__main__":

    device, resourceType = 'UE', 'CPU'
    if len(sys.argv) > 2:
        device, resourceType = sys.argv[1], sys.argv[2]

    ani = animation.FuncAnimation(fig, animate, interval=200)
    plt.show()