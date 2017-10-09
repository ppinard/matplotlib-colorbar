matplotlib-colorbar
===================

.. image:: https://travis-ci.org/ppinard/matplotlib-colorbar.svg
   :target: https://travis-ci.org/ppinard/matplotlib-colorbar

.. image:: https://badge.fury.io/py/matplotlib-colorbar.svg
   :target: http://badge.fury.io/py/matplotlib-colorbar

.. image:: https://codecov.io/github/ppinard/matplotlib-colorbar/coverage.svg?branch=master
   :target: https://codecov.io/github/ppinard/matplotlib-colorbar?branch=master
   
Provides a new artist for matplotlib to display a colorbar,
instead of an axis as it is the default in matplotlib.
The position of the colorbar artist can be decided as for the legend.

.. image:: https://raw.githubusercontent.com/ppinard/matplotlib-colorbar/master/doc/example1.png

The artist supports customization either directly from the *Colorbar* object or
from the matplotlibrc.

Installation
------------

Easiest way to install using ``pip``::

    $ pip install matplotlib-colorbar

For development installation from the git repository::

    $ git clone git@github.com:ppinard/matplotlib-colorbar.git
    $ pip install -e matplotlib-colorbar

Example
-------

Here is an example how to add a color bar::

   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> import matplotlib.cbook as cbook
   >>> from matplotlib_colorbar.colorbar import Colorbar
   >>> plt.figure()
   >>> data = np.array(plt.imread(cbook.get_sample_data('grace_hopper.png')))
   >>> mappable = plt.imshow(data[...,0], cmap='viridis')
   >>> colorbar = Colorbar(mappable, location='lower left')
   >>> colorbar.set_ticks([0.0, 0.5, 1.0])
   >>> plt.gca().add_artist(colorbar)
   >>> plt.show()

Colorbar arguments
------------------

Here are parameters of the **Colorbar** class constructor.

* ``mappable``: scalar mappable object which implements the methods *get_cmap* and *get_array* (default: ``None``, the mappable can be specified later)
* ``label``: label on top of the color bar (default: ``None``, no label is shown)
* ``orientation``: orientation, ``vertical`` or ``horizontal`` (default: ``vertical``)
* ``length_fraction``: length of the color bar as a fraction of the axes's width (horizontal) or height (vertical) depending on the orientation (default: ``0.2``)
* ``width_fraction``: width of the color bar as a fraction of the axes's height (horizontal) or width (vertical) depending on the orientation (default: ``0.02``)
* ``location``: a location code (same as legend) (default: ``upper right``)
* ``pad``: fraction of the font size (default: ``0.2``)
* ``border_pad``: fraction of the font size (default: ``0.1``)
* ``sep``: separation between color bar and label in points (default: ``5``)
* ``frameon``: if True, will draw a box around the color bar (default: ``True``)
* ``color``: color for the tick text and label (default: ``k``)
* ``box_color``: color of the box (if *frameon*) (default: ``w``)
* ``box_alpha``: transparency of box (default: ``1.0``)
* ``font_properties``: font properties of the label text, specified either as dict or `fontconfig <http://www.fontconfig.org/>`_ pattern (XML).
* ``ticks``: ticks location (default: minimal and maximal values)
* ``ticklabels``: a list of tick labels (same length as ``ticks`` argument)
* ``ticklocation``: location of the ticks: ``left`` or ``right`` for vertical oriented colorbar, ``bottom`` or ``top for horizontal oriented colorbar, or ``auto`` for automatic adjustment (``right`` for vertical and ``bottom`` for horizontal oriented colorbar). (default: ``auto``)

matplotlibrc parameters
-----------------------

Here are parameters that can be customized in the matplotlibrc file.

* ``orientation``: orientation, ``vertical`` or ``horizontal`` (default: ``vertical``)
* ``length_fraction``: length of the color bar as a fraction of the axes's width (horizontal) or height (vertical) depending on the orientation (default: ``0.2``)
* ``width_fraction``: width of the color bar as a fraction of the axes's height (horizontal) or width (vertical) depending on the orientation (default: ``0.02``)
* ``location``: a location code (same as legend) (default: ``upper right``)
* ``pad``: fraction of the font size (default: ``0.2``)
* ``border_pad``: fraction of the font size (default: ``0.1``)
* ``sep``: separation between color bar and label in points (default: ``5``)
* ``frameon``: if True, will draw a box around the color bar (default: ``True``)
* ``color``: color for the tick text and label (default: ``k``)
* ``box_color``: color of the box (if *frameon*) (default: ``w``)
* ``box_alpha``: transparency of box (default: ``1.0``)
* ``ticklocation``: location of the ticks (default: ``auto``)

Release notes
-------------
0.3.6
^^^^^

* Fix deprecated usage of is_string_like

0.3.5
^^^^^

* Fix: UserWarning This call to matplotlib.use() has no effect (`#9 <https://github.com/ppinard/matplotlib-colorbar/issues/9>`_)

Contributors
------------

`@cphyc <https://github.com/cphyc>`_ and `@jnth <https://github.com/jnth>`_

License
-------

License under the BSD License, compatible with matplotlib.

Copyright (c) 2015-2017 Philippe Pinard
