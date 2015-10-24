# -*- coding: utf-8 -*-

'''
This module tests the correct behaviour of planet Mars.
'''

from unittest import main, TestCase

from pyrover.mars import InvalidPosition, Mars, OutOfBounds


class TestMars(TestCase):
    '''
    Instantiates a TestMars object.
    '''

    def aux_generate_handle_mars(self):
        '''
        Auxiliary method that properly creates a Mars instance and returns it.
        '''
        handle_mars = Mars(self.valid_width + 1, self.valid_height + 1)
        return handle_mars

    def setUp(self):
        '''
        Initializes whatever is common to all tests.
        '''
        self.valid_width = 10
        self.valid_height = 20

    def tearDown(self):
        '''
        Instructions to execute at the end of each test method.
        '''
        pass

    def test_init_correct(self):
        '''
        Tests that an instance of Mars is correctly created if all the mandatory parameters are
        properly passed. Edge cases, such as a dimension of 0 or -0 are also tested.
        '''
        for planet_width, planet_height in ((100, 10), (10, 0), (1, -0), (0, 10), (-0, 20), (0, 0), (-0, -0)):
            handle_mars = Mars(planet_width, planet_height)
            self.assertIsInstance(handle_mars, Mars)
            self.assertEqual(handle_mars._height, planet_height)
            self.assertEqual(handle_mars._width, planet_width)
            self.assertEqual(handle_mars._name, 'Mars')
            self.assertIsInstance(handle_mars._height, int)
            self.assertIsInstance(handle_mars._width, int)
            self.assertTrue(handle_mars._height >= 0)
            self.assertTrue(handle_mars._width >= 0)
            self.assertIsInstance(handle_mars._plateau, dict)
            del handle_mars
        

    def test_init_wrong_illegal_args(self):
        '''
        Tests that a ValueError exception is raised if the mandatory parameters required by Mars
        are given but their value is not valid.
        '''
        for planet_width, planet_height in ((100, -1), (0, -1), (-1, 0), (-10, 10), (-1, -2)):
            self.assertRaises(
                                ValueError,
                                Mars,
                                *[planet_width, planet_height]
                                )

    def test_init_wrong_missing_mandatory_args(self):
        '''
        Tests that a TypeError exception is raised if any or all of the mandatory parameters
        required by Mars are not given when instantiating an object.
        '''
        for missing_args in ([1], []):
            self.assertRaises(
                                TypeError,
                                Mars,
                                *missing_args
                                )
    
    def test_init_wrong_mistyped_mandatory_args(self):
        '''
        Tests that a ValueError exception is raised if any of the mandatory parameters required
        by Mars are not of the expected type.
        '''
        for mistyped_args in ([1, {"hello":123}], ['not_an_int', 1], [None, True]):
            self.assertRaises(
                                ValueError,
                                Mars,
                                *mistyped_args
                                )

    def test_str_correct(self):
        '''
        Tests that a properly instantiated Mars object returns name and dimension when printed.
        '''
        handle_mars = Mars(self.valid_width, self.valid_height)
        expected_response = "Planet Mars has dimensions %s and %s." % (self.valid_width, self.valid_height)
        response = handle_mars.__str__()
        self.assertEqual(response, expected_response)
        del handle_mars

    def test_update_plateau_correct_landing(self):
        '''
        Tests that update_plateau correctly sets the initial position of an object on the
        planet's surface if all the mandatory parameters are correctly given and the position is
        valid. It also tests that being the landing, the object is currently not present in the
        surface.
        '''
        landing_object = {
                            'id'        :   'rover_1234',
                            'position'  :   {
                                                'x' :   self.valid_width,
                                                'y' :   self.valid_height
                                                }
                            }
        handle_mars = self.aux_generate_handle_mars()
        self.assertTrue(landing_object['id'] not in handle_mars._plateau.keys())
        handle_mars.update_plateau(landing_object['id'], landing_object['position']['x'], landing_object['position']['y'])
        self.assertTrue(landing_object['id'] in handle_mars._plateau.keys())
        del handle_mars

    def test_update_plateau_correct_moving(self):
        '''
        Tests that update_plateau correctly updates the position of an object already present on
        the planet's surface if all the mandatory parameters are correctly given and the position
        is valid.
        '''
        moving_object = {
                            'id'            :   'rover_1234',
                            'new_position'  :   {
                                                    'x' : self.valid_width,
                                                    'y' : self.valid_height
                                                    },
                            'old_position'  :   {
                                                    'x' : self.valid_width - 1,
                                                    'y' : self.valid_height - 1
                                                    }
                            }
        handle_mars = self.aux_generate_handle_mars()
        handle_mars.update_plateau(moving_object['id'], moving_object['old_position']['x'], moving_object['old_position']['y'])
        handle_mars.update_plateau(moving_object['id'], moving_object['new_position']['x'], moving_object['new_position']['y'])
        self.assertTrue(moving_object['id'] in handle_mars._plateau.keys())
        self.assertEqual((moving_object['new_position']['x'],moving_object['new_position']['y']), handle_mars._plateau[moving_object['id']])
        del handle_mars

    def test_update_plateau_wrong_invalid_position(self):
        '''
        Tests that an InvalidPosition exception is raised if an object tries to move to an invalid
        position, that is a position whose any of the co-ordinates is a negative integer.
        '''
        for invalid_positions in ([1,-1], [-1,-1], [-1,1]):
            handle_mars = self.aux_generate_handle_mars()
            object_id = ['test_rover_1234']
            self.assertRaises(
                                InvalidPosition,
                                handle_mars.update_plateau,
                                *object_id + invalid_positions
                                )
            del handle_mars

    def test_update_plateau_wrong_missing_mandatory_args(self):
        '''
        Tests that a TypeError exception is raised if an object tries to a position without passing
        the method all the mandatory parameters.
        '''
        for mistyped_args in ([], ['test_rover'], ['test_rover', 4]):
            handle_mars = self.aux_generate_handle_mars()
            self.assertRaises(
                                TypeError,
                                handle_mars.update_plateau,
                                *mistyped_args
                                )
            del handle_mars

    def test_update_plateau_wrong_mistyped_mandatory_args(self):
        '''
        Tests that a ValueError exception is raised if an object tries to move to a position
        passing the required parameters of the wrong type.
        '''
        for mistyped_args in (['test_rover', 'not_an_int', 1], ['test_rover', 1, 'not_an_int'], ['test_rover', None, True]):
            handle_mars = self.aux_generate_handle_mars()
            self.assertRaises(
                                ValueError,
                                handle_mars.update_plateau,
                                *mistyped_args
                                )
            del handle_mars

    def test_update_plateau_wrong_out_of_bounds_land(self):
        '''
        Tests that an OutOfBounds exception is raised if an object tries to move to a valid
        position that anyway lies out of the boundaries of the surface of the planet.
        '''
        for out_of_bounds_positions in ([self.valid_width, self.valid_height+1], [self.valid_width+1, self.valid_height], [self.valid_width+1, self.valid_height+1]):
            handle_mars = self.aux_generate_handle_mars()
            object_id = ['test_rover_1234']
            self.assertRaises(
                                OutOfBounds,
                                handle_mars.update_plateau,
                                *object_id + out_of_bounds_positions
                                )
            del handle_mars

    def test_update_plateau_wrong_out_of_bounds_move(self):
        '''
        Tests that an OutOfBounds exception is raised if an object that has already landed onto the
        planet tries to move to a valid position that anyway lies out of the boundaries of the
        surface of the planet itself.
        '''
        for out_of_bounds_positions in ([self.valid_width, self.valid_height+1], [self.valid_width+1, self.valid_height], [self.valid_width+1, self.valid_height+1]):
            handle_mars = self.aux_generate_handle_mars()
            object_id = 'test_rover_1234'
            handle_mars.update_plateau(object_id, self.valid_width, self.valid_height)
            self.assertTrue(object_id in handle_mars._plateau.keys())
            self.assertRaises(
                                OutOfBounds,
                                handle_mars.update_plateau,
                                *[object_id] + out_of_bounds_positions
                                )
            del handle_mars

        
if __name__ == '__main__':
        main()