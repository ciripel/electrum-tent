# -*- coding: utf-8 -*-
#
# Electrum - lightweight Bitcoin client
# Copyright (C) 2018 The Electrum developers
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json

from .util import inv_dict
from . import bitcoin
from .blockchain import CHUNK_SIZE


def read_json(filename, default):
    path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(path, 'r') as f:
            r = json.loads(f.read())
    except:
        r = default
    return r


GIT_REPO_URL = "https://github.com/ciripel/electrum-tent"
GIT_REPO_ISSUES_URL = "https://github.com/ciripel/electrum-tent/issues"
BIP39_WALLET_FORMATS = read_json('bip39_wallet_formats.json', [])


class AbstractNet:

    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 0

    @classmethod
    def max_checkpoint(cls) -> int:
        return max(0, len(cls.CHECKPOINTS) * CHUNK_SIZE - 1)

    @classmethod
    def rev_genesis_bytes(cls) -> bytes:
        return bytes.fromhex(bitcoin.rev_hex(cls.GENESIS))


class BitcoinMainnet(AbstractNet):

    TESTNET = False
    WIF_PREFIX = 0x80
    ADDRTYPE_P2PKH = [0x1C, 0x28]
    ADDRTYPE_P2SH = [0x1C, 0x2D]
    SEGWIT_HRP = "bc"
    GENESIS = "00068b35729d9d2b0c294ff1fe9af0094740524311a131de40e7f705e4c29a5b"
    DEFAULT_PORTS = {'t': '50001', 's': '50002'}
    DEFAULT_SERVERS = read_json('servers.json', {})
    CHECKPOINTS = read_json('checkpoints.json', [])
    BLOCK_HEIGHT_FIRST_LIGHTNING_CHANNELS = 497000

    EQUIHASH_N = 200
    EQUIHASH_K = 9
    EQUIHASH_N_NEW = 144
    EQUIHASH_K_NEW = 5
    FORK_BLOCK = 266000

    EQUIHASH_FORK_HEIGHT = 266001
    OVERWINTER_HEIGHT = 520000

    XPRV_HEADERS = {
        'standard':    0x0488ade4,  # xprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x0488b21e,  # xpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 410
    LN_REALM_BYTE = 0
    LN_DNS_SEEDS = [
        'nodes.lightning.directory.',
        'lseed.bitcoinstats.com.',
        'lseed.darosior.ninja',
    ]


class BitcoinTestnet(AbstractNet):

    TESTNET = True
    WIF_PREFIX = 0xEF
    ADDRTYPE_P2PKH = [0x1D, 0x25]
    ADDRTYPE_P2SH = [0x1C, 0xBA]
    SEGWIT_HRP = "tb"
    GENESIS = "0739bced3341885cf221cf22b5e91cdb0f5da3cb34da982167c4c900723c725a"
    DEFAULT_PORTS = {'t': '51001', 's': '51002'}
    DEFAULT_SERVERS = read_json('servers_testnet.json', {})
    CHECKPOINTS = read_json('checkpoints_testnet.json', [])

    XPRV_HEADERS = {
        'standard':    0x04358394,  # tprv
    }
    XPRV_HEADERS_INV = inv_dict(XPRV_HEADERS)
    XPUB_HEADERS = {
        'standard':    0x043587cf,  # tpub
    }
    XPUB_HEADERS_INV = inv_dict(XPUB_HEADERS)
    BIP44_COIN_TYPE = 1
    LN_REALM_BYTE = 1
    LN_DNS_SEEDS = [  # TODO investigate this again
        #'test.nodes.lightning.directory.',  # times out.
        #'lseed.bitcoinstats.com.',  # ignores REALM byte and returns mainnet peers...
    ]


class BitcoinRegtest(BitcoinTestnet):

    SEGWIT_HRP = "bcrt"
    GENESIS = "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


class BitcoinSimnet(BitcoinTestnet):

    WIF_PREFIX = 0x64
    ADDRTYPE_P2PKH = 0x3f
    ADDRTYPE_P2SH = 0x7b
    SEGWIT_HRP = "sb"
    GENESIS = "683e86bd5c6d110d91b94b97137ba6bfe02dbbdb8e3dff722a669b5d69d77af6"
    DEFAULT_SERVERS = read_json('servers_regtest.json', {})
    CHECKPOINTS = []
    LN_DNS_SEEDS = []


# don't import net directly, import the module instead (so that net is singleton)
net = BitcoinMainnet

def set_simnet():
    global net
    net = BitcoinSimnet

def set_mainnet():
    global net
    net = BitcoinMainnet

def set_testnet():
    global net
    net = BitcoinTestnet


def set_regtest():
    global net
    net = BitcoinRegtest
