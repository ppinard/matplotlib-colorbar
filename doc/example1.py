"""
Draw the example used in the README file.
"""

# Standard library modules.

# Third party modules.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

# Local modules.
from matplotlib_colorbar.colorbar import ColorBar

# Globals and constants variables.


plt.figure()
data = np.array(plt.imread(cbook.get_sample_data('grace_hopper.png')))
mappable = plt.imshow(data[..., 0], cmap='viridis')
colorbar = ColorBar(mappable, location='lower left')
colorbar.set_ticks([0.0, 0.5, 1.0])
plt.gca().add_artist(colorbar)
plt.savefig('example1.png', bbox_inches='tight')
