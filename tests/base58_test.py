from unittest import TestCase

from pybtc.base58 import *


class Base58Test(TestCase):
    def test_encode(self):
        h1 = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d.to_bytes(32, 'big')
        encoded1 = '9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6'
        self.assertEqual(encode_base58(h1), encoded1)

        h2 = 0x00eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c.to_bytes(32, 'big')
        encoded2 = '14fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd'
        self.assertEqual(encode_base58(h2), encoded2)

        h3 = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6.to_bytes(32, 'big')
        encoded3 = 'EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7'
        self.assertEqual(encode_base58(h3), encoded3)
        self.assertFalse(encode_base58(h1) == encoded3)


