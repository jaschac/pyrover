# pyrover

#### **Table of Contents**
1. [Overview](#overview)
    * [Development](#development)
2. [Problem Description](#problem-description)
    * [Input](#input)
    * [Output](#output)
3. [Package Description](#package-description)
    * [Modules](#modules)
4. [Setup](#setup)
5. [Usage](#usage)
    * [Unit Tests](#unit-tests)
6. [Planned Optimizations](#planned-optimziations)
    * [Mars](#mars)
    * [Mission](#mission)
    * [Rover](#rover)

## Overview
This package simulates the NASA sending rover(s) on expedition to exotic locations far away from us. It allows the client to define the target planet properties, as well as the number of rovers that will be sent over, including the instructions they must execute once landed. 

An expedition is made up of the following:

 - A **destination** which is an unknown location to explore. Mars is the only available option.
 - A **crew** which is the team that will be sent to the destination. Rovers are the only option.
 - A **mission** which represents the overall operation. It includes a target destination as well as the crew that will be sent over. Each member of the crew is given instructions to execute upon landing.

#### Development
The pyrover package has been developed with the following setup:

 - Debian
	 - Wheezy (3.2.68-1+deb7u5 x86_64)
	 - Jessie (3.16.7-ckt11-1+deb8u5 x86_64)
 - Python 3.4.3
	 - pip 7.1.2
	 - virtualenv 13.1.2

For pyrover's dependencies, check the Usage section.

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


##### Mission
This module represent a NASA mission. The mission has several protagonists:

 - The mission's blueprints, that is the instructions that allow the NASA to properly setup the mission itself. These blueprints, which come in the form a properly formatted input file, provide information about the target destination and the crew that is sent over there.
 - A crew, whose members are limited to rovers. Each rover is assigned a landing zone, represented by x,y co-ordinates and a facing direction, and a set of optional instructions that it will execute once it has safely landed onto the surface.
 - A destination, which is Mars.

All the information to setup a Mission are expected to be provided through an input file, as stated in the Problem.

 - The first line of the input file is a space-separated list of 2 values, representing the size of the destination planet.
 - The following lines are optional. They do represent details about each and every rover to be sent to Mars.
 	 - Each rover is represented by two lines.
 	 	 - The first line is a space-separated list of three values, representing, in order, the x and y landing coordinates and the cardinal point it will be facing upon arrival.
 	 	 - The second line, optional, is a string representing the instructions to execute once it has safely landed onto the surface.

A mission is made up of two phases:

 - The setup, which is responsible of getting through the mission's blueprints and generate the resources for the mission itself.
 - The start, which is responsible of sending the rovers to the target planet and instruct them to execute the commands they were assigned to.

The results achieved by the rovers represent the outcome of the Mission. 

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
In order to use pyrover:

 1. The pyrover package and its dependencies must be properly installed.
 2. A valid input file containing the mission's blueprints must be provided.

Here is a working example. The example assumes an input file called 'example.in' in the current working directory.
```python
>>> cd <PYROVER_ROOT>
>>> from pyrover.mission import Mission
>>> input_file = 'example.in'
>>> handle_mission = Mission(input_file)
>>> handle_mission.setup()
>>> handle_mission.start()
>>> mission_outcome = handle_mission.outcome
>>> print(mission_outcome)
1 3 N
5 1 E
```

#### Unit Tests
Each module comes with its set of unit tests. The whole suite of tests should be executed before merging and branch into the master.
```bash
# running the unit tests of the Mars module
$ python -m pyrover.tests.mars
----------------------------------------------------------------------
Ran 11 tests in 0.001s
OK

# running all of them
$ for module in rover mars mission; do python -m pyrover.tests.$module; done
----------------------------------------------------------------------
Ran 27 tests in 0.005s
OK
----------------------------------------------------------------------
Ran 11 tests in 0.001s
OK
----------------------------------------------------------------------
Ran 8 tests in 0.002s
OK
```

## Planned Optimizations
The pyrover package has just reached its first stable release, still there is much that can be done to get it better. What follow is a per module section with the optimizations that could be applied to make it better and more flexible to new features.

#### Mars

The following are optimizations that could be applied to the Mars module.

 - Define attributes as properties
	 - self._height
	 - self._name
	 - self._plateau
	 - self._width

 - Add a support structure to keep track of collisions. At the very moment, indeed, the module is keeping track of the IDs of the objects and their position. In order to find if an object collides with another, all the objects should be parsed. This is an O(N) operation that should be performed each time an object moves/reaches the end, depending if collisions are checked at each move or based on the final position only. In order to get an O(1) time, a second dictionary could be used. This would use the coordinates as a key and the objects that are currently in that position as values. This obviously requires more space and complexity, since each time an object moves, both structures should be updated. On the other hand, if new kind of objects are added, this could prove to be a good choice: if for example we add landmarks that a rover must discover, we would immediately find this out and be aware that object ID found it, without colliding with it (assuming a landmark is a non collision object).

 - Add a Crashed exception to support objects colliding with each others.

 - Refactor the test_str_correct test to use the auxiliary method to instantiate Mars objects.

 - Add a plateau property that pretty-print on the standard output the surface of the planet and the position of the object on it, if any.

 - Redefine the whole concept as that of destinations. The mission can have any kind of destination, not only planets. This would require a hierarchy of base (abstract) classes defining interfaces and properties common to their subclasses, but would open pyrover to more possibilities.
```bash
	├── destinations
	│   ├── base.py
	│   ├── __init__.py
	│   └── planets
	│       ├── base.py
	│       ├── __init__.py
	│       └── mars.py
	├── __init__.py
```

#### Mission

The following are optimizations that could be applied to the Mission module.

 - Add a blueprints property to pritty-print the mission's blueprints.

#### Rover

The following are optimizations that could be applied to the Rover module.

- Define attributes as properties

- The instructions could be handled through a generator.
	 - The rover could be able to self-assign itself instructions (randomly?) but still, never get the host running out of memory.

- Redefine the whole concept as that of crew. The mission could have a crew made of different protagonists, including, but not limited to human beings and robots, each with its properties (movement, ...). In this sense 
```bash
	crew
	├── base.py
	├── humans
	│   ├── base.py
	│   └── __init__.py
	├── __init__.py
	├── mechs
	│   ├── base.py
	│   ├── __init__.py
	│   └── rover.py
	└── rover
	    └── __init__.py
```