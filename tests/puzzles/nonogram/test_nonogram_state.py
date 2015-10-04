""" Testing NonogramState """
import unittest

from src.puzzles.nonogram.nonogram_state import NonogramState


class TestNonogramState(unittest.TestCase):
    """ Tests for checking that NonogramState sets domains correctly """
    def test_init_domain_one_block(self):
        """ Test that init domain generates correct domains """
        correct_domain = [
            '0000001111',
            '0000011110',
            '0000111100',
            '0001111000',
            '0011110000',
            '0111100000',
            '1111000000',
        ]

        domain = sorted(NonogramState.init_domain(10, [4]))

        self.assertEqual(len(correct_domain), len(domain))

        for i, element in enumerate(domain):
            self.assertEqual(element, correct_domain[i])

    def test_init_domain_two_blocks(self):
        """ Test that init domain generates correct domains """
        correct_domain = [
            '0000111101',
            '0001111001',
            '0001111010',
            '0011110001',
            '0011110010',
            '0011110100',
            '0111100001',
            '0111100010',
            '0111100100',
            '0111101000',
            '1111000001',
            '1111000010',
            '1111000100',
            '1111001000',
            '1111010000'
        ]

        domain = sorted(NonogramState.init_domain(10, [4, 1]))

        self.assertEqual(len(correct_domain), len(domain))

        for i, element in enumerate(domain):
            self.assertEqual(element, correct_domain[i])

    def test_init_domain_three_blocks(self):
        """ Test that init domain generates correct domains """
        correct_domain = [
            '0011101011',
            '0111001011',
            '0111010011',
            '0111010110',
            '1110001011',
            '1110010011',
            '1110010110',
            '1110100011',
            '1110100110',
            '1110101100'
        ]

        domain = sorted(NonogramState.init_domain(10, [3, 1, 2]))

        self.assertEqual(len(correct_domain), len(domain))

        for i, element in enumerate(domain):
            self.assertEqual(element, correct_domain[i])


if __name__ == '__main__':
    unittest.main()
