#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.testing.decorators import cleanup, image_comparison

import numpy as np

from nose.tools import \
    (assert_equal, assert_almost_equal, assert_is_none, assert_true,
     assert_false, assert_raises)

# Local modules.
from matplotlib_colorbar.colorbar import Colorbar


# Globals and constants variables.

def create_figure():
    fig = plt.figure()
    ax = fig.add_subplot("111")

    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mappable = ax.imshow(data)

    colorbar = Colorbar(mappable)
    ax.add_artist(colorbar)

    return fig, ax, colorbar


@cleanup
def test_colorbar_draw():
    create_figure()
    plt.draw()


@cleanup
def test_colorbar_draw_ticklocation_bottom():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('bottom')
    plt.draw()


@cleanup
def test_colorbar_draw_ticklocation_top():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('top')
    plt.draw()


@cleanup
def test_colorbar_draw_ticklocation_left():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('left')
    plt.draw()


@cleanup
def test_colorbar_draw_ticklocation_right():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('right')
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
    assert_raises(ValueError, colorbar.set_orientation, 'blah')


@cleanup
def test_colorbar_orientation_vertical():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_orientation())
    assert_is_none(colorbar.orientation)

    colorbar.set_orientation('vertical')
    assert_equal('vertical', colorbar.get_orientation())
    assert_equal('vertical', colorbar.orientation)

    colorbar.orientation = 'vertical'
    assert_equal('vertical', colorbar.get_orientation())
    assert_equal('vertical', colorbar.orientation)

    plt.draw()


@cleanup
def test_colorbar_orientation_horizontal():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_orientation())
    assert_is_none(colorbar.orientation)

    colorbar.set_orientation('horizontal')
    assert_equal('horizontal', colorbar.get_orientation())
    assert_equal('horizontal', colorbar.orientation)

    colorbar.orientation = 'horizontal'
    assert_equal('horizontal', colorbar.get_orientation())
    assert_equal('horizontal', colorbar.orientation)

    plt.draw()


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

    assert_raises(ValueError, colorbar.set_location, 'blah')


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
def test_colorbar_box_alpha():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_box_alpha())
    assert_is_none(colorbar.box_alpha)

    colorbar.set_box_alpha(0.1)
    assert_almost_equal(0.1, colorbar.get_box_alpha())
    assert_almost_equal(0.1, colorbar.box_alpha)

    colorbar.box_alpha = 0.2
    assert_almost_equal(0.2, colorbar.get_box_alpha())
    assert_almost_equal(0.2, colorbar.box_alpha)

    assert_raises(ValueError, colorbar.set_box_alpha, -0.1)
    assert_raises(ValueError, colorbar.set_box_alpha, 1.1)


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
def test_colorbar_ticks_nominimum():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_ticks([0.0, 2.0])
    plt.draw()

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


@cleanup
def test_colorbar_ticklocation():
    _fig, _ax, colorbar = create_figure()

    assert_is_none(colorbar.get_ticklocation())
    assert_is_none(colorbar.ticklocation)

    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('bottom')
    assert_equal('bottom', colorbar.get_ticklocation())
    assert_equal('bottom', colorbar.ticklocation)
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('top')
    assert_equal('top', colorbar.get_ticklocation())
    assert_equal('top', colorbar.ticklocation)
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('left')
    assert_equal('left', colorbar.get_ticklocation())
    assert_equal('left', colorbar.ticklocation)
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('right')
    assert_equal('right', colorbar.get_ticklocation())
    assert_equal('right', colorbar.ticklocation)
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('horizontal')
    assert_raises(ValueError, colorbar.set_ticklocation, 'left')
    assert_raises(ValueError, colorbar.set_ticklocation, 'right')

    colorbar.set_orientation('vertical')
    assert_raises(ValueError, colorbar.set_ticklocation, 'bottom')
    assert_raises(ValueError, colorbar.set_ticklocation, 'top')

@cleanup
def test_colorbar_set_visible():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_visible(False)
    plt.draw()


@cleanup
def test_colorbar_no_mappable():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_mappable(False)
    plt.draw()


@image_comparison(baseline_images=['example1'], extensions=['png'])
def test_colorbar_example1():
    with cbook.get_sample_data('grace_hopper.png') as fp:
        data = np.array(plt.imread(fp))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot("111", aspect='equal')
    mappable = ax.imshow(data[..., 0], cmap='viridis')
    colorbar = Colorbar(mappable, location='lower left')
    colorbar.set_ticks([0.0, 0.5, 1.0])
    ax.add_artist(colorbar)


@image_comparison(baseline_images=['example2'], extensions=['png'])
def test_colorbar_example2():
    with cbook.get_sample_data('grace_hopper.png') as fp:
        data = np.array(plt.imread(fp))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot("111", aspect='equal')
    norm = matplotlib.colors.Normalize(vmin=-1.0, vmax=1.0)
    mappable = ax.imshow(data[..., 0], cmap='viridis', norm=norm)
    colorbar = Colorbar(mappable, location='lower left')
    colorbar.set_ticks([-1.0, 0, 1.0])
    ax.add_artist(colorbar)


if __name__ == '__main__':
    import nose
    import sys

    args = ['-s', '--with-doctest']
    argv = sys.argv
    argv = argv[:1] + args + argv[1:]
    nose.runmodule(argv=argv, exit=False)
