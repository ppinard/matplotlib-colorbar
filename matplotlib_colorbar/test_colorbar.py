#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import cleanup

import numpy as np

from nose.tools import \
    (assert_equal, assert_almost_equal, assert_is_none, assert_true,
     assert_false, assert_raises)

# Local modules.
from matplotlib_colorbar.colorbar import ColorBar


# Globals and constants variables.

def create_figure():
    fig = plt.figure()
    ax = fig.add_subplot("111")

    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mappable = ax.imshow(data)

    colorbar = ColorBar(mappable)
    ax.add_artist(colorbar)

    return fig, ax, colorbar


@cleanup
def test_colorbar_draw():
    create_figure()
    plt.draw()


@cleanup
def test_colorbar_label():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_label())
    assert_is_none(colorbar.label)

    colorbar.set_label('Hello world')
    assert_equal('Hello world', colorbar.get_label())
    assert_equal('Hello world', colorbar.label)

    colorbar.label = 'Hello world'
    assert_equal('Hello world', colorbar.get_label())
    assert_equal('Hello world', colorbar.label)

    plt.draw()


@cleanup
def test_colorbar_orientation():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_orientation())
    assert_is_none(colorbar.orientation)

    colorbar.set_orientation('vertical')
    assert_equal('vertical', colorbar.get_orientation())
    assert_equal('vertical', colorbar.orientation)

    colorbar.orientation = 'vertical'
    assert_equal('vertical', colorbar.get_orientation())
    assert_equal('vertical', colorbar.orientation)

    assert_raises(ValueError, colorbar.set_orientation, 'blah')


@cleanup
def test_colorbar_nbins():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_nbins())
    assert_is_none(colorbar.nbins)

    colorbar.set_nbins(25)
    assert_equal(25, colorbar.get_nbins())
    assert_equal(25, colorbar.nbins)

    colorbar.nbins = 25
    assert_equal(25, colorbar.get_nbins())
    assert_equal(25, colorbar.nbins)

    assert_raises(ValueError, colorbar.set_nbins, 0)


@cleanup
def test_colorbar_length_fraction():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_length_fraction())
    assert_is_none(colorbar.length_fraction)

    colorbar.set_length_fraction(0.2)
    assert_almost_equal(0.2, colorbar.get_length_fraction())
    assert_almost_equal(0.2, colorbar.length_fraction)

    colorbar.length_fraction = 0.1
    assert_almost_equal(0.1, colorbar.get_length_fraction())
    assert_almost_equal(0.1, colorbar.length_fraction)

    assert_raises(ValueError, colorbar.set_length_fraction, 0.0)
    assert_raises(ValueError, colorbar.set_length_fraction, 1.1)


@cleanup
def test_colorbar_width_fraction():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_width_fraction())
    assert_is_none(colorbar.width_fraction)

    colorbar.set_width_fraction(0.2)
    assert_almost_equal(0.2, colorbar.get_width_fraction())
    assert_almost_equal(0.2, colorbar.width_fraction)

    colorbar.width_fraction = 0.1
    assert_almost_equal(0.1, colorbar.get_width_fraction())
    assert_almost_equal(0.1, colorbar.width_fraction)

    assert_raises(ValueError, colorbar.set_width_fraction, 0.0)
    assert_raises(ValueError, colorbar.set_width_fraction, 1.1)


@cleanup
def test_colorbar_location():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_location())
    assert_is_none(colorbar.location)

    colorbar.set_location('upper right')
    assert_equal(1, colorbar.get_location())
    assert_equal(1, colorbar.location)

    colorbar.location = 'lower left'
    assert_equal(3, colorbar.get_location())
    assert_equal(3, colorbar.location)


@cleanup
def test_colorbar_pad():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_pad())
    assert_is_none(colorbar.pad)

    colorbar.set_pad(4)
    assert_almost_equal(4, colorbar.get_pad())
    assert_almost_equal(4, colorbar.pad)

    colorbar.pad = 5
    assert_almost_equal(5, colorbar.get_pad())
    assert_almost_equal(5, colorbar.pad)


@cleanup
def test_colorbar_border_pad():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_border_pad())
    assert_is_none(colorbar.border_pad)

    colorbar.set_border_pad(4)
    assert_almost_equal(4, colorbar.get_border_pad())
    assert_almost_equal(4, colorbar.border_pad)

    colorbar.border_pad = 5
    assert_almost_equal(5, colorbar.get_border_pad())
    assert_almost_equal(5, colorbar.border_pad)


@cleanup
def test_colorbar_sep():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_sep())
    assert_is_none(colorbar.sep)

    colorbar.set_sep(4)
    assert_almost_equal(4, colorbar.get_sep())
    assert_almost_equal(4, colorbar.sep)

    colorbar.sep = 5
    assert_almost_equal(5, colorbar.get_sep())
    assert_almost_equal(5, colorbar.sep)


@cleanup
def test_colorbar_frameon():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_frameon())
    assert_is_none(colorbar.frameon)

    colorbar.set_frameon(True)
    assert_true(colorbar.get_frameon())
    assert_true(colorbar.frameon)

    colorbar.frameon = False
    assert_false(colorbar.get_frameon())
    assert_false(colorbar.frameon)


@cleanup
def test_colorbar_ticks():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_ticks())
    assert_is_none(colorbar.ticks)

    colorbar.set_ticks([0., 0.5, 1.])
    assert_equal([0., 0.5, 1.], colorbar.get_ticks())
    assert_equal([0., 0.5, 1.], colorbar.ticks)

    colorbar.ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert_equal([0, 0.2, 0.4, 0.6, 0.8, 1], colorbar.get_ticks())
    assert_equal([0, 0.2, 0.4, 0.6, 0.8, 1], colorbar.ticks)


@cleanup
def test_colorbar_ticklabels():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_ticklabels())
    assert_is_none(colorbar.ticklabels)

    colorbar.set_ticklabels(['min', 'max'])
    assert_equal(['min', 'max'], colorbar.get_ticklabels())
    assert_equal(['min', 'max'], colorbar.ticklabels)

    colorbar.ticklabels = ['small', 'big']
    assert_equal(['small', 'big'], colorbar.get_ticklabels())
    assert_equal(['small', 'big'], colorbar.ticklabels)

    colorbar.ticks = [0., 1.]
    assert_raises(ValueError, colorbar.set_ticklabels, ['one label', ])


if __name__ == '__main__':
    import nose
    import sys

    args = ['-s', '--with-doctest']
    argv = sys.argv
    argv = argv[:1] + args + argv[1:]
    nose.runmodule(argv=argv, exit=False)
