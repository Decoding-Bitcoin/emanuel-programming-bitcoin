import requests
from io import BytesIO

from pybtc.helper import *
from pybtc.script import *


class Tx:
    def __init__(self, version, tx_ins, tx_outs, lock_time, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.lock_time = lock_time
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''
        for tx_in in self.tx_ins:
            tx_ins += tx_in.__repr__() + '\n'
        tx_outs = ''

        for tx_out in self.tx_outs:
            tx_outs += tx_out.__repr__() + '\n'

        return 'tx: {}\nversion: {}\ntx_ins: {}\ntx_outs: {}\nlock_time: {}\n'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.lock_time
        )

    def id(self):
        """Human-readable hexadecimal of the transaction hash"""
        return self.hash().hex()

    def hash(self):
        """Binary hash of the legacy serialization"""
        return hash256(self.serialize())[::-1]

    def serialize(self):
        """Returns the byte serialization of the transaction"""
        result = int_to_little_endian(self.version, 4)

        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.lock_time, 4)
        return result

    def fee(self, testnet=False):
        fee = 0

        for tx_in in self.tx_ins:
            fee += tx_in.value(testnet)

        for tx_out in self.tx_outs:
            fee -= tx_out.amount

        return fee

    @classmethod
    def parse(cls, stream, testnet=False):
        serialized_version = stream.read(4)
        version = little_endian_to_int(serialized_version)

        input_qty = read_varint(stream)
        tx_ins = []
        for n in range(input_qty):
            tx_ins.append(TxIn.parse(stream, testnet))

        output_qty = read_varint(stream)
        tx_outs = []
        for n in range(output_qty):
            tx_outs.append(TxOut.parse(stream, testnet))

        serialized_lock_time = stream.read(4)
        lock_time = little_endian_to_int(serialized_lock_time)

        return Tx(version, tx_ins, tx_outs, lock_time)


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return '{}:{}'.format(self.prev_tx.hex(), self.prev_index)

    def serialize(self):
        """Returns the byte serialization of the transaction input"""
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet)

    def value(self, testnet=False):
        """
        Get the output value by looking up the tx hash
        Returns the amount in satoshi
        """
        tx = self.fetch_tx(testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        """
        Get the ScriptPubKey by looking up the tx hash
        Returns a Script object
        """
        tx = self.fetch_tx(testnet)
        return tx.tx_outs[self.prev_index].script_pubkey

    @classmethod
    def parse(cls, stream, testnet=False):
        tx_id = stream.read(32)[::-1]

        serialized_tx_index = stream.read(4)
        tx_index = little_endian_to_int(serialized_tx_index)

        script_sig = Script.parse(stream)

        serialized_sequence = stream.read(4)
        sequence = little_endian_to_int(serialized_sequence)

        return TxIn(tx_id, tx_index, script_sig, sequence)


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    def serialize(self):
        """Returns the byte serialization of the transaction output"""
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

    @classmethod
    def parse(cls, stream, testnet=False):
        serialized_amount = stream.read(8)
        amount = little_endian_to_int(serialized_amount)

        script_pubkey = Script.parse(stream)

        return TxOut(amount, script_pubkey)


class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('Unexpected response: {}'.format(response.text))

            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet)
                tx.lock_time = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet)

            if tx.id() != tx_id:
                raise ValueError('Not the same id: {} vs {}'.format(tx.id(), tx_id))

            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
