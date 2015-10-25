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
            raise ValueError("The dimensions of a planet must be both integers, not %s and %s." % (type(self._width), type(self._height)))

        if self._width < 0 or self._height < 0:
            raise ValueError("The dimensions of a planet must be both positive integers.")

        # increase _height and _width so that a planet with dimension 5,5 has _height, _width both equal to 5
        self._height += 1
        self._width += 1
        

    def __str__(self):
        '''
        Returns a user-friendly description of the planet.
        '''
        return "Planet %s has dimensions %s and %s." % (self._name, self._width, self._height)


    def update_plateau(self, object_id, object_new_x, object_new_y):
        '''
        Validates and updates the new position of an object currently moving on the planet.
        '''
        if not isinstance(object_new_x, int) or not isinstance(object_new_y, int):
            raise ValueError("The new position of an object must be represented by two integers, not %s and %s." % (object_new_x, object_new_y))

        # Out of bounds position
        if object_new_x >= self._width or object_new_y >= self._height or object_new_x < 0 or object_new_y < 0:

            # The object moved out of the plateau
            if object_id in self._plateau.keys():
                del self._plateau[object_id]
                message = "%s was lost on %s moving towards %s, %s!" % (object_id, self._name, object_new_x, object_new_y)

            # The object was lost during the landing
            elif object_id not in self._plateau.keys():
                message = "%s never made it to %s!" % (object_id, self._name)

            else:
                raise Exception("This should never happen.")

            raise OutOfBounds("%s" % (message))

        # Valid position
        elif object_new_x < self._width and object_new_y < self._height:
            self._plateau[object_id] = (object_new_x, object_new_y)



class OutOfBounds(Exception):
    '''
    This class represents a position out of the plateau's boundaries.
    '''
    pass