# `linesgodown.py`

This is library for making slightly nicer looking plots of lines going down.

The utility of this library will be immediately obvious to those working in 
optimization.

This library has experimental support for lines that go up, or behave in a 
nonmonotonic fashion.  The usage is the same.

## usage

There are currently two functions, `plot` and `autocolor`.  The functions
are reasonably well documented, here's an example use:

```
from matplotlib import figure
from linesgodown import autocolor, plot

...

autocolor('jobs', 'money', 'work')
plot(t, j, 'jobs')
plot(t, m, 'money')
figure()
autocolor('jobs', 'money', 'work')
plot(t2, m2, 'money')
plot(t2, j2, 'jobs')
plot(t2, w, 'work')
```

The "jobs" series will always appear in e.g., blue with circle markers, etc.,
and everything will probably looks better than it does with `matplotlib`'s 
default settings :-)

