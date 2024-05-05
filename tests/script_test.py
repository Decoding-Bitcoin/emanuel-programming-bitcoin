from unittest import TestCase

from pybtc.script import *
from pybtc.ecc import S256Point, Signature


class ScriptTest(TestCase):
    def test_evaluate(self):
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60

        p = S256Point(0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
                      0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)
        sec = p.sec(False)

        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4

        s = Signature(r, s)
        sig = s.der()

        script_pubkey_1 = Script([sec, 0xAC])
        script_sig_1 = Script([sig])

        combined_script_1 = script_sig_1 + script_pubkey_1

        self.assertTrue(combined_script_1.evaluate(z))

        script_pubkey_2 = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
        script_sig_2 = Script([0x52])
        combined_script_2 = script_sig_2 + script_pubkey_2
        self.assertTrue(combined_script_2.evaluate(z))

        script_sig_3 = Script([0x53, 0x8f])
        combined_script_3 = script_sig_3 + script_pubkey_2
        self.assertTrue(combined_script_3.evaluate(z))
