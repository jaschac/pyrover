# -*- coding: utf-8 -*-

'''
This module tests the correct behaviour of Rover.
'''

from copy import deepcopy
from unittest import main, TestCase

from pyrover.mars import InvalidPosition, Mars, OutOfBounds
from pyrover.rover import Rover


class TestRover(TestCase):
    '''
    Instantiates a TestRover object.
    '''
    def setUp(self):
        '''
        Initializes whatever is common to all tests.
        '''
        self.valid_cardinal_point = ['E', 'N', 'S', 'W']
        self.valid_instructions = 'MMMMLLRRMRLRMRLRMRLM'
        self.valid_landing_coords = {'x' : 10, 'y' : 20, 'facing' : 'S'}
        self.valid_movements = ['M']
        self.valid_rotations = ['L', 'R']
        self.valid_statuses = ['ALIVE', 'LOST']

    def tearDown(self):
        '''
        Instructions to execute at the end of each test method.
        '''
        pass

    def aux_generate_handle_mars(self, x = None, y = None):
        '''
        Auxiliary method that properly creates a Mars instance and returns it.
        '''
        if x is None:
            x = self.valid_landing_coords['x'] + 1
        if y is None:
            y = self.valid_landing_coords['y'] + 1
        handle_mars = Mars(x, y)
        return handle_mars

    def aux_generate_handle_rover(self, landing_coords = None, handle_mars = None, instructions = None):
        '''
        Auxiliary method that properly creates a Rover instance and returns it.
        '''
        if landing_coords is None:
            landing_coords = self.valid_landing_coords
        if handle_mars is None:
            handle_mars = self.aux_generate_handle_mars()
        if instructions is None:
            instructions = self.valid_instructions
        handle_rover = Rover(landing_coords, handle_mars, instructions)
        return handle_rover

    def test_init_correct(self):
        '''
        Tests that an instance of Rover is correctly created if all the mandatory parameters are
        properly passed and, if no instructions are given, the rover will have none.
        '''
        for facing_direction in self.valid_cardinal_point:
            landing_coords = {'x' : 1, 'y' : 2, 'facing' : facing_direction}
            handle_mars = self.aux_generate_handle_mars()
            handle_rover = Rover(landing_coords, handle_mars)
            self.assertIsInstance(handle_rover, Rover)
            self.assertEqual(handle_rover._landing_coords['x'], landing_coords['x'])
            self.assertEqual(handle_rover._landing_coords['y'], landing_coords['y'])
            self.assertEqual(handle_rover._landing_coords['facing'], landing_coords['facing'])
            self.assertEqual(handle_rover._current_position, None)
            self.assertEqual(handle_rover._last_known_position, None)
            self.assertEqual(handle_rover._instructions, '')
            self.assertEqual(handle_rover._status, 'ALIVE')
            del handle_rover

    def test_init_correct_instructions_given(self):
        '''
        Tests that an instance of Rover is correctly created if all the mandatory parameters are
        properly passed and if instructions are given, they will added to the rover.
        '''
        for facing_direction in self.valid_cardinal_point:
            landing_coords = {'x' : 1, 'y' : 2, 'facing' : facing_direction}
            handle_mars = self.aux_generate_handle_mars()
            handle_rover = Rover(landing_coords, handle_mars, self.valid_instructions)
            self.assertIsInstance(handle_rover, Rover)
            self.assertEqual(handle_rover._landing_coords['x'], landing_coords['x'])
            self.assertEqual(handle_rover._landing_coords['y'], landing_coords['y'])
            self.assertEqual(handle_rover._landing_coords['facing'], landing_coords['facing'])
            self.assertEqual(handle_rover._current_position, None)
            self.assertEqual(handle_rover._last_known_position, None)
            self.assertEqual(handle_rover._instructions, self.valid_instructions)
            self.assertEqual(handle_rover._status, 'ALIVE')
            del handle_rover

    def test_init_wrong_missing_mandatory_args(self):
        '''
        Tests that a TypeError exception is raised if any or all of the mandatory parameters
        required by Rover are not given when instantiating an object.
        '''
        for missing_args in ([], [self.valid_landing_coords],):
            self.assertRaises(
                                TypeError,
                                Rover,
                                *missing_args
                                )

    def test_init_wrong_mistyped_landing_coords(self):
        '''
        Tests that a TypeError exception is raised if the landing co-ordinates are passed to Rover,
        but not as a dictionary.
        '''
        handle_mars = self.aux_generate_handle_mars()
        self.assertRaises(
                            TypeError,
                            Rover,
                            *['not_really_a_dictionary', handle_mars]
                            )
        del handle_mars

    def test_init_wrong_mistyped_destination(self):
        '''
        Tests that a TypeError exception is raised if the destination is passed to Rover,
        but not as an instance of Mars.
        '''
        self.assertRaises(
                            TypeError,
                            Rover,
                            *[self.valid_landing_coords, 'not_really_an_instance_of_Mars']
                            )

    def test_init_wrong_missing_mandatory_landing_coords(self):
        '''
        Tests that a ValueError exception is raised if the landing co-ordinates are passed to Rover
        as a dictionary, but any of the mandatory keys are missing.
        '''
        handle_mars = self.aux_generate_handle_mars()
        for param in self.valid_landing_coords.keys():
            landing_coords = deepcopy(self.valid_landing_coords)
            del landing_coords[param]
            self.assertRaises(
                                ValueError,
                                Rover,
                                *[landing_coords, handle_mars]
                                )
        del handle_mars

    def test_init_wrong_landing_coords_illegal_facing(self):
        '''
        Tests that a ValueError exception is raised if the landing co-ordinates are passed to Rover
        as a dictionary, but the rover is told to face an illegal cardinal point.
        '''
        handle_mars = self.aux_generate_handle_mars()
        for illegal_cardinal_point in ['A', None, (1,2,3), {}]:
            self.assertRaises(
                                ValueError,
                                Rover,
                                *[{'x' : 10, 'y' : 20, 'facing' : illegal_cardinal_point}, handle_mars]
                                )
        del handle_mars

    def test_init_wrong_mistyped_instructions(self):
        '''
        Tests that a TypeError exception is raised if instructions are passed to Rover but not as
        a string.
        '''
        handle_mars = self.aux_generate_handle_mars()
        for illegal_instructions in [None, {}, 12143, ['MMMMM']]:
            self.assertRaises(
                                TypeError,
                                Rover,
                                *[self.valid_landing_coords, handle_mars, illegal_instructions]
                                )
        del handle_mars

    def test_init_wrong_illegal_instructions(self):
        '''
        Tests that a ValueError exception is raised if instructions are passed to Rover as a
        string, but they do contain illegal commands.
        '''
        handle_mars = self.aux_generate_handle_mars()
        illegal_instructions = 'LLLLT'
        self.assertRaises(
                            ValueError,
                            Rover,
                            *[self.valid_landing_coords, handle_mars, illegal_instructions]
                            )
        del handle_mars

    def test_str_correct_alive(self):
        '''
        Tests that a properly instantiated Rover object returns a response stating that the rover
        is alive, plus its current position.
        '''
        handle_rover = self.aux_generate_handle_rover()
        # simulate the rover moved
        handle_rover._current_position = {'x' : self.valid_landing_coords['x'], 'y' : self.valid_landing_coords['y'], 'facing' : self.valid_landing_coords['facing']}
        expected_response = "Rover %s is in position %s, %s, facing %s." % (handle_rover._id, self.valid_landing_coords['x'], self.valid_landing_coords['y'], self.valid_landing_coords['facing'])
        response = handle_rover.__str__()
        self.assertEqual(response, expected_response)
        del handle_rover

    def test_str_correct_lost_never_landed(self):
        '''
        Tests that a properly instantiated Rover object returns a response stating that the rover
        is was lost if the landing co-ordinates were out of the surface of its target destination.
        '''
        handle_rover = self.aux_generate_handle_rover()
        # simulate the rover never made it to the planet
        status = 'LOST'
        handle_rover._status = status
        expected_response = "Rover %s was lost. It never made it to the planet." % (handle_rover._id)
        response = handle_rover.__str__()
        self.assertEqual(response, expected_response)
        del handle_rover

    def test_str_correct_lost_out_of_bounds(self):
        '''
        Tests that a properly instantiated Rover object returns a response stating that the rover
        is lost if while moving, it went out of the surface of the target planet.
        '''
        handle_rover = self.aux_generate_handle_rover()
        # simulate the rover went out of bounds
        x, y, facing = 10, 20, 'S'
        status = 'LOST'
        handle_rover._last_known_position = {'x' : self.valid_landing_coords['x'], 'y' : self.valid_landing_coords['y'], 'facing' : self.valid_landing_coords['facing']}
        handle_rover._status = status
        expected_response = "Rover %s was lost. Its last known position was %s, %s, facing %s." % (handle_rover._id, self.valid_landing_coords['x'], self.valid_landing_coords['y'], self.valid_landing_coords['facing'])
        response = handle_rover.__str__()
        self.assertEqual(response, expected_response)
        del handle_rover

    def test_send_correct(self):
        '''
        Tests that a rover correctly lands on the target destination if the landing co-ordinates are valid.
        '''
        handle_rover = self.aux_generate_handle_rover()
        handle_rover.send()
        self.assertEqual(handle_rover._status, 'ALIVE')
        self.assertEqual(handle_rover._current_position, self.valid_landing_coords)
        self.assertEqual(handle_rover._last_known_position, self.valid_landing_coords)
        del handle_rover

    def test_send_wrong_invalid_landing_coordinates(self):
        '''
        Tests that a rover is lost if the landing co-ordinates are invalid.
        '''
        invalid_landing_coords = deepcopy(self.valid_landing_coords)
        invalid_landing_coords['x'] = -1
        handle_rover = self.aux_generate_handle_rover(invalid_landing_coords)
        handle_rover.send()
        self.assertEqual(handle_rover._status, 'LOST')
        del handle_rover

    def test_send_wrong_out_of_bounds(self):
        '''
        Tests that a rover is lost if the landing co-ordinates are valid but out of bounds.
        '''
        invalid_landing_coords = deepcopy(self.valid_landing_coords)
        invalid_landing_coords['x'] *= 2
        handle_rover = self.aux_generate_handle_rover(invalid_landing_coords)
        handle_rover.send()
        self.assertEqual(handle_rover._status, 'LOST')
        del handle_rover


if __name__ == '__main__':
        main()