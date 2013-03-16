# Animates 3 ellipses overlain on a scatterplot
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

num = 10
x = np.random.random(num)
y = np.random.random(num)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
line = ax.plot(x, y, 'bo')

fig.canvas.draw()
bg = fig.canvas.copy_from_bbox(ax.bbox)

# Make and add the ellipses the first time (won't ever be drawn)
ellipses = []
for i in range(3):
    ellip = Ellipse(xy=(0.5, 0.5), width=1, height=1, 
            facecolor='red', alpha=0.5)
    ax.add_patch(ellip)
    ellipses.append(ellip)

# Pseudo-main loop
for i in range(100):
    fig.canvas.restore_region(bg)

    # Update the ellipse artists...
    for ellip in ellipses:
        ellip.width, ellip.height, ellip.angle = np.random.random(3)
        ellip.angle *= 180
        ax.draw_artist(ellip)

    fig.canvas.blit(ax.bbox)