# -*- coding: utf-8 -*-

'''
This module represent the planet Mars, a possible destination of a NASA's mission.
'''

class Mars(object):
    '''
    This class represent planet Mars and its properties.
    '''

    def __init__(self, planet_width, planet_height):
        self._height = planet_height
        self._name = 'Mars'
        self._plateau = {}
        self._width = planet_width
        
        if not isinstance(self._width, int) or not isinstance(self._height, int):
            raise ValueError("The dimensions of a planet must be both integers, not %s and %s." % (self._width, self._height))

        if self._width < 0 or self._height < 0:
            raise ValueError("The dimensions of a planet must be both positive integers.")


    def __str__(self):
        '''
        Returns a user-friendly description of the planet.
        '''
        return "Planet %s has dimensions %s and %s." % (self._name, self._width, self._height)