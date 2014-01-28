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
    if 'axis' in kwargs:
        axis = kwargs['axis']
    else:
        axis = pylab.gca()

    if 'symbols_colors' in kwargs:
        sc = kwargs['symbols_colors']
    else:
        sc = symbols_colors

    ac_map = dict((name, sc) for name, sc in zip(names, sc))
    axis._linesgodown_autocolor_map = ac_map

def plot(*args, **kwargs):
    '''Plot a line, or a bunch of lines, and make them pretty.'''

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

