# pyrover

#### **Table of Contents**
1. [Overview](#overview)
2. [Problem Description](#problem-description)
    * [Input](#input)
    * [Output](#output)
3. [Package Description](#package-description)
    * [Modules](#modules)
    * [Unit Tests](#unit-tests)
4. [Setup](#setup)
5. [Usage](#usage)
6. [Reference](#reference)

## Overview
This package simulates the NASA sending rover(s) on expedition to exotic locations far away from us. It allows the client to define the target planet properties, as well as the number of rovers that will be sent over, including the instructions they must execute once landed. 

An expedition is made up of the following:

 - A **destination** which is an unknown location to explore. Mars is the only available option.
 - A **crew** which is the team that will be sent to the destination. Rovers are the only option.
 - A **mission** which represents the overall operation. It includes a target destination as well as the crew that will be sent over. Each member of the crew is given instructions to execute upon landing.

## Problem Description
A squad of robotic rovers are to be landed by NASA on a plateau on Mars. This plateau, which is curiously rectangular, must be navigated by the rovers so that their on-board cameras can get a complete view of the surrounding terrain to send back to Earth.

A rover's position and location is represented by a combination of x and y co-ordinates and a letter representing one of the four cardinal compass points. The plateau is divided up into a grid to simplify navigation. An example position might be 0, 0, N, which means the rover is in the bottom left corner and facing North.

In order to control a rover, NASA sends a simple string of letters. The possible letters are ‘L', ‘R' and ‘M'. ‘L' and ‘R' makes the rover spin 90 degrees left or right respectively, without moving from its current spot. ‘M' means move forward one grid point, and maintain the same heading. Assume that the square directly North from (x, y) is (x, y+1).

#### **Input**
A file containing the dimensions of the plateau, the position and orientation of each rover and each rover's instructions. The first line of input is the upper-right coordinates of the plateau, the lower-left coordinates are assumed to be 0,0. The rest of the input is information pertaining to the rovers that have been deployed. Each rover has two lines of input. The first line gives the rover's position, and the second line is a series of instructions telling the rover how to explore the plateau. The position is made up of two integers and a letter separated by spaces, corresponding to the x and y co-ordinates and the rover's orientation. Each rover will be finished sequentially, which means that the second rover won't start to move until the first one has finished moving.

**Example Input**
```bash
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

#### **Output**
The output for each rover should be its final co-ordinates and heading.

**Expected Output**
```bash
1 3 N
5 1 E
```

## Package Description
The pyrover package contains all the modules required to simulate a NASA expedition. Each module comes with its own unit tests. The package has the following structure:
```bash
├── LICENSE
├── MANIFEST.in
├── pyrover
│   ├── __init__.py
│   ├── mars.py
│   ├── mission.py
│   ├── rover.py
│   └── tests
│       ├── __init__.py
│       ├── mars.py
│       ├── mission.py
│       └── rover.py
├── README
├── README.md
├── requirements.txt
└── setup.py
```

#### Modules
The pyrover package contains the following modules:

##### Mars
This module represents the surface over which the rover(s) will land and move. The planet has the following properties:

 - A name.
 - A two-dimensional size, represented by x and y.
 - An implicit rectangular shape, with the aforementioned size.
 - A surface, also referred to as plateau, which tracks the objects that are currently over it. Each object is tracked through a unique ID and its co-ordinates. 
```bash
	0,Y             X,Y
	+---+---+---+---+
	|   |   |   |   |
	+---------------+
	|   |   |   |   |
	+---------------+
	|   |   |   |   |
	+---+---+---+---+
	0,0              X,0
```

The module is responsible of:

 - Keeping track of the current position of the objects that are over it.
	 - If an object moves out of the surface of the planet (out of bounds), it is removed from the internal representation of the plateau.
 - Raising specific exceptions whenever an object demands to occupy an illegal position.
	 - Any position whose x or y co-ordinates are negative integers raises an Illegal Position exception.
	 - Any position whose x or y co-ordinates are out of the surface raises an Out of Bounds exception.

The module has no knowledge of the objects that are over it, and thus of their properties. As such, the module representing the object placed/moving over the planet is responsible of:

 - Calculating the (new) position co-ordinates.
 - Handling any exception raised by the planet when interacting with it.
 
##### Rover
This class represents the only crew member available to participate to a NASA's mission. It represent a robotic machine that is sent over to the target destination and that, if able to safely land at the desired co-ordinates, will execute instructions.

A rover has the following properties:

 - A unique ID, which is automatically generated when an object is instantiated.
 - A status, that tells if the rover is still alive or got lost.
	 - A rover can get lost in two different occasions:
		 - During landing, if the landing co-ordinates are not on the planet's surface. When this happens, the rover never makes it to the planet and as such:
			 - It does not execute any instruction.
			 - Both its current and last known positions are null.
		 - Once safely landed, when moving throughout the planet, if its instructions gets it out of the planet's surface. In this case:
			 - The current position of the rover is null.
			 - The last known position of the rover is available and can be used to investigate where it was last seen before losing contact.
 - A current position, which tells the NASA where the rover is currently at. It is a ternary made of the x and y co-ordinates, and the direction it is facing. It corresponds to the landing co-ordinates upon arrival to destination, before the instructions get executed.
 - A last known position, which, unless the rover is lost, equals the current position.
 - A set of instructions to execute. The rover also accepts being sent over to the target destination without any instruction to execute. When this happens both the current and last known positions correspond to the landing position, assuming it safely lands onto the surface.

In order to properly instantiate a rover, it must be provided with the following information:

 - A target destination.
 - A landing position.
 - Optionally, it can be provided wit ha set of instructions to execute upon arrival. No instruction is executed by default.

There are two operations that can be performed on a rover, once created:

 - The rover can be sent to the target destination. This operation is responsible of the landing of the rover onto the surface of the target planet. Since the landing co-ordinates could be wrong, the rover could get lost during this phase. When this happens, it won't be able to execute any instruction and its position is unknown.
 - The rover can be told to execute the instructions it was given when created. Starting from the landing zone, it will execute all of them, one by one, sequentially. At each step the rover can end up out of the planet surface. When this happens, the rover is lost. Its last known position is still available to the NASA. If the rover is instead able to fully complete its job, its final position is also known.

#### Unit Tests
Each module comes with its set of unit tests. The whole suite of tests should be executed before merging and branch into the master.
```bash
# running the unit tests of the Mars module
$ python -m pyrover.tests.mars
----------------------------------------------------------------------
Ran 11 tests in 0.001s
OK

# running all of them
$ for module in rover mars; do python -m pyrover.tests.$module; done
----------------------------------------------------------------------
Ran 27 tests in 0.006s
OK

----------------------------------------------------------------------
Ran 11 tests in 0.002s

OK
```

## Setup
In order to use pyrover, the module itself, and its dependencies, must be installed first. This should be done in a virtual environment, since this would rule out different versions of Python and packages colliding.

The following installation steps assume Git, pip and Python3 already installed in the system.

1) Clone the repository into a local folder:
```bash
$ git clone git@bitbucket.org:lostinmalloc/pyrover.git pyrover
```

2) Create and activate a virtual environment:
```bash
$ PYROVER_HOME=$HOME/virtualenvs/pyrover
$ PYTHON3_BIN=/usr/local/bin/python3
$ virtualenv --python=$PYTHON3_BIN --system-site-packages $PYROVER_HOME
$ source $PYROVER_HOME/bin/activate
```

3) Install the dependencies
```bash
$ cd pyrover
$ pip install -r requirements.txt
```

4) Install pyrover
```bash
$ python setup.py sdist
$ pip install dist/pyrover-<VERSION>.tar.gz
```

## Usage
@todo

## Reference
@todo