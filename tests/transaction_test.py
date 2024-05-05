from unittest import TestCase

from pybtc.transaction import *
from pybtc.script import *


class TransactionTest(TestCase):
    def test_parse(self):
        raw_transaction = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_transaction)
        transaction = Tx.parse(stream)

        # Assert Version
        self.assertEqual(transaction.version, 1)

        # Assert tx_ins size
        self.assertEqual(len(transaction.tx_ins), 1)

        # Assert tx_in prev_tx and prev_index
        prev_tx = bytes.fromhex('813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1')[::-1]
        self.assertEqual(transaction.tx_ins[0].prev_tx, prev_tx)
        self.assertEqual(transaction.tx_ins[0].prev_index, 0)

        # Assert script sig
        raw_script = bytes.fromhex(
            '6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        script_stream = BytesIO(raw_script)
        script_sig = Script.parse(script_stream)
        self.assertEqual(transaction.tx_ins[0].script_sig.cmds, script_sig.cmds)

        # Assert sequence
        sequence = little_endian_to_int(bytes.fromhex('feffffff'))
        self.assertEqual(transaction.tx_ins[0].sequence, sequence)

        # Assert tx_outs size
        self.assertEqual(len(transaction.tx_outs), 2)

        # Assert tx_out[0] amount
        amount = little_endian_to_int(bytes.fromhex('a135ef0100000000'))
        self.assertEqual(transaction.tx_outs[0].amount, amount)

        # Assert tx_out[0] script pubkey
        raw_script_pubkey_0 = bytes.fromhex('1976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
        script_pubkey_0_stream = BytesIO(raw_script_pubkey_0)
        script_pubkey_0 = Script.parse(script_pubkey_0_stream)
        self.assertEqual(transaction.tx_outs[0].script_pubkey.cmds, script_pubkey_0.cmds)

        # Assert tx_out[1] amount
        amount = little_endian_to_int(bytes.fromhex('99c3980000000000'))
        self.assertEqual(transaction.tx_outs[1].amount, amount)

        # Assert tx_out[1] script pubkey
        raw_script_pubkey_1 = bytes.fromhex('1976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
        script_pubkey_1_stream = BytesIO(raw_script_pubkey_1)
        script_pubkey_1 = Script.parse(script_pubkey_1_stream)
        self.assertEqual(transaction.tx_outs[1].script_pubkey.cmds, script_pubkey_1.cmds)

        # Assert lock_time
        lock_time = little_endian_to_int(0x19430600.to_bytes(4))
        self.assertEqual(transaction.lock_time, lock_time)

    def test_fee(self):
        raw_transaction = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_transaction)
        transaction = Tx.parse(stream)
        self.assertEqual(transaction.fee(), 40000)

    def test_serialize(self):
        raw_transaction = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_transaction)
        transaction = Tx.parse(stream)
        self.assertEqual(transaction.serialize(), raw_transaction)

    def test_hash(self):
        raw_transaction = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_transaction)
        transaction = Tx.parse(stream)
        tx_hash = bytes.fromhex('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
        self.assertEqual(transaction.hash(), tx_hash)

    def test_id(self):
        raw_transaction = bytes.fromhex(
            '0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_transaction)
        transaction = Tx.parse(stream)
        self.assertEqual(transaction.id(), '452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
