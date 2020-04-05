#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.colors

import numpy as np

import pytest

# Local modules.
from matplotlib_colorbar.colorbar import Colorbar


# Globals and constants variables.


@pytest.fixture
def figure():
    fig = plt.figure()

    yield fig

    plt.close()
    del fig


@pytest.fixture
def colorbar(figure):
    ax = figure.add_subplot("111")

    data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mappable = ax.imshow(data)

    colorbar = Colorbar(mappable)
    ax.add_artist(colorbar)

    return colorbar


def test_colorbar_draw(colorbar):
    plt.draw()


def test_colorbar_draw_ticklocation_bottom(colorbar):
    colorbar.set_orientation("horizontal")
    colorbar.set_ticklocation("bottom")
    plt.draw()


def test_colorbar_draw_ticklocation_top(colorbar):
    colorbar.set_orientation("horizontal")
    colorbar.set_ticklocation("top")
    plt.draw()


def test_colorbar_draw_ticklocation_left(colorbar):
    colorbar.set_orientation("vertical")
    colorbar.set_ticklocation("left")
    plt.draw()


def test_colorbar_draw_ticklocation_right(colorbar):
    colorbar.set_orientation("vertical")
    colorbar.set_ticklocation("right")
    plt.draw()


def test_colorbar_label(colorbar):
    assert colorbar.get_label() is None
    assert colorbar.label is None

    colorbar.set_label("Hello world")
    assert colorbar.get_label() == "Hello world"
    assert colorbar.label == "Hello world"

    colorbar.label = "Hello world"
    assert colorbar.get_label() == "Hello world"
    assert colorbar.label == "Hello world"

    plt.draw()


def test_colorbar_orientation(colorbar):
    with pytest.raises(ValueError):
        colorbar.set_orientation("blah")


def test_colorbar_orientation_vertical(colorbar):
    assert colorbar.get_orientation() is None
    assert colorbar.orientation is None

    colorbar.set_orientation("vertical")
    assert colorbar.get_orientation() == "vertical"
    assert colorbar.orientation == "vertical"

    colorbar.orientation = "vertical"
    assert colorbar.get_orientation() == "vertical"
    assert colorbar.orientation == "vertical"

    plt.draw()


def test_colorbar_orientation_horizontal(colorbar):
    assert colorbar.get_orientation() is None
    assert colorbar.orientation is None

    colorbar.set_orientation("horizontal")
    assert colorbar.get_orientation() == "horizontal"
    assert colorbar.orientation == "horizontal"

    colorbar.orientation = "horizontal"
    assert colorbar.get_orientation() == "horizontal"
    assert colorbar.orientation == "horizontal"

    plt.draw()


def test_colorbar_length_fraction(colorbar):
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


def test_colorbar_width_fraction(colorbar):
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


def test_colorbar_location(colorbar):
    assert colorbar.get_location() is None
    assert colorbar.location is None

    colorbar.set_location("upper right")
    assert colorbar.get_location() == 1
    assert colorbar.location == 1

    colorbar.location = "lower left"
    assert colorbar.get_location() == 3
    assert colorbar.location == 3

    with pytest.raises(ValueError):
        colorbar.set_location("blah")


def test_colorbar_pad(colorbar):
    assert colorbar.get_pad() is None
    assert colorbar.pad is None

    colorbar.set_pad(4)
    assert colorbar.get_pad() == pytest.approx(4.0, abs=1e-2)
    assert colorbar.pad == pytest.approx(4.0, abs=1e-2)

    colorbar.pad = 5
    assert colorbar.get_pad() == pytest.approx(5.0, abs=1e-2)
    assert colorbar.pad == pytest.approx(5.0, abs=1e-2)


def test_colorbar_border_pad(colorbar):
    assert colorbar.get_border_pad() is None
    assert colorbar.border_pad is None

    colorbar.set_border_pad(4)
    assert colorbar.get_border_pad() == pytest.approx(4.0, abs=1e-2)
    assert colorbar.border_pad == pytest.approx(4.0, abs=1e-2)

    colorbar.border_pad = 5
    assert colorbar.get_border_pad() == pytest.approx(5.0, abs=1e-2)
    assert colorbar.border_pad == pytest.approx(5.0, abs=1e-2)


def test_colorbar_box_alpha(colorbar):
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


def test_colorbar_sep(colorbar):
    assert colorbar.get_sep() is None
    assert colorbar.sep is None

    colorbar.set_sep(4)
    assert colorbar.get_sep() == 4
    assert colorbar.sep == 4

    colorbar.sep = 5
    assert colorbar.get_sep() == 5
    assert colorbar.sep == 5


def test_colorbar_frameon(colorbar):
    assert colorbar.get_frameon() is None
    assert colorbar.frameon is None

    colorbar.set_frameon(True)
    assert colorbar.get_frameon()
    assert colorbar.frameon

    colorbar.frameon = False
    assert not colorbar.get_frameon()
    assert not colorbar.frameon


def test_colorbar_ticks(colorbar):
    assert colorbar.get_ticks() is None
    assert colorbar.ticks is None

    colorbar.set_ticks([0.0, 0.5, 1.0])
    assert colorbar.get_ticks() == [0.0, 0.5, 1.0]
    assert colorbar.ticks == [0.0, 0.5, 1.0]

    colorbar.ticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert colorbar.get_ticks() == [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert colorbar.ticks == [0, 0.2, 0.4, 0.6, 0.8, 1]


def test_colorbar_ticks_nominimum(colorbar):

    colorbar.set_ticks([0.0, 2.0])
    plt.draw()


def test_colorbar_ticklabels(colorbar):
    assert colorbar.get_ticklabels() is None
    assert colorbar.ticklabels is None

    colorbar.set_ticklabels(["min", "max"])
    assert colorbar.get_ticklabels() == ["min", "max"]
    assert colorbar.ticklabels == ["min", "max"]

    colorbar.ticklabels = ["small", "big"]
    assert colorbar.get_ticklabels() == ["small", "big"]
    assert colorbar.ticklabels == ["small", "big"]

    colorbar.ticks = [0.0, 1.0]
    with pytest.raises(ValueError):
        colorbar.set_ticklabels(
            ["one label",]
        )


def test_colorbar_ticklocation(colorbar):
    assert colorbar.get_ticklocation() is None
    assert colorbar.ticklocation is None

    colorbar.set_orientation("horizontal")
    colorbar.set_ticklocation("bottom")
    assert colorbar.get_ticklocation() == "bottom"
    assert colorbar.ticklocation == "bottom"
    colorbar.set_ticklocation(None)

    colorbar.set_orientation("horizontal")
    colorbar.set_ticklocation("top")
    assert colorbar.get_ticklocation() == "top"
    assert colorbar.ticklocation == "top"
    colorbar.set_ticklocation(None)

    colorbar.set_orientation("vertical")
    colorbar.set_ticklocation("left")
    assert colorbar.get_ticklocation() == "left"
    assert colorbar.ticklocation == "left"
    colorbar.set_ticklocation(None)

    colorbar.set_orientation("vertical")
    colorbar.set_ticklocation("right")
    assert colorbar.get_ticklocation() == "right"
    assert colorbar.ticklocation == "right"
    colorbar.set_ticklocation(None)

    colorbar.set_orientation("horizontal")
    with pytest.raises(ValueError):
        colorbar.set_ticklocation("left")
    with pytest.raises(ValueError):
        colorbar.set_ticklocation("right")

    colorbar.set_orientation("vertical")
    with pytest.raises(ValueError):
        colorbar.set_ticklocation("bottom")
    with pytest.raises(ValueError):
        colorbar.set_ticklocation("top")


def test_colorbar_set_visible(colorbar):
    colorbar.set_visible(False)
    plt.draw()


def test_colorbar_no_mappable(colorbar):
    colorbar.set_mappable(False)
    plt.draw()


@pytest.mark.mpl_image_compare
def test_colorbar_example1(colorbar):
    with cbook.get_sample_data("grace_hopper.png") as fp:
        data = np.array(plt.imread(fp))

    fig = plt.figure()
    ax = fig.add_subplot("111", aspect="equal")
    mappable = ax.imshow(data[..., 0], cmap="viridis")
    colorbar = Colorbar(mappable, location="lower left")
    colorbar.set_ticks([0.0, 0.5, 1.0])
    ax.add_artist(colorbar)

    return fig


@pytest.mark.mpl_image_compare
def test_colorbar_example2():
    with cbook.get_sample_data("grace_hopper.png") as fp:
        data = np.array(plt.imread(fp))

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot("111", aspect="equal")
    norm = matplotlib.colors.Normalize(vmin=-1.0, vmax=1.0)
    mappable = ax.imshow(data[..., 0], cmap="viridis", norm=norm)
    colorbar = Colorbar(mappable, location="lower left")
    colorbar.set_ticks([-1.0, 0, 1.0])
    ax.add_artist(colorbar)

    return fig
