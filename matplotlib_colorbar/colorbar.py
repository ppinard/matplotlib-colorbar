"""
Artist for matplotlib to display a colorbar as an artist,
instead of an axis as it is the default in matplotlib.

Example::

   >>> fig = plt.figure()
   >>> ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
   >>> mappable = ax.imshow(...)
   >>> colorbar = ColorBar(mappable)
   >>> ax.add_artist(scalebar)
   >>> plt.show()

The following parameters are available for customization in the matplotlibrc:
    - colorbar.orientation
    - colorbar.length_fraction
    - colorbar.width_fraction
    - colorbar.location
    - colorbar.pad
    - colorbar.border_pad
    - colorbar.sep
    - colorbar.frameon
    - colorbar.color
    - colorbar.box_color
    - colorbar.box_alpha
    - colorbar.ticklocation

See the class documentation (:class:`.ColorBar`) for a description of the
parameters.
"""

# Standard library modules.
import warnings

# Third party modules.
import matplotlib
from matplotlib.rcsetup import \
    (defaultParams, ValidateInStrings, validate_float,
     validate_legend_loc, validate_bool, validate_color)
from matplotlib.artist import Artist
from matplotlib.offsetbox import \
    AnchoredOffsetbox, AuxTransformBox, VPacker, HPacker
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.text import Text
from matplotlib.font_manager import FontProperties
from matplotlib.colorbar import ColorbarBase
import matplotlib.contour as contour
import matplotlib.ticker as ticker

import numpy as np

import six

import packaging.version

# Local modules.

# Globals and constants variables.

__all__ = ['ColorBar']

# Setup of extra parameters in the matplotlic rc
validate_orientation = ValidateInStrings('orientation',
                                         ['horizontal', 'vertical'])
validate_ticklocation = ValidateInStrings('orientation',
                                          ['auto', 'left', 'right', 'bottom', 'top'])

defaultParams.update(
    {'colorbar.orientation': ['vertical', validate_orientation],
     'colorbar.ticklocation': ['auto', validate_ticklocation],
     'colorbar.length_fraction': [0.2, validate_float],
     'colorbar.width_fraction': [0.02, validate_float],
     'colorbar.location': ['upper right', validate_legend_loc],
     'colorbar.pad': [0.2, validate_float],
     'colorbar.border_pad': [0.1, validate_float],
     'colorbar.sep': [5, validate_float],
     'colorbar.frameon': [True, validate_bool],
     'colorbar.color': ['k', validate_color],
     'colorbar.box_color': ['w', validate_color],
     'colorbar.box_alpha': [1.0, validate_float],
     })

# Recreate the validate function
matplotlib.rcParams.validate = \
    dict((key, converter) for key, (default, converter) in
         six.iteritems(defaultParams)
         if key not in matplotlib._all_deprecated)

class ColorbarBase2(ColorbarBase):
    """
    Disable some methods from the original :class:`ColorbarBase` class of
    matplotlib that required an :class:`Axes` object.
    """

    def _set_label(self):
        pass

    def _patch_ax(self):
        pass

    def _config_axes(self, X, Y):
        pass

    def config_axis(self):
        pass

    def draw_all(self):
        pass

class ColorbarCalculator(object):
    """
    Internally computes the values to draw a colorbar without actually drawing
    it as in the original :class:`ColorbarBase` class from matplotlib.
    """

    def __init__(self, mappable, **kw):
        # Ensure the given mappable's norm has appropriate vmin and vmax set
        # even if mappable.draw has not yet been called.
        mappable.autoscale_None()

        self.mappable = mappable
        kw['cmap'] = cmap = mappable.cmap
        kw['norm'] = mappable.norm

        if isinstance(mappable, contour.ContourSet):
            CS = mappable
            kw['alpha'] = mappable.get_alpha()
            kw['boundaries'] = CS._levels
            kw['values'] = CS.cvalues
            kw['extend'] = CS.extend
            #kw['ticks'] = CS._levels
            kw.setdefault('ticks', ticker.FixedLocator(CS.levels, nbins=10))
            kw['filled'] = CS.filled

        else:
            if getattr(cmap, 'colorbar_extend', False) is not False:
                kw.setdefault('extend', cmap.colorbar_extend)

            if isinstance(mappable, Artist):
                kw['alpha'] = mappable.get_alpha()

        ticks = kw.pop('ticks', None)
        ticklabels = kw.pop('ticklabels', None)

        self._base = ColorbarBase2(None, **kw)
        if ticks:
            self._base.set_ticks(ticks, update_ticks=False)
        if ticks and ticklabels:
            self._base.set_ticklabels(ticklabels, update_ticks=False)

    def calculate_colorbar(self):
        """
        Returns the positions and colors of all intervals inside the colorbar.
        """
        self._base._process_values()
        self._base._find_range()
        X, Y = self._base._mesh()
        C = self._base._values[:, np.newaxis]
        return X, Y, C

    def calculate_ticks(self):
        """
        Returns the sequence of ticks (colorbar data locations),
        ticklabels (strings), and the corresponding offset string.
        """
        current_version = packaging.version.parse(matplotlib.__version__)
        critical_version = packaging.version.parse('3.0.0')

        if current_version > critical_version:
            locator, formatter = self._base._get_ticker_locator_formatter()
            return self._base._ticker(locator, formatter)
        else:
            return self._base._ticker()

class Colorbar(Artist):

    zorder = 5

    _LOCATIONS = {'upper right':  1,
                  'upper left':   2,
                  'lower left':   3,
                  'lower right':  4,
                  'right':        5,
                  'center left':  6,
                  'center right': 7,
                  'lower center': 8,
                  'upper center': 9,
                  'center':       10}

    def __init__(self, mappable=None, label=None, orientation=None,
                 length_fraction=None, width_fraction=None,
                 location=None, pad=None, border_pad=None, sep=None,
                 frameon=None, color=None, box_color=None, box_alpha=None,
                 font_properties=None, ticks=None, ticklabels=None,
                 ticklocation=None):
        """
        Creates a new color bar.

        :arg mappable: scalar mappable object which implements the methods:
            :meth:`get_cmap` and :meth:`get_array`
            (default: ``None``, the mappable can be specified later)
        :arg label: label on top of the color bar
            (default: ``None``, no label is shown)
        :arg orientation: orientation, ``vertical`` or ``horizontal``
            (default: rcParams['colorbar.orientation'] or ``vertical``)
        :arg length_fraction: length of the color bar as a fraction of the
            axes's width (horizontal) or height (vertical) depending on the
            orientation (default: rcParams['colorbar.length_fraction'] or ``0.2``)
        :arg width_fraction: width of the color bar as a fraction of the
            axes's height (horizontal) or width (vertical) depending on the
            orientation (default: rcParams['colorbar.width_fraction'] or ``0.02``
        :arg location: a location code (same as legend)
            (default: rcParams['colorbar.location'] or ``upper right``)
        :arg pad: fraction of the font size
            (default: rcParams['colorbar.pad'] or ``0.2``)
        :arg border_pad: fraction of the font size
            (default: rcParams['colorbar.border_pad'] or ``0.1``)
        :arg sep: separation between color bar and label in points
            (default: rcParams['colorbar.sep'] or ``5``)
        :arg frameon: if True, will draw a box around the color bar
            (default: rcParams['colorbar.frameon'] or ``True``)
        :arg color: color for the tick text and label
            (default: rcParams['colorbar.color'] or ``k``)
        :arg box_color: color of the box (if *frameon*)
            (default: rcParams['colorbar.box_color'] or ``w``)
        :arg box_alpha: transparency of box
            (default: rcParams['colorbar.box_alpha'] or ``1.0``)
        
        :arg font_properties: font properties of the label text, specified
            either as dict or `fontconfig <http://www.fontconfig.org/>`_
            pattern (XML).
        :type font_properties: :class:`matplotlib.font_manager.FontProperties`,
            :class:`str` or :class:`dict`
        
        :arg ticks: ticks location
            (default: minimal and maximal values)
        :arg ticklabels: a list of tick labels (same length as ``ticks`` argument)
        :arg ticklocation: location of the ticks: ``left`` or ``right`` for
            vertical oriented colorbar, ``bottom`` or ``top for horizontal
            oriented colorbar, or ``auto`` for automatic adjustment (``right``
            for vertical and ``bottom`` for horizontal oriented colorbar).
            (default: rcParams['colorbar.ticklocation'] or ``auto``)
        """
        Artist.__init__(self)

        self.mappable = mappable
        self.label = label
        self.orientation = orientation
        self.length_fraction = length_fraction
        self.width_fraction = width_fraction
        self.location = location
        self.pad = pad
        self.border_pad = border_pad
        self.sep = sep
        self.frameon = frameon
        self.color = color
        self.box_color = box_color
        self.box_alpha = box_alpha

        if font_properties is None:
            font_properties = FontProperties()
        elif isinstance(font_properties, dict):
            font_properties = FontProperties(**font_properties)
        elif isinstance(font_properties, six.string_types):
            font_properties = FontProperties(font_properties)
        else:
            raise TypeError("Unsupported type for `font_properties`. Pass "
                            "either a dict or a font config pattern as string.")
        self.font_properties = font_properties

        self.ticks = ticks
        self.ticklabels = ticklabels
        self.ticklocation = ticklocation

    def draw(self, renderer, *args, **kwargs):
        if not self.get_visible():
            return
        if not self.get_mappable():
            return

        # Get parameters
        from matplotlib import rcParams  # late import

        def _get_value(attr, default):
            value = getattr(self, attr)
            if value is None:
                value = rcParams.get('colorbar.' + attr, default)
            return value
        orientation = _get_value('orientation', 'vertical')
        length_fraction = _get_value('length_fraction', 0.2)
        width_fraction = _get_value('width_fraction', 0.01)
        location = _get_value('location', 'upper right')
        if isinstance(location, six.string_types):
            location = self._LOCATIONS[location]
        pad = _get_value('pad', 0.2)
        border_pad = _get_value('border_pad', 0.1)
        sep = _get_value('sep', 5)
        frameon = _get_value('frameon', True)
        color = _get_value('color', 'k')
        box_color = _get_value('box_color', 'w')
        box_alpha = _get_value('box_alpha', 1.0)
        font_properties = self.font_properties
        ticklocation = _get_value('ticklocation', 'auto')
        if ticklocation == 'auto':
            ticklocation = 'bottom' if orientation == 'horizontal' else 'right'

        mappable = self.mappable
        cmap = self.mappable.get_cmap()
        norm = self.mappable.norm
        label = self.label
        ticks = self.ticks
        ticklabels = self.ticklabels

        ax = self.axes

        # Calculate
        calculator = ColorbarCalculator(mappable, ticks=ticks, ticklabels=ticklabels)

        X, Y, C = calculator.calculate_colorbar()
        X *= width_fraction
        Y *= length_fraction
        widths = np.diff(X, axis=1)[:, 0]
        heights = np.diff(Y[:, 0])
        if orientation == 'horizontal':
            X, Y = Y, X
            widths, heights = heights, widths

        ticks, ticklabels, offset_string = calculator.calculate_ticks()
        ticks *= length_fraction

        # Create colorbar
        colorbarbox = AuxTransformBox(ax.transAxes)

        patches = []
        for x0, y0, width, height in zip(X[:-1, 0], Y[:-1, 0], widths, heights):
            patch = Rectangle((x0, y0), width, height)
            patches.append(patch)

        edgecolors = 'none' #if self.drawedges else 'none'
        #FIXME: drawedge property
        #FIXME: Filled property
        col = PatchCollection(patches, cmap=cmap, edgecolors=edgecolors, norm=norm)
        col.set_array(C[:, 0])
        colorbarbox.add_artist(col)

        # Create outline
        if orientation == 'horizontal':
            outline = Rectangle((0, 0), length_fraction, width_fraction,
                                fill=False, ec=color)
        else:
            outline = Rectangle((0, 0), width_fraction, length_fraction,
                                fill=False, ec=color)
        colorbarbox.add_artist(outline)

        # Create ticks and tick labels
        w10th = width_fraction / 10.0
        ticklines = []
        ticktexts = []
        for tick, ticklabel in zip(ticks, ticklabels):
            if ticklocation == 'bottom':
                x0 = x1 = xtext = tick
                y0 = w10th
                y1 = -w10th
                ytext = -2 * w10th
                ha = 'center'
                va = 'top'
            elif ticklocation == 'top':
                x0 = x1 = xtext = tick
                y0 = width_fraction - w10th
                y1 = width_fraction + w10th
                ytext = width_fraction + 2 * w10th
                ha = 'center'
                va = 'bottom'
            elif ticklocation == 'left':
                x0 = w10th
                x1 = -w10th
                xtext = -2 * w10th
                y0 = y1 = ytext = tick
                ha = 'right'
                va = 'center'
            elif ticklocation == 'right':
                x0 = width_fraction - w10th
                x1 = width_fraction + w10th
                xtext = width_fraction + 2 * w10th
                y0 = y1 = ytext = tick
                ha = 'left'
                va = 'center'

            ticklines.append([(x0, y0), (x1, y1)])

            ticklabel = offset_string + ticklabel
            ticktext = Text(xtext, ytext, ticklabel,
                            color=color,
                            fontproperties=font_properties,
                            horizontalalignment=ha,
                            verticalalignment=va)
            ticktexts.append(ticktext)

        col = LineCollection(ticklines, color=color)
        colorbarbox.add_artist(col)

        for ticktext in ticktexts:
            colorbarbox.add_artist(ticktext)

        # Create label
        if label:
            labelbox = AuxTransformBox(ax.transAxes)

            va = 'baseline' if orientation == 'horizontal' else 'center'
            text = Text(0, 0, label,
                        fontproperties=font_properties,
                        verticalalignment=va,
                        rotation=orientation,
                        color=color)
            labelbox.add_artist(text)
        else:
            labelbox = None

        # Create final offset box
        if ticklocation == 'bottom':
            children = [colorbarbox, labelbox] if labelbox else [colorbarbox]
            child = VPacker(children=children, align='center', pad=0, sep=sep)
        elif ticklocation == 'top':
            children = [labelbox, colorbarbox] if labelbox else [colorbarbox]
            child = VPacker(children=children, align='center', pad=0, sep=sep)
        elif ticklocation == 'left':
            children = [labelbox, colorbarbox] if labelbox else [colorbarbox]
            child = HPacker(children=children, align='center', pad=0, sep=sep)
        elif ticklocation == 'right':
            children = [colorbarbox, labelbox] if labelbox else [colorbarbox]
            child = HPacker(children=children, align='center', pad=0, sep=sep)
#
        box = AnchoredOffsetbox(loc=location,
                                pad=pad,
                                borderpad=border_pad,
                                child=child,
                                frameon=frameon)

        box.axes = ax
        box.set_figure(self.get_figure())
        box.patch.set_color(box_color)
        box.patch.set_alpha(box_alpha)
        box.draw(renderer)

    def get_mappable(self):
        return self._mappable

    def set_mappable(self, mappable):
        self._mappable = mappable

    mappable = property(get_mappable, set_mappable)

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label

    label = property(get_label, set_label)

    def get_orientation(self):
        return self._orientation

    def set_orientation(self, orientation):
        if orientation is not None and \
                orientation not in ['vertical', 'horizontal']:
            raise ValueError('Unknown orientation: %s' % orientation)
        self._check_ticklocation(orientation=orientation)
        self._orientation = orientation

    orientation = property(get_orientation, set_orientation)

    def get_length_fraction(self):
        return self._length_fraction

    def set_length_fraction(self, fraction):
        if fraction is not None:
            fraction = float(fraction)
            if fraction <= 0.0 or fraction > 1.0:
                raise ValueError('Length fraction must be between ]0.0, 1.0]')
        self._length_fraction = fraction

    length_fraction = property(get_length_fraction, set_length_fraction)

    def get_width_fraction(self):
        return self._width_fraction

    def set_width_fraction(self, fraction):
        if fraction is not None:
            fraction = float(fraction)
            if fraction <= 0.0 or fraction > 1.0:
                raise ValueError('Width fraction must be between ]0.0, 1.0]')
        self._width_fraction = fraction

    width_fraction = property(get_width_fraction, set_width_fraction)

    def get_location(self):
        return self._location

    def set_location(self, loc):
        if isinstance(loc, six.string_types):
            if loc not in self._LOCATIONS:
                raise ValueError('Unknown location code: %s' % loc)
            loc = self._LOCATIONS[loc]
        self._location = loc

    location = property(get_location, set_location)

    def get_pad(self):
        return self._pad

    def set_pad(self, pad):
        self._pad = pad

    pad = property(get_pad, set_pad)

    def get_border_pad(self):
        return self._border_pad

    def set_border_pad(self, pad):
        self._border_pad = pad

    border_pad = property(get_border_pad, set_border_pad)

    def get_sep(self):
        return self._sep

    def set_sep(self, sep):
        self._sep = sep

    sep = property(get_sep, set_sep)

    def get_frameon(self):
        return self._frameon

    def set_frameon(self, on):
        self._frameon = on

    frameon = property(get_frameon, set_frameon)

    def get_color(self):
        return self._color

    def set_color(self, color):
        self._color = color

    color = property(get_color, set_color)

    def get_box_color(self):
        return self._box_color

    def set_box_color(self, color):
        self._box_color = color

    box_color = property(get_box_color, set_box_color)

    def get_box_alpha(self):
        return self._box_alpha

    def set_box_alpha(self, alpha):
        if alpha is not None:
            alpha = float(alpha)
            if alpha < 0.0 or alpha > 1.0:
                raise ValueError('Alpha must be between [0.0, 1.0]')
        self._box_alpha = alpha

    box_alpha = property(get_box_alpha, set_box_alpha)

    def get_font_properties(self):
        return self._font_properties

    def set_font_properties(self, props):
        self._font_properties = props

    font_properties = property(get_font_properties, set_font_properties)

    def get_ticks(self):
        return self._ticks

    def set_ticks(self, ticks):
        self._ticks = ticks

    ticks = property(get_ticks, set_ticks)

    def get_ticklabels(self):
        return self._ticklabels

    def set_ticklabels(self, ticklabels):
        if ticklabels is not None:
            if self.ticks and len(self.ticks) != len(ticklabels):
                raise ValueError("Ticklabels must be the same length as "
                                 "ticks")
        self._ticklabels = ticklabels

    ticklabels = property(get_ticklabels, set_ticklabels)

    def _check_ticklocation(self, loc=None, orientation=None):
        if loc is None:
            loc = getattr(self, 'ticklocation', None) # late definition
        if orientation is None:
            orientation = getattr(self, 'orientation', None) # late definition

        if loc is None or loc == 'auto':
            return
        if orientation == 'vertical' and loc not in ['left', 'right']:
            raise ValueError('Location must be either "left" or "right"'
                             'for vertical orientation')
        if orientation == 'horizontal' and loc not in ['top', 'bottom']:
            raise ValueError('Location must be either "top" or "bottom"'
                             'for horizontal orientation')

    def get_ticklocation(self):
        return self._ticklocation

    def set_ticklocation(self, loc):
        self._check_ticklocation(loc=loc)
        self._ticklocation = loc

    ticklocation = property(get_ticklocation, set_ticklocation)

def ColorBar(*args, **kwargs): # pragma: no cover
    warnings.warn("Class is deprecated. Use Colorbar(...) instead", DeprecationWarning)
    return Colorbar(*args, **kwargs)

