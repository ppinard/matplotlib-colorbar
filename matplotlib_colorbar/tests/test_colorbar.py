#!/usr/bin/env python
""" """

# Standard library modules.
import sys

# Third party modules.
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.colors
from matplotlib.testing.decorators import cleanup, image_comparison

import numpy as np

import pytest

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

    assert colorbar.get_label() is None
    assert colorbar.label is None

    colorbar.set_label('Hello world')
    assert colorbar.get_label() == 'Hello world'
    assert colorbar.label == 'Hello world'

    colorbar.label = 'Hello world'
    assert colorbar.get_label() == 'Hello world'
    assert colorbar.label == 'Hello world'

    plt.draw()


@cleanup
def test_colorbar_orientation():
    _fig, _ax, colorbar = create_figure()

    with pytest.raises(ValueError):
        colorbar.set_orientation('blah')


@cleanup
def test_colorbar_orientation_vertical():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_orientation() is None
    assert colorbar.orientation is None

    colorbar.set_orientation('vertical')
    assert colorbar.get_orientation() == 'vertical'
    assert colorbar.orientation == 'vertical'

    colorbar.orientation = 'vertical'
    assert colorbar.get_orientation() == 'vertical'
    assert colorbar.orientation == 'vertical'

    plt.draw()


@cleanup
def test_colorbar_orientation_horizontal():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_orientation() is None
    assert colorbar.orientation is None

    colorbar.set_orientation('horizontal')
    assert colorbar.get_orientation() == 'horizontal'
    assert colorbar.orientation == 'horizontal'

    colorbar.orientation = 'horizontal'
    assert colorbar.get_orientation() == 'horizontal'
    assert colorbar.orientation == 'horizontal'

    plt.draw()


@cleanup
def test_colorbar_length_fraction():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_length_fraction() is None
    assert colorbar.length_fraction is None

    colorbar.set_length_fraction(0.2)
    assert colorbar.get_length_fraction() == pytest.approx(0.2, abs=1e-2)
    assert colorbar.length_fraction == pytest.approx(0.2, abs=1e-2)

    colorbar.length_fraction = 0.1
    assert colorbar.get_length_fraction() == pytest.approx(0.1, abs=1e-2)
    assert colorbar.length_fraction == pytest.approx(0.1, abs=1e-2)

    with pytest.raises(ValueError):
        colorbar.set_length_fraction(0.0)
    with pytest.raises(ValueError):
        colorbar.set_length_fraction(1.1)


@cleanup
def test_colorbar_width_fraction():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_width_fraction() is None
    assert colorbar.width_fraction is None

    colorbar.set_width_fraction(0.2)
    assert colorbar.get_width_fraction() == pytest.approx(0.2, abs=1e-2)
    assert colorbar.width_fraction == pytest.approx(0.2, abs=1e-2)

    colorbar.width_fraction = 0.1
    assert colorbar.get_width_fraction() == pytest.approx(0.1, abs=1e-2)
    assert colorbar.width_fraction == pytest.approx(0.1, abs=1e-2)

    with pytest.raises(ValueError):
        colorbar.set_width_fraction(0.0)
    with pytest.raises(ValueError):
        colorbar.set_width_fraction(1.1)


@cleanup
def test_colorbar_location():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_location() is None
    assert colorbar.location is None

    colorbar.set_location('upper right')
    assert colorbar.get_location() == 1
    assert colorbar.location == 1

    colorbar.location = 'lower left'
    assert colorbar.get_location() == 3
    assert colorbar.location == 3

    with pytest.raises(ValueError):
        colorbar.set_location('blah')


@cleanup
def test_colorbar_pad():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_pad() is None
    assert colorbar.pad is None

    colorbar.set_pad(4)
    assert colorbar.get_pad() == pytest.approx(4.0, abs=1e-2)
    assert colorbar.pad == pytest.approx(4.0, abs=1e-2)

    colorbar.pad = 5
    assert colorbar.get_pad() == pytest.approx(5.0, abs=1e-2)
    assert colorbar.pad == pytest.approx(5.0, abs=1e-2)


@cleanup
def test_colorbar_border_pad():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_border_pad() is None
    assert colorbar.border_pad is None

    colorbar.set_border_pad(4)
    assert colorbar.get_border_pad() == pytest.approx(4.0, abs=1e-2)
    assert colorbar.border_pad == pytest.approx(4.0, abs=1e-2)

    colorbar.border_pad = 5
    assert colorbar.get_border_pad() == pytest.approx(5.0, abs=1e-2)
    assert colorbar.border_pad == pytest.approx(5.0, abs=1e-2)


@cleanup
def test_colorbar_box_alpha():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_box_alpha() is None
    assert colorbar.box_alpha is None

    colorbar.set_box_alpha(0.1)
    assert colorbar.get_box_alpha() == pytest.approx(0.1, abs=1e-2)
    assert colorbar.box_alpha == pytest.approx(0.1, abs=1e-2)

    colorbar.box_alpha = 0.2
    assert colorbar.get_box_alpha() == pytest.approx(0.2, abs=1e-2)
    assert colorbar.box_alpha == pytest.approx(0.2, abs=1e-2)

    with pytest.raises(ValueError):
        colorbar.set_box_alpha(-0.1)
    with pytest.raises(ValueError):
        colorbar.set_box_alpha(1.1)


@cleanup
def test_colorbar_sep():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_sep() is None
    assert colorbar.sep is None

    colorbar.set_sep(4)
    assert colorbar.get_sep() == 4
    assert colorbar.sep == 4

    colorbar.sep = 5
    assert colorbar.get_sep() == 5
    assert colorbar.sep == 5


@cleanup
def test_colorbar_frameon():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_frameon() is None
    assert colorbar.frameon is None

    colorbar.set_frameon(True)
    assert colorbar.get_frameon()
    assert colorbar.frameon

    colorbar.frameon = False
    assert not colorbar.get_frameon()
    assert not colorbar.frameon


@cleanup
def test_colorbar_ticks():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_ticks() is None
    assert colorbar.ticks is None

    colorbar.set_ticks([0., 0.5, 1.])
    assert colorbar.get_ticks() == [0., 0.5, 1.]
    assert colorbar.ticks == [0., 0.5, 1.]

    colorbar.ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert colorbar.get_ticks() == [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert colorbar.ticks == [0, 0.2, 0.4, 0.6, 0.8, 1]


@cleanup
def test_colorbar_ticks_nominimum():
    _fig, _ax, colorbar = create_figure()
    colorbar.set_ticks([0.0, 2.0])
    plt.draw()

@cleanup
def test_colorbar_ticklabels():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_ticklabels() is None
    assert colorbar.ticklabels is None

    colorbar.set_ticklabels(['min', 'max'])
    assert colorbar.get_ticklabels() == ['min', 'max']
    assert colorbar.ticklabels == ['min', 'max']

    colorbar.ticklabels = ['small', 'big']
    assert colorbar.get_ticklabels() == ['small', 'big']
    assert colorbar.ticklabels == ['small', 'big']

    colorbar.ticks = [0., 1.]
    with pytest.raises(ValueError):
        colorbar.set_ticklabels(['one label', ])


@cleanup
def test_colorbar_ticklocation():
    _fig, _ax, colorbar = create_figure()

    assert colorbar.get_ticklocation() is None
    assert colorbar.ticklocation is None

    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('bottom')
    assert colorbar.get_ticklocation() == 'bottom'
    assert colorbar.ticklocation == 'bottom'
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('horizontal')
    colorbar.set_ticklocation('top')
    assert colorbar.get_ticklocation() == 'top'
    assert colorbar.ticklocation == 'top'
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('left')
    assert colorbar.get_ticklocation() == 'left'
    assert colorbar.ticklocation == 'left'
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('vertical')
    colorbar.set_ticklocation('right')
    assert colorbar.get_ticklocation() == 'right'
    assert colorbar.ticklocation == 'right'
    colorbar.set_ticklocation(None)

    colorbar.set_orientation('horizontal')
    with pytest.raises(ValueError):
        colorbar.set_ticklocation('left')
    with pytest.raises(ValueError):
        colorbar.set_ticklocation('right')

    colorbar.set_orientation('vertical')
    with pytest.raises(ValueError):
        colorbar.set_ticklocation('bottom')
    with pytest.raises(ValueError):
        colorbar.set_ticklocation('top')

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


@image_comparison(baseline_images=['example1'], extensions=['png'], style='mpl20')
def test_colorbar_example1():
    with cbook.get_sample_data('grace_hopper.png') as fp:
        data = np.array(plt.imread(fp))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot("111", aspect='equal')
    mappable = ax.imshow(data[..., 0], cmap='viridis')
    colorbar = Colorbar(mappable, location='lower left')
    colorbar.set_ticks([0.0, 0.5, 1.0])
    ax.add_artist(colorbar)

@pytest.mark.skipif(sys.version_info < (3, 5),
                    reason="requires python3.5 or higher")
@image_comparison(baseline_images=['example2'], extensions=['png'], style='mpl20')
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

