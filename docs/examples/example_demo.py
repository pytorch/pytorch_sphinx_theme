"""
Introduction to PyTorch
=======================

Follow along with the video below or on `youtube <https://www.youtube.com/watch?v=IC0_FRiX-sw>`__.

.. raw:: html

   <div style="margin-top:10px; margin-bottom:10px;">
     <iframe width="560" height="315" src="https://www.youtube.com/embed/IC0_FRiX-sw" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
   </div>

PyTorch Tensors
---------------

Follow along with the video beginning at `03:50 <https://www.youtube.com/watch?v=IC0_FRiX-sw&t=230s>`__.

First, we’ll import pytorch.

"""

import torch

######################################################################
# Let’s see a few basic tensor manipulations. First, just a few of the
# ways to create tensors:
# 

z = torch.zeros(5, 3)
print(z)
print(z.dtype)
