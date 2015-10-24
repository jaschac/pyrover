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

 - **Mars**
 @todo

 - **Mission**
 @todo
 - **Rover**
 @todo

#### Unit Tests
Each module comes with its set of unit tests.
@todo: give an example to run them.

## Setup
In order to use pyrover, the module itself, and its dependencies, must be installed first. This should be done in a virtual environment, since this would rule out different versions of Python and packages colliding.

The following installation steps assume Git, pip and Python3 already installed in the system.

 1. Clone the repository into a local folder:
 ```
 $ git clone git@bitbucket.org:lostinmalloc/pyrover.git pyrover
 ```
 2. Create and activate a virtual environment:
 ```
 $ PYROVER_HOME=$HOME/virtualenvs/pyrover
 $ PYTHON3_BIN=/usr/local/bin/python3
 $ virtualenv --python=$PYTHON3_BIN --system-site-packages $PYROVER_HOME
 $ source $PYROVER_HOME/bin/activate
 ```
 3. Install the dependencies
 ```
 $ cd pyrover
 $ pip install -r requirements.txt
 ```
 4. Install pyrover
 ```
 $ python setup.py sdist
 $ pip install dist/pyrover-<VERSION>.tar.gz
 ```

## Usage
@todo

## Reference
@todo