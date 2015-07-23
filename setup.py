from setuptools import setup


setup(
    name='c.py',
    version='0.0.0',
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
