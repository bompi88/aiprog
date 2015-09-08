__author__ = 'krisvage'

import unittest

from algorithms.astar.checkers_example.checkers_state import CheckersState


class TestCheckersState(unittest.TestCase):
    def setUp(self):
        self.task = [
            [  7, 24, 10, 19,  3],
            [ 12, 20,  8, 22, 23],
            [  2, 15, 25, 18, 13],
            [ 11, 21,  5,  9, 16],
            [ 17,  4, 14,  1,  6]
        ]

        self.test_state = CheckersState(self.task)

    def test_id_set_correctly(self):
        correct_id = ''.join(map(str, [item for row in self.task for item in row]))

        self.assertEqual(correct_id, self.test_state.id)

    def test_heuristic_evaluation(self):
        correct_h = 43

        self.assertEqual(correct_h, self.test_state.heuristic_evaluation())

    def test_generate_all_successors(self):
        correct_length = 40
        generated = {}

        succs = self.test_state.generate_all_successors(generated)

        self.assertEqual(correct_length, len(succs))
        self.assertEqual(correct_length, len(generated))

    def test_is_solution(self):
        solution = [
            [ 1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25]
        ]

        state = CheckersState(solution)

        self.assertTrue(state.is_solution())
        self.assertFalse(self.test_state.is_solution())

    def test_manhattan_distance(self):
        a = (0, 0)
        b = (10, 10)
        res = 20
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (20, 0)
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (10, 0)
        res = 10
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (20, 20)
        res = 20
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

        a = (11, 10)
        res = 1
        self.assertEqual(CheckersState.manhattan_distance(a, b), res)

if __name__ == '__main__':
    unittest.main()