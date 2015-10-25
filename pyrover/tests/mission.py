# -*- coding: utf-8 -*-

'''
This module tests the correct behaviour of Mission.
'''

from copy import deepcopy
from os.path import abspath, split
from pdb import set_trace
from pprint import pprint
from unittest import main, TestCase

from pyrover.mars import Mars, OutOfBounds
from pyrover.mission import Mission, MissionFailed
from pyrover.rover import Rover


class TestMission(TestCase):
    '''
    Instantiates a TestMission object.
    '''
    def aux_get_blueprints(self, filename):
        '''
        Auxiliary methos that reads a mock input file with the mission's blueprints.
        '''
        with open(filename, "r") as f:
            content = f.read().splitlines() 
        return content

    def setUp(self):
        '''
        Initializes whatever is common to all tests.
        '''
        dirname, _ = split(abspath(__file__))
        self.mock_valid_mission_blueprints_file = "%s/files/mocks_mission_valid" % (dirname)
        self.mock_invalid_mission_blueprints_file = "%s/files/mocks_mission_invalid" % (dirname)
        self._mission_blueprints_input = self.aux_get_blueprints(self.mock_valid_mission_blueprints_file)
        self._mission_blueprints_input_invalid = self.aux_get_blueprints(self.mock_invalid_mission_blueprints_file)

    def tearDown(self):
        '''
        Instructions to execute at the end of each test method.
        '''
        pass

    def test_init_correct(self):
        '''
        Tests that a Mission is correctly istantiated if all the mandatory parameters are
        properly passed.
        '''
        handle_mission = Mission(self._mission_blueprints_input)
        self.assertIsInstance(handle_mission, Mission)
        self.assertEqual(handle_mission._destination, 'MARS')
        self.assertEqual(handle_mission._mission_blueprints_input, self._mission_blueprints_input)
        del handle_mission

    def test_init_wrong_missing_mandatory_args(self):
        '''
        Tests that a ValueError exception is raised if a Mission is created but the blueprints are
        not given.
        '''
        self.assertRaises(
                            ValueError,
                            Mission,
                            )

    def test_init_wrong_non_existant__mission_blueprints_input(self):
        '''
        Tests that a ValueError exception is raised if a Mission is created with a destination that
        is not available.
        '''
        invalid_destination = 'PLUTO'
        self.assertRaises(
                            ValueError,
                            Mission,
                            *[self._mission_blueprints_input, invalid_destination]
                            )

    def test__get_input_correct(self):
        '''
        Tests that the mission blueprints are correctly read if they are correctly given.
        '''
        handle_mission = Mission(self.mock_valid_mission_blueprints_file)
        handle_mission._get_input()
        self.assertEqual(handle_mission._mission_blueprints, self._mission_blueprints_input)
        del handle_mission

    def test__get_input_wrong_blueprints_not_found(self):
        '''
        Tests that a MissionFailed exception is raised if the mission's blueprints can't be found
        at the specified location.
        '''
        wrong_mission_blueprints_location = '/tmp/blueprints'
        handle_mission = Mission(wrong_mission_blueprints_location)
        self.assertRaises(
                            MissionFailed,
                            handle_mission._get_input,
                            )
        del handle_mission

    def test_setup_correct(self):
        '''
        Tests that given the correct blueprints, a Mission is properly setup. The desired number
        of rovers is created, with their landing co-ordinates and instructions. The destination
        planet is also properly setup with a surface of the correct size.
        '''
        handle_mission = Mission(self.mock_valid_mission_blueprints_file)
        handle_mission.setup()
        self.assertIsInstance(handle_mission._destination, Mars)
        self.assertTrue(len(handle_mission._rovers), 2)
        for rover in handle_mission._rovers:
            self.assertIsInstance(rover, Rover)
        del handle_mission

    def test_setup_wrong_invalid_blueprints(self):
        '''
        Tests that a MissionFailed exception is raised if, during the setup of the Mission, the
        mission's blueprints contain an even number of instructions.
        '''
        handle_mission = Mission(self.mock_invalid_mission_blueprints_file)
        self.assertRaises(
                            MissionFailed,
                            handle_mission.setup,
                            )
        del handle_mission

    def test_start_correct(self):
        '''
        Tests that a properly setup missing is correctly setup. In this case each and every rover
        is at the expected final position.
        '''
        handle_mission = Mission(self.mock_valid_mission_blueprints_file)
        handle_mission.setup()
        handle_mission.start()
        rover_1_expected_final_position = {'x' : 1, 'y' : 3, 'facing' : 'N'}
        rover_2_expected_final_position = {'x' : 5, 'y' : 1, 'facing' : 'E'}
        rovers_expected_positions = [rover_1_expected_final_position, rover_2_expected_final_position]

        for rover, rover_expected_position in zip(handle_mission._rovers, rovers_expected_positions):
            self.assertEqual(rover._current_position, rover_expected_position)

if __name__ == '__main__':
        main()