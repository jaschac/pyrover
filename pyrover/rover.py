# -*- coding: utf-8 -*-

'''
This module represent a Rover, a possible crew member of a NASA's expedition.
'''

from copy import deepcopy
from pdb import set_trace
from pprint import pprint
from uuid import uuid4

from pyrover.mars import Mars, OutOfBounds


class Rover(object):
    '''
    This class represent a Rover bot and its properties.
    '''
    def __init__(self, landing_coords, destination, instructions=''):
        '''
        This methods takes care of initializing a new Rover. A rover must be at least assigned the
        landing co-ordinates where it will try to touch the alien surface. The landing zone is a
        ternary representing the x and y co-ordinates and direction the rover will face. It is
        expected to be sent as a dictionary with the 'x', 'y' and 'facing' keys properly set.

        A target destination must also be given to the rover. It is expected to be an instance of
        the Mars class.

        A rover is supposed to execute instructions upon arrival, but this is not mandatory. For
        this reason, if a rover is not given any instruction, it will simply stay where it landed,
        if it safely did.
        '''
        self._current_position = None
        self._destination = destination
        self._id = "rover_%s" % uuid4()
        self._instructions = instructions
        self._landing_coords = landing_coords
        self._last_known_position = None
        self._status = 'ALIVE'
        self._valid_cardinal_point = ['N', 'E', 'S', 'W']
        self._valid_movements = ['M']
        self._valid_rotations = ['L', 'R']
        self._valid_statuses = ['ALIVE', 'LOST']

        if not isinstance(self._landing_coords, dict):
            raise TypeError("The landing_coords are expected as a dictionary, not %s." % (type(self._landing_coords)))
        if any([expected_key not in self._landing_coords.keys() for expected_key in ('x', 'y', 'facing')]):
            raise ValueError('The landing_coords are expected to have three values: x, y and facing.')
        if self._landing_coords['facing'] not in self._valid_cardinal_point:
            raise ValueError('The rover cannot face %s, but only: %s' % (self._landing_coords['facing'], ', '.join(self._valid_cardinal_point)))

        if not isinstance(self._destination, Mars):
            raise TypeError("The target destination must be Mars, not %s!" % (type(self._destination)))

        if not isinstance(self._instructions, str):
            raise TypeError("The instructions a rover must execute are expected as a string, not %s." % (type(self._instructions)))
        if any([i not in self._valid_movements + self._valid_rotations for i in self._instructions]):
            raise ValueError("The instructions a rover must execute can contain only the following values: %s" % ', '.join(self._valid_movements + self._valid_rotations))


    def __str__(self):
        '''
        Returns a user-friendly representation of a Rover.
        '''
        if self._status is 'ALIVE':
            message = "Rover %s is in position %s, %s, facing %s." % (self._id, self._current_position['x'], self._current_position['y'], self._current_position['facing'])
        elif self._status is 'LOST':
            if self._last_known_position is None:
                message = "Rover %s was lost. It never made it to the planet." % (self._id)
            elif isinstance(self._last_known_position, dict):
                message = "Rover %s was lost. Its last known position was %s, %s, facing %s." % (self._id, self._last_known_position['x'], self._last_known_position['y'], self._last_known_position['facing'])
        return message


    def send(self):
        '''
        This method is responsible of the landing of the rover on the target destination. It does
        take care of updating the rover's position and status, making sure to handle the case that
        it never makes it to the surface.
        '''
        try:
            self._destination.update_plateau(self._id, self._landing_coords['x'], self._landing_coords['y'])
            self._current_position = deepcopy(self._landing_coords)
            self._last_known_position = deepcopy(self._landing_coords)
        except OutOfBounds as e:
            self._status = 'LOST'


    def execute_instructions(self):
        '''
        Executes the instructions assigned, as long as the rover has safely landed and is alive.
        '''
        for instruction in self._instructions:
            if self._status is 'ALIVE':

                current_facing = self._current_position['facing']
                self._last_known_position['facing'] = current_facing

                if instruction is 'M':
                    new_position_x, new_position_y = self._calculate_new_position()
                    try:
                        self._destination.update_plateau(self._id, new_position_x, new_position_y)
                        self._last_known_position['x'], self._last_known_position['y'] = new_position_x, new_position_y
                        self._current_position['x'], self._current_position['y'] = new_position_x, new_position_y
                    except OutOfBounds as e:
                        self._status = 'LOST'
                        self._current_position = None

                elif instruction in ['L', 'R']:

                    if instruction is 'L':
                        try:
                            self._current_position['facing'] = self._valid_cardinal_point[self._valid_cardinal_point.index(current_facing) - 1]
                        except IndexError:
                            self._current_position['facing'] = self._valid_cardinal_point[-1]

                    elif instruction is 'R':
                        try:
                            self._current_position['facing'] = self._valid_cardinal_point[self._valid_cardinal_point.index(current_facing) + 1]
                        except IndexError:
                            self._current_position['facing'] = self._valid_cardinal_point[0]

                    self._last_known_position['facing'] = self._current_position['facing']
                    

    def _calculate_new_position(self, squares=1, x=None, y=None, facing=None):
        '''
        Calculates the x,y co-ordinates the rover will try to move to.
        '''
        if not isinstance(squares, int):
            raise TypeError("If passed, squares must be an integer, not %s." % (type(squares)))
        
        if facing is None:
            facing = self._current_position['facing']
        if x is None:
            x = self._current_position['x']
        if y is None:
            y = self._current_position['y']

        if facing is 'N':
            return x, y + squares
        elif facing is 'E':
            return x + squares, y
        elif facing is 'S':
            return x, y - squares
        elif facing is 'W':
            return x - squares, y
        else:
            raise Exception('This should never happen.')