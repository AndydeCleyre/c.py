from setuptools import setup
import c


setup(
    name='c.py',
    version=c.__version__,
    description='A [c]at replacement with automatic syntax highlighting',
    author='Stefan Tatschner',
    author_email='rumpelsepp@sevenbyte.org',
    url='https://github.com/rumpelsepp/c.py',
    license='MIT',
    py_modules=['c'],
    install_requires=['click','docopt', 'pygments'],
    entry_points={
        'console_scripts': [
            'c = c:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
)
