from distutils.core import setup

setup(
    name='pyrover',
    version='1.0.0',
    author='Jascha Casadio',
    author_email='jaschacasadio@gmail.com',
    packages=   [
                "pyrover",
                "pyrover.tests",
	      ],
    url='https://bitbucket.org/lostinmalloc/pyrover',
    license='LICENSE',
    description="A Python package to simulate NASA's expeditions.",
    long_description="A Python package to simulate NASA's expeditions",
    requires=[],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    	"Programming Language :: Python :: 3.4.3",
    ],
)