# -*- coding: utf-8 -*-

'''
This module tests the correct behaviour of planet Mars.
'''

from unittest import main, TestCase

from pyrover.mars import Mars


class TestMars(TestCase):
    '''
    Instantiates a TestMars object.
    '''

    def setUp(self):
        '''
        Initializes whatever is common to all tests.
        '''
        pass

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
        for mistyped_args in ([1, {"hello":123}], ['not_an_int', 1], [None,True]):
            self.assertRaises(
                                ValueError,
                                Mars,
                                *mistyped_args
                                )

    def test_str_correct(self):
        '''
        Tests that a properly instantiated Mars object returns name and dimension when printed.
        '''
        planet_width, planet_height = 10, 20
        handle_mars = Mars(planet_width, planet_height)
        expected_response = "Planet Mars has dimensions %s and %s." % (planet_width, planet_height)
        response = handle_mars.__str__()
        self.assertEqual(response, expected_response)
        del handle_mars

        
if __name__ == '__main__':
        main()