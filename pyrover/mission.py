# -*- coding: utf-8 -*-

'''
This module represent a NASA mission.
'''

from pdb import set_trace
from pprint import pprint

from pyrover.mars import Mars, OutOfBounds
from pyrover.rover import Rover


class Mission(object):
    '''
    This class represent a Mission and its properties.
    '''
    def __init__(self, _mission_blueprints_input = None, destination = 'MARS'):
        '''
        Initializes a Mission object.
        '''
        # mission_setup is the file
        self._available_destinations = {'MARS' : Mars}
        self._destination = destination
        self._mission_blueprints_input = _mission_blueprints_input
        self._mission_blueprints = None
        self._rovers = []

        if self._mission_blueprints_input is None:
            raise ValueError("A Mission requires _mission_blueprints_input to be given!")
        if self._destination not in self._available_destinations:
            raise ValueError("%s is not a valid destination! Valid destinations are %s." % (destination, ', '.join(self._available_destinations.keys())))
    

    def _get_input(self):
        '''
        Auxiliary method responsible of reading and parsing the input file containing the details
        of the mission.
        '''
        try:
            with open(self._mission_blueprints_input, "r") as f:
                self._mission_blueprints = f.read().splitlines()
        except (FileNotFoundError, IOError) as e:
            raise MissionFailed("The mission's blueprints, %s, were not found! Aborting mission!" % (self._mission_blueprints_input))


    def setup(self):
        '''
        Sets up a NADA mission. The methods takes care of reading and validatin the mission's
        input and convert it into a Mission. The method does read the input file containing the
        mission's blueprints. It then parses this information, which is expected to contain from 1
        to N lines, with N odd. The first lines provides details about the destination target,
        while each following couple of lines represents a rover's landing position and
        instructions, with the latter being, again, optional.

        If the blueprints are valid, mission's resources are created.
        '''
        self._get_input()

        if len(self._mission_blueprints) % 2 == 0:
            raise MissionFailed('The input file containing the mission\'s blueprints must contain an odd number of lines.')

        # setup the destination planet
        planet_w, planet_h = self._mission_blueprints[0].split()
        self._destination = self._available_destinations[self._destination](int(planet_w), int(planet_h))

        # setup rovers, if any
        for rover_lz, rover_cmds in zip(self._mission_blueprints[1::2], self._mission_blueprints[2::2]):

            # prepare the landing co-ordinates
            x, y, facing = rover_lz.split()
            landing_coords = {'x' : int(x), 'y' : int(y), 'facing' : facing}
            
            new_rover = Rover(landing_coords, self._destination, rover_cmds)
            self._rovers.append(new_rover)


    def start(self):
        '''
        Starts the mission itself. Each rover is sent over to destination and told to execute the
        instructions it was assigned.
        '''
        for rover in self._rovers:
            rover.send()
            rover.execute_instructions()

    @property
    def outcome(self):
        '''
        Returns the outcome of a mission, that is the final position of the rovers sent to the
        destination target.
        '''
        response = ''
        for rover in self._rovers:
            if rover._status is 'ALIVE':
                rover_x = rover._current_position['x']
                rover_y = rover._current_position['y']
                rover_facing = rover._current_position['facing']
                response += "%s %s %s\n" % (rover_x, rover_y, rover_facing)
            elif rover._status is 'LOST':
                pass
        return response


class MissionFailed(Exception):
    '''
    This class represents a Mission that entered a critical error and is aborted.
    '''
    pass 