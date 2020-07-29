from main import generate

from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np

z = generate(6, 3)
x = np.arange(len(z))
y = np.arange(len(z))

X, Y = np.meshgrid(x, y)

# Set up plot
# fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
fig = plt.figure()
ax = fig.gca(projection='3d')

ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(z, cmap=cm.jet, vert_exag=0.1, blend_mode='soft')
# surf = ax.plot_surface(X, Y, z)
ax.set_zlim(-10, 10)
surf = ax.plot_surface(X, Y, z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)

plt.show()