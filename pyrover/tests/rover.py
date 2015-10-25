# -*- coding: utf-8 -*-

'''
This module tests the correct behaviour of Rover.
'''

from copy import deepcopy
from pdb import set_trace
from pprint import pprint
from unittest import main, TestCase

from pyrover.mars import Mars, OutOfBounds
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

    def test_send_wrong_out_of_bounds(self):
        '''
        Tests that a rover is lost if the landing co-ordinates are valid but out of bounds.
        '''
        for invalid_x in (self.valid_landing_coords['x'] * 2, -1):
            invalid_landing_coords = deepcopy(self.valid_landing_coords)
            invalid_landing_coords['x'] = invalid_x
            handle_rover = self.aux_generate_handle_rover(invalid_landing_coords)
            handle_rover.send()
            self.assertEqual(handle_rover._status, 'LOST')
            del handle_rover

    def test_execute_instructions_correct_lost_at_landing_no_instruction_executed(self):
        '''
        Tests that a rover that is lost during landing does not execute any instruction at all.
        This can be proved by checking the initial status of the rover, which is 'LOST', as well as
        its current and last known positions, which are both null.
        '''
        mars_x, mars_y = 1, 1
        handle_mars = self.aux_generate_handle_mars(mars_x, mars_y)
        bad_landing_coords = {'x' : mars_x + 1, 'y' : mars_y + 1, 'facing' : 'N'}
        instructions = 'M'
        handle_rover = self.aux_generate_handle_rover(bad_landing_coords, handle_mars, instructions)
        expected_final_position = handle_rover._calculate_new_position(x=bad_landing_coords['x'], y=bad_landing_coords['y'],facing=bad_landing_coords['facing'])
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'LOST')
        self.assertEqual(handle_rover._current_position, None)
        self.assertEqual(handle_rover._last_known_position, None)
        self.assertTrue(handle_rover._current_position != expected_final_position)
        del handle_mars
        del handle_rover

    def test_execute_instructions_correct_no_instructions_given(self):
        '''
        Tests that a rover that has safely landed onto the planet ends up in the same position
        where it has landed if it has no instruction to execute.
        '''
        no_instructions = ''
        handle_rover = self.aux_generate_handle_rover(instructions=no_instructions)
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'ALIVE')
        self.assertEqual(handle_rover._landing_coords, handle_rover._last_known_position)
        self.assertEqual(handle_rover._current_position, handle_rover._last_known_position)
        del handle_rover

    def test_execute_instructions_correct_all_instructions_executed(self):
        '''
        Tests that a rover that has safely landed onto the planet executes all its instructions and
        ends up in the expected position, if it does not fall out of bounds.
        '''
        instructions = 'M'
        handle_rover = self.aux_generate_handle_rover(instructions=instructions)
        handle_rover.send()
        expected_final_position = handle_rover._calculate_new_position(x=self.valid_landing_coords['x'], y=self.valid_landing_coords['y'],facing=self.valid_landing_coords['facing'])
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'ALIVE')
        current_position_x, current_position_y = handle_rover._current_position['x'], handle_rover._current_position['y']
        self.assertEqual((current_position_x, current_position_y), expected_final_position)
        last_known_position_x, last_known_position_y = handle_rover._last_known_position['x'], handle_rover._last_known_position['y']
        self.assertEqual((last_known_position_x, last_known_position_y), expected_final_position)
        del handle_rover

    def test_execute_instructions_correct_360_degrees_clockwise_rotation(self):
        '''
        Tests that a rover that has safely landed onto the planet correctly ends up in the same
        position facing the same cardinal point if its executes a 360 degrees clockwise rotation.
        '''
        clockwise_rotation_instructions = 'RRRR'
        expected_final_position = self.valid_landing_coords
        handle_rover = self.aux_generate_handle_rover(instructions=clockwise_rotation_instructions)
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'ALIVE')
        self.assertEqual(handle_rover._current_position, expected_final_position)
        self.assertEqual(handle_rover._last_known_position, handle_rover._current_position)
        del handle_rover

    def test_execute_instructions_correct_360_degrees_counterclockwise_rotation(self):
        '''
        Tests that a rover that has safely landed onto the planet correctly ends up in the same
        position facing the same cardinal point if its executes a 360 degrees counterclockwise
        rotation.
        '''
        counterclockwise_rotation_instructions = 'LLLL'
        expected_final_position = self.valid_landing_coords
        handle_rover = self.aux_generate_handle_rover(instructions=counterclockwise_rotation_instructions)
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'ALIVE')
        self.assertEqual(handle_rover._current_position, expected_final_position)
        self.assertEqual(handle_rover._last_known_position, handle_rover._current_position)
        del handle_rover

    def test_execute_instructions_correct_movement(self):
        '''
        Tests that a rover that has safely landed onto the planet correctly ends up in the expected
        position by moving once in a specifc direction from the current landing position, assuming
        the new position is not out of bounds. 
        '''
        for facing in self.valid_cardinal_point:
            landing_coords = {'x' : 5, 'y' : 5, 'facing' : facing}
            instructions = 'M'
            handle_rover = self.aux_generate_handle_rover(landing_coords=landing_coords, instructions=instructions)
            expected_final_position = handle_rover._calculate_new_position(x=landing_coords['x'], y=landing_coords['y'],facing=landing_coords['facing'])
            handle_rover.send()
            handle_rover.execute_instructions()
            self.assertEqual(handle_rover._status, 'ALIVE')
            current_position_x, current_position_y = handle_rover._current_position['x'], handle_rover._current_position['y']
            self.assertEqual((current_position_x, current_position_y), expected_final_position)
            last_known_position_x, last_known_position_y = handle_rover._last_known_position['x'], handle_rover._last_known_position['y']
            self.assertEqual((last_known_position_x, last_known_position_y), expected_final_position)
            del handle_rover

    def test_execute_instructions_correct_movement_doesnt_affect_facing(self):
        '''
        Tests that any valid movement of a rover that has safely landed onto the planet does not
        affect the direction it is facing.

        check facing is the same
        '''
        instructions = 'M'
        handle_rover = self.aux_generate_handle_rover(instructions=instructions)
        expected_final_facing = self.valid_landing_coords['facing']
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._current_position['facing'], expected_final_facing)
        del handle_rover

    def test_execute_instructions_correct_rover_is_lost_if_goes_out_of_bounds(self):
        '''
        Tests that a rover that has safely landed onto the planet gets lost if it moves out of
        bounds.
        '''
        mars_x, mars_y = 1, 1
        handle_mars = self.aux_generate_handle_mars(mars_x, mars_y)
        landing_coords = {'x' : 0, 'y' : 0, 'facing' : 'N'}
        instructions = 'M'
        handle_rover = self.aux_generate_handle_rover(landing_coords, handle_mars, instructions)
        handle_rover.send()
        handle_rover.execute_instructions()
        self.assertEqual(handle_rover._status, 'LOST')
        self.assertEqual(handle_rover._current_position, None)
        self.assertEqual(handle_rover._last_known_position, landing_coords)
        del handle_mars
        del handle_rover

    def test_calculate_new_position_wrong_mistyped_squares(self):
        '''
        Tests that a TypeError exception is raised if _calculate_new_position is passed the
        optional parameter squares but not as an integer.
        '''
        handle_rover = self.aux_generate_handle_rover()
        for squares in [None, {}, 'not_an_int', [123]]:
            self.assertRaises(
                                TypeError,
                                handle_rover._calculate_new_position,
                                *[squares]
                                )
        del handle_rover

    def test_calculate_new_position_correct_movement_north(self):
        '''
        Tests that t_calculate_new_position correctly returns the new expected position when moving
        north. 
        '''
        landing_coords = {'x' : 2, 'y' : 2, 'facing' : 'N'}
        handle_rover = self.aux_generate_handle_rover(landing_coords)
        expected_response = (2, 3)
        response = handle_rover._calculate_new_position(x=landing_coords['x'], y=landing_coords['y'], facing=landing_coords['facing'])
        self.assertEqual(expected_response, response)
        del handle_rover

    def test_calculate_new_position_correct_movement_east(self):
        '''
        Tests that t_calculate_new_position correctly returns the new expected position when moving
        east. 
        '''
        landing_coords = {'x' : 2, 'y' : 2, 'facing' : 'E'}
        handle_rover = self.aux_generate_handle_rover(landing_coords)
        expected_response = (3, 2)
        response = handle_rover._calculate_new_position(x=landing_coords['x'], y=landing_coords['y'], facing=landing_coords['facing'])
        self.assertEqual(expected_response, response)
        del handle_rover

    def test_calculate_new_position_correct_movement_south(self):
        '''
        Tests that t_calculate_new_position correctly returns the new expected position when moving
        south. 
        '''
        landing_coords = {'x' : 2, 'y' : 2, 'facing' : 'S'}
        handle_rover = self.aux_generate_handle_rover(landing_coords)
        expected_response = (2, 1)
        response = handle_rover._calculate_new_position(x=landing_coords['x'], y=landing_coords['y'], facing=landing_coords['facing'])
        self.assertEqual(expected_response, response)
        del handle_rover

    def test_calculate_new_position_correct_movement_west(self):
        '''
        Tests that t_calculate_new_position correctly returns the new expected position when moving
        west. 
        '''
        landing_coords = {'x' : 2, 'y' : 2, 'facing' : 'W'}
        handle_rover = self.aux_generate_handle_rover(landing_coords)
        expected_response = (1, 2)
        response = handle_rover._calculate_new_position(x=landing_coords['x'], y=landing_coords['y'], facing=landing_coords['facing'])
        self.assertEqual(expected_response, response)
        del handle_rover


if __name__ == '__main__':
        main()