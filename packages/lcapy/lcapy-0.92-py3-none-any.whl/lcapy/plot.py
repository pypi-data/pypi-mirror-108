"""
This module performs plotting using matplotlib.

Copyright 2014--2021 Michael Hayes, UCECE
"""

import numpy as np

# Perhaps add Formatter classes that will produce the plot data?


def make_axes(figsize=None, axes=None, **kwargs):

    from matplotlib.pyplot import subplots
    
    if axes is not None:
        if isinstance(axes, tuple):
            # FIXME
            axes = axes[0]
        fig = axes.figure
    elif figsize is not None:
        fig, axes = subplots(1, figsize=figsize, **kwargs)
    else:
        fig, axes = subplots(1, **kwargs)

    return axes


def plot_pole_zero(obj, **kwargs):

    from matplotlib.pyplot import Circle, rcParams
    
    poles = obj.poles()
    zeros = obj.zeros()
    try:
        p = np.array([p.cval for p in poles.keys()])
        z = np.array([z.cval for z in zeros.keys()])
    except TypeError:
        raise TypeError('Cannot plot poles and zeros of symbolic expression')

    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None))

    unitcircle = kwargs.pop('unitcircle', False)    
    
    ax.axvline(0, color='0.7')
    ax.axhline(0, color='0.7')

    if unitcircle:
        ax.add_artist(Circle((0, 0), 1, color='blue', linestyle='--', fill=False))
    
    a = np.hstack((p, z))
    x_min = a.real.min()
    x_max = a.real.max()
    y_min = a.imag.min()
    y_max = a.imag.max()

    if unitcircle:
        if x_min > -1:
            x_min = -1
        if x_max < 1:
            x_max = 1
        if y_min > -1:
            y_min = -1
        if y_max < 1:
            y_max = 1                        
    
    x_extra, y_extra = 0.0, 0.0

    # This needs tweaking for better bounds.
    if len(a) >= 2:
        x_extra, y_extra = 0.1 * (x_max - x_min), 0.1 * (y_max - y_min)
    if x_extra == 0:
        x_extra += 1.0
    if y_extra == 0:
        y_extra += 1.0

    x_min -= 0.5 * x_extra
    x_max += 0.5 * x_extra
    if unitcircle:
        bbox = ax.get_window_extent()
        aspect = bbox.width / bbox.height
        
        x_min *= aspect
        x_max *= aspect       
        
    ax.axis('equal')
    ax.set_xlim(x_min, x_max)
    # overconstrained so ignored
    #ax.set_ylim(y_min - 0.5 * y_extra, y_max + 0.5 * y_extra)

    def annotate(axes, poles, offset=None):
        if offset is None:
            xmin, xmax = axes.get_xlim()
            offset = (xmax - xmin) / 40
        
        for pole, num in poles.items():
            if num > 1:
                p = pole.cval
                axes.text(p.real + offset, p.imag + offset, '%d' % num)

    # Marker size.  Unfortunately, the default is too small
    # but if the user wants a size of 6 set in rcParams, they are out of luck...
    if 'ms' not in kwargs and 'markersize' not in kwargs and rcParams['lines.markersize'] == 6:
        kwargs['ms'] = 19

    fillstyle = kwargs.pop('fillstyle', 'none')
    xlabel = kwargs.pop('xlabel', 'Re(%s)' % obj.var)
    ylabel = kwargs.pop('ylabel', 'Im(%s)' % obj.var)
    title = kwargs.pop('title', None)
    
    lines = ax.plot(z.real, z.imag, 'o', fillstyle=fillstyle, **kwargs)
    annotate(ax, zeros)
    color = kwargs.pop('color', lines[0].get_color())    
    ax.plot(p.real, p.imag, 'x', fillstyle=fillstyle, color=color, **kwargs)
    annotate(ax, poles)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:        
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)        

    ax.grid(True)
    
    return ax


def plot_frequency(obj, f, norm=False, **kwargs):

    npoints = kwargs.pop('npoints', 400)    
    log_magnitude = kwargs.get('log_magnitude', False)
    log_frequency = kwargs.get('log_frequency', False) or kwargs.pop('log_scale', False)
    if kwargs.pop('loglog', False):
        log_magnitude = True 
        log_frequency = True    

    # FIXME, determine useful frequency range...
    if f is None:
        if norm:
            f = (-0.5, 0.5)
        else:
            f = (0, 2)
    if isinstance(f, (int, float)):
        f = (0, f)
    if isinstance(f, tuple):
        if log_frequency:
            f = np.logspace(f[0], f[1], npoints)
        else:
            f = np.linspace(f[0], f[1], npoints)            

    # Objects can have a `part` attribute that is set by methods such
    # as real, imag, phase, magnitude.  If this is defined,
    # `plot_type` is ignored.
            
    if obj.is_complex and obj.part == '':

        plot_type = kwargs.pop('plot_type', 'dB-phase')

        obj2 = None        
        if plot_type in ('dB_phase', 'dB-phase'):
            obj1 = obj.magnitude.dB
            if obj.is_complex:
                obj2 = obj.phase
        elif plot_type in ('mag_phase', 'magnitude_phase', 'mag-phase',
                           'magnitude-phase'):
            obj1 = obj.magnitude
            if not obj.is_positive:
                obj2 = obj.phase
        elif plot_type in ('real_imag', 'real-imag'):
            obj1 = obj.real
            obj2 = obj.imag
        elif plot_type in ('mag', 'magnitude'):
            obj1 = obj.magnitude
        elif plot_type == 'phase':
            obj1 = obj.phase
        elif plot_type == 'real':
            obj1 = obj.real 
        elif plot_type == 'imag':
            obj1 = obj.imag
        elif plot_type == 'dB':
            obj1 = obj.magnitude.dB            
        else:
            raise ValueError('Unknown plot type: %s' % plot_type)

        if obj2 is None:
            return plot_frequency(obj1, f, **kwargs)
        
        ax = plot_frequency(obj1, f, **kwargs)
        ax2 = ax.twinx()
        kwargs['axes'] = ax2
        kwargs['linestyle'] = '--'
        ax2 = plot_frequency(obj2, f, second=True, **kwargs)
        return ax, ax2

    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None))

    V = obj.evaluate(f)

    kwargs.pop('log_frequency', None)
    kwargs.pop('log_magnitude', None)
    kwargs.pop('plot_type', None)        

    plots = {(True, True) : ax.loglog,
             (True, False) : ax.semilogy,
             (False, True) : ax.semilogx,
             (False, False) : ax.plot}

    if obj.is_magnitude or np.all(V > 0):
        plot = plots[(log_magnitude, log_frequency)]
    else:
        plot = plots[(False, log_frequency)]                    

    if norm:
        default_xlabel = 'Normalised frequency'
    else:
        default_xlabel = obj.domain_label_with_units
        
    xlabel = kwargs.pop('xlabel', default_xlabel)
    ylabel = kwargs.pop('ylabel', obj.label_with_units)                
    ylabel2 = kwargs.pop('ylabel2', obj.label_with_units)
    second = kwargs.pop('second', False)
    xscale = kwargs.pop('xscale', 1)
    yscale = kwargs.pop('yscale', 1)
    title = kwargs.pop('title', None)    

    plot(f * xscale, V * yscale, **kwargs)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    ylabel = ylabel2 if second else ylabel
    if ylabel is not None:        
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
        
    ax.grid(True)
    return ax


def plot_bode(obj, f, **kwargs):

    if 'log_frequency' not in kwargs:
        kwargs['log_frequency'] = True
    
    return plot_frequency(obj, f, **kwargs)


def plot_angular_frequency(obj, omega, norm=False, **kwargs):

    npoints = kwargs.pop('npoints', 400)        

    # FIXME, determine useful frequency range...
    if omega is None:
        if norm:
            omega = (-np.pi, np.pi)
        else:
            omega = (0, np.pi)
    if isinstance(omega, (int, float)):
        omega = (0, omega)
    if isinstance(omega, tuple):
        omega = np.linspace(omega[0], omega[1], npoints)

    if norm and 'xlabel' not in kwargs:
        kwargs['xlabel'] = 'Normalised angular frequency'
        
    return plot_frequency(obj, omega, **kwargs)


def plot_time(obj, t, **kwargs):

    npoints = kwargs.pop('npoints', 400)        
    
    # FIXME, determine useful time range...
    if t is None:
        t = (-0.2, 2)
    if isinstance(t, (int, float)):
        t = (0, t)
    if isinstance(t, tuple):
        t = np.linspace(t[0], t[1], npoints)

    v = obj.evaluate(t)

    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None))    

    xlabel = kwargs.pop('xlabel', obj.domain_label_with_units)
    ylabel = kwargs.pop('ylabel', obj.label_with_units)
    xscale = kwargs.pop('xscale', 1)
    yscale = kwargs.pop('yscale', 1)
    title = kwargs.pop('title', None)
    
    ax.plot(t * xscale, v * yscale, **kwargs)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:        
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
        
    ax.grid(True)
    return ax


# make a stem plot for complex values sequences in the complex domain
def plot_sequence_polar(obj, ni=(-10, 10), **kwargs):

    npoints = kwargs.pop('npoints', 400)        
    
    # FIXME, determine useful range...
    if ni is None:
        ni = (-20, 20)
    if isinstance(ni, tuple):
        # Use float data type since NumPy barfs for n**(-a) where a is
        # an integer.
        ni = np.arange(ni[0], ni[1] + 1, dtype=float)

    v = obj.evaluate(ni)
    
    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None),
                   subplot_kw=dict(polar=True))

    phi = np.angle(v)
    mag = abs(v)
    
    # Plot symbols
    lines = ax.plot(phi, mag, 'o', **kwargs)

    color = kwargs.pop('color', lines[0].get_color())
    
    # Plot lines from origin
    Nv = len(v)
    ax.plot((phi, phi), (np.zeros(Nv), mag), color=color, **kwargs)    
    ax.grid(True)
    return ax    


def plot_sequence(obj, ni, polar=False, **kwargs):

    from matplotlib.ticker import MaxNLocator

    if polar:
        return plot_sequence_polar(obj, ni, **kwargs)
    
    npoints = kwargs.pop('npoints', 400)        
    
    # FIXME, determine useful range...
    if ni is None:
        ni = (-20, 20)
    if isinstance(ni, tuple):
        # Use float data type since NumPy barfs for n**(-a) where a is
        # an integer.
        ni = np.arange(ni[0], ni[1] + 1, dtype=float)

    v = obj.evaluate(ni)

    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None))

    xlabel = kwargs.pop('xlabel', obj.domain_label_with_units)
    ylabel = kwargs.pop('ylabel', obj.label_with_units)
    xscale = kwargs.pop('xscale', 1)
    yscale = kwargs.pop('yscale', 1)
    title = kwargs.pop('title', None)

    ax.stem(ni * xscale, v * yscale, use_line_collection=True, **kwargs)
    # Ensure integer ticks.
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:        
        ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
        
    ax.grid(True)
    return ax


def plot_phasor(obj, **kwargs):

    ax = make_axes(figsize=kwargs.pop('figsize', None),
                   axes=kwargs.pop('axes', None),
                   subplot_kw=dict(polar=True))

    phi = obj.phase.fval
    mag = obj.magnitude.fval
    
    ax.plot((phi, phi), (0, mag), **kwargs)
    return ax
