"""
Sphinx Gallery Demo
===================

This is a simple example demonstrating the Sphinx Gallery integration
with the PyTorch Sphinx Theme.

NumPy Arrays
------------

Let's create some arrays and demonstrate basic operations.

"""

import numpy as np

######################################################################
# First, let's create some arrays:
#

z = np.zeros((5, 3))
print(z)
print(z.dtype)

######################################################################
# We can also create arrays with random values:
#

x = np.random.randn(3, 3)
print(x)

######################################################################
# Plotting with Matplotlib
# ------------------------
#
# The gallery can also display plots:

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_title('Simple Plot')
plt.show()
