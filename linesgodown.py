import matplotlib.pylab as pylab

symbols_colors = [ \
        ('o', 'blue'),
        ('^', 'green'),
        ('s', 'red'),
        ('p', 'purple'),
        ('D', 'orange'),
        ('d', 'cyan')
        ]

fake_names = [ \
        'Bobbins',
        'Frobnizzles',
        'Jazzrabbles',
        'Encabulations',
        'Turbibbles',
        'Flip-fumpets',
        'Codswallops',
        'Cherrywiddicks',
        'Conderhandles',
        'Pipfiths',
        'Chads',
        'Featherwicks' ]

def autocolor(*names, **kwargs):
    '''Associate names with colors for consistency across multiple plots.

    Calling autocolor(list_of_names) before calling any plot commands will
    ensure that a named series will always have the same color associated
    with it.

    Example usage:

    >>> autocolor('jobs', 'money', 'work')
    >>> plot(t, j, 'jobs')
    >>> plot(t, m, 'money')
    >>> figure()
    >>> autocolor('jobs', 'money', 'work')
    >>> plot(t2, m2, 'money')
    >>> plot(t2, j2, 'jobs')
    >>> plot(t2, w, 'work')

    The "jobs" series will always appear in e.g., blue with circle markers, etc.

    Instead of a string, you can give an `iterable` of strings, all of which will
    be associated with the name color/symbol pair.  e.g.,

    >>> autocolor('money', ('jobs', 'jerbs'))

    autocolor understands the following kwargs:
    - axis : matplotlib axis object to associate this list with
    - symbols_colors : an alternate list of symbols and colors to use for
        associating with names

    '''
    if 'axis' in kwargs:
        axis = kwargs['axis']
    else:
        axis = pylab.gca()

    if 'symbols_colors' in kwargs:
        sc = kwargs['symbols_colors']
    else:
        sc = symbols_colors

    ac_map = {}
    sc = sc[:]
    for name in names:
      if isinstance(name, str):
        ac_map[name] = sc.pop(0)
      else:
        multi_sc = sc.pop(0)
        for nname in name:
          ac_map[nname] = multi_sc
    axis._linesgodown_autocolor_map = ac_map

def plot(*args, **kwargs):
    '''Plot a line, or a bunch of lines, and make them pretty.

    Plot a series with [0, ..., N-1] as the horizontal axis, with a fake name:
    >>> plot(y)

    Plot series y (vertical) against x (horizontal), with a silly fake name:
    >>> plot(x, y)

    Plot series y (vertical) against x (horizontal), with a given name:
    >>> plot(x, y, name)

    Do the above with a bunch of series:
    >>> plot(x1, y1, name1, x2, y2, name2, ...)

    plot also understands the following kwargs:
    - axis : matplotlib axis to plot onto
    - symbol_color : a tuple (s, c) of a symbol and color to use,
        e.g., ('-o', 'blue').  linesgodown has sensible defaults.  See also 
        linesgodown.autocolor()
    - symbol_at : index of data at which to place the symbol.  Currently, 
        some hand-tweaking may be needed to produce readable plots.

    '''

    if len(args) == 0:
        # you gotta give me something to work with here!
        raise ValueError('no data given to plot!')
    if len(args) == 1:
        y = args[0]
        x = range(len(y))
        name = 'Series %d'
    elif len(args) == 2:
        x = args[0]
        y = args[1]
        import random
        name = random.choice(fake_names) # :-)
    elif len(args) == 3:
        x = args[0]
        y = args[1]
        name = args[2]
    elif len(args) % 3 == 0:
        for (x, y, name) in zip(*[iter(args)]*3):
            plot(x, y, name, **kwargs)
        return
    else: 
        raise ValueError('unknown usage')

    if 'axis' is kwargs:
        axis = kwargs['axis']
    else:
        axis = pylab.gca()

    if not hasattr(axis, '_linesgodown_symbol_colors_used'):
        axis._linesgodown_symbol_colors_used = []
    symbol_colors_used = axis._linesgodown_symbol_colors_used

    if 'symbol_color' in kwargs:
        symbol_color = kwargs['symbol_color']
        if symbol_color in symbol_colors_used:
            raise ValueError('Symbol/Color pair %s already used' % \
                    str(symbol_color))
    elif hasattr(axis, '_linesgodown_autocolor_map') \
            and name in axis._linesgodown_autocolor_map:
        symbol_color = axis._linesgodown_autocolor_map[name]
    else:
        unused = [ z for z in symbols_colors if z not in symbol_colors_used ]
        symbol_color = unused[0]

    symbol_colors_used.append(symbol_color) 
    symbol, color = symbol_color

    axis.plot(x, y, color=color, linewidth = 2)

    if 'sigil_at' in kwargs:
        sigil_at = kwargs['sigil_at']
    else:
        # todo: need a smarter way to determine where to put the sigils
        sigil_at = len(x) // 4
    axis.plot((x[sigil_at],), (y[sigil_at],), '-%s' % symbol, color=color, 
            linewidth = 2, label = name)

    axis._linesgodown_symbol_colors_used = symbol_colors_used

