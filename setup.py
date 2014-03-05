from distutils.core import setup

setup(
        name = 'linesgodown',
        version = '0.0.1',
        author = 'Madison McGaffin',
        author_email = 'greyhill@gmail.com',
        packages = [ 'linesgodown' ],
        scripts = [],
        url = 'http://github.com/greyhill/linesgodown',
        description = 'Sensible defaults and utilities for plotting',
        install_requires = [
            'matplotlib',
            ],
        )

