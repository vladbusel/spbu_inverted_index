import unittest
from app.encoder import *

class EncoderTests(unittest.TestCase):
    def test_unary(self):
        self.assertEqual(unary(b'1010101'), b'000000')

    def test_binary(self):
        self.assertEqual(binary(0), b'0')
        self.assertEqual(binary(1), b'1')
        self.assertEqual(binary(2), b'10')
        self.assertEqual(binary(3), b'11')

    def test_elias_gamma(self):
        self.assertEqual(elias_gamma(0), b'1')
        self.assertEqual(elias_gamma(1), b'010')
        self.assertEqual(elias_gamma(2), b'011')
        self.assertEqual(elias_gamma(3), b'00100')
        self.assertEqual(elias_gamma(4), b'00101')
        self.assertEqual(elias_gamma(5), b'00110')
        self.assertEqual(elias_gamma(6), b'00111')
        self.assertEqual(elias_gamma(7), b'0001000')
        self.assertEqual(elias_gamma(8), b'0001001')      

    def test_decoding_gamma_bytes(self):
        self.assertEqual(decoding_gamma_bytes(b'1'), 0)
        self.assertEqual(decoding_gamma_bytes(b'010'), 1)
        self.assertEqual(decoding_gamma_bytes(b'011'), 2)
        self.assertEqual(decoding_gamma_bytes(b'00100'), 3)
        self.assertEqual(decoding_gamma_bytes(b'00101'), 4)
        self.assertEqual(decoding_gamma_bytes(b'00110'), 5)
        self.assertEqual(decoding_gamma_bytes(b'00111'), 6)
        self.assertEqual(decoding_gamma_bytes(b'0001000'), 7)
        self.assertEqual(decoding_gamma_bytes(b'0001001'), 8)  

    def test_elias_delta(self):
        self.assertEqual(elias_delta(0), b'1')
        self.assertEqual(elias_delta(1), b'0100')
        self.assertEqual(elias_delta(2), b'0101')
        self.assertEqual(elias_delta(3), b'01100')
        self.assertEqual(elias_delta(4), b'01101')
        self.assertEqual(elias_delta(5), b'01110')
        self.assertEqual(elias_delta(6), b'01111')
        self.assertEqual(elias_delta(7), b'00100000')
        self.assertEqual(elias_delta(8), b'00100001')

    def test_decoding_delta_bytes(self):
        self.assertEqual(decoding_gamma_bytes(b'1'), 0)
        self.assertEqual(decoding_gamma_bytes(b'0100'), 1)
        self.assertEqual(decoding_gamma_bytes(b'0101'), 2)
        self.assertEqual(decoding_gamma_bytes(b'01100'), 3)
        self.assertEqual(decoding_gamma_bytes(b'01101'), 4)
        self.assertEqual(decoding_gamma_bytes(b'01110'), 5)
        self.assertEqual(decoding_gamma_bytes(b'01111'), 6)
        self.assertEqual(decoding_gamma_bytes(b'00100000'), 7)
        self.assertEqual(decoding_gamma_bytes(b'00100001'), 8)

    def test_list_compression(self):
        self.assertEqual(list_compression([111,112,114,117]), [111,1,2,3])