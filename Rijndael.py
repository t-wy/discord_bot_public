# Supporting Rijndael block cipher Encryption and Decryption in Python
# (The superclass of AES)
# Supported Block Size (in bytes): 16, 20, 24, 28, 32
# Supported Key Size (in bytes): 16, 20, 24, 28, 32
# Reference: https://web.archive.org/web/20070226100442/http://csrc.nist.gov/CryptoToolkit/aes/rijndael/Rijndael.pdf
# Implementation by TWY (@t-wy)
# The "TypeError: decrypt() cannot be called after encrypt()"-like thing is not raised, but expect unexpected behavior if you do so unless you know what you are doing.

# The Numpy implementation provides an advantage when there are about more than 5 blocks to handle.

# Usage:
"""
import Rijndael
cipher = Rijndael.new(b'Hello World! xxx', blocksize=160, mode=Rijndael.MODE_ECB)
plaintext: bytes = b"Hello World!\x08\x08\x08\x08\x08\x08\x08\x08"
ciphertext: bytes = cipher.encrypt(plaintext)
"""

"""
MIT License

Copyright (c) 2024 TWY

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# """
class _Rijndael:
    # The version without numpy
    __sbox = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    )

    __sbox_inv = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
    )

    __r_con = [
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
    ]
    __xtime = lambda a: ((a << 1) ^ 0x11B) if (a & 0x80) else (a << 1)
    __xor = lambda a, b: bytes([ac ^ bc for ac, bc in zip(a, b)])
    def __bytes2matrix(bs):
        return [[j for j in bs[i:i+4]] for i in range(0, len(bs), 4)]
    def __matrix2bytes(bs):
        return bytes([y for x in bs for y in x])

    def __init__(self, key, mode, blocksize=128, *args, **kwargs):
        assert blocksize % 32 == 0
        assert blocksize >> 3 in block_size
        if mode in [MODE_CBC, MODE_CFB, MODE_OFB]:
            if "iv" in kwargs:
                self.iv = kwargs["iv"]
                assert len(self.iv) << 3 == blocksize
            else:
                import os
                self.iv = os.urandom(blocksize >> 3)
            self.__iv = self.iv
        self.nc = blocksize >> 3 # number of chars
        self.nk = blocksize >> 5 # number of cols
        self.blocksize = blocksize
        self.n_rounds = 6 + max(self.nk, len(key) >> 2)
        self.keymatrix = _Rijndael.__bytes2matrix(key)
        self.extend_key()
        if blocksize == 128:
            self.shift = [1, 2, 3]
        elif blocksize == 160:
            self.shift = [1, 2, 3]
        elif blocksize == 192:
            self.shift = [1, 2, 3]
        elif blocksize == 224:
            self.shift = [1, 2, 4]
        elif blocksize == 256:
            self.shift = [1, 3, 4]
        else:
            assert False
        if mode == MODE_ECB:
            self.encrypt = self.__encrypt_ecb
            self.decrypt = self.__decrypt_ecb
        elif mode == MODE_CBC:
            self.encrypt = self.__encrypt_cbc
            self.decrypt = self.__decrypt_cbc
        elif mode == MODE_CFB:
            self.encrypt = self.__encrypt_cfb
            self.decrypt = self.__decrypt_cfb
        elif mode == MODE_OFB:
            self.encrypt = self.__encrypt_ofb
            self.decrypt = self.__decrypt_ofb
    def extend_key(self):
        i = len(self.keymatrix)
        i2 = i
        n_rounds = 6 + max(self.nk, i)
        while i < (n_rounds + 1) * self.nk:
            self.keymatrix.append([])
            if i % i2 == 0:
                for j in range(4):
                    self.keymatrix[i].append(self.keymatrix[i - i2][j] ^ _Rijndael.__sbox[self.keymatrix[i - 1][(j + 1) % 4]] ^ (_Rijndael.__r_con[(i // i2) - 1] if j == 0 else 0))
            elif i2 > 6 and i % i2 == 4:
                for j in range(4):
                    self.keymatrix[i].append(self.keymatrix[i - i2][j] ^ _Rijndael.__sbox[self.keymatrix[i - 1][j]])
            else:
                for j in range(4):
                    self.keymatrix[i].append(self.keymatrix[i - i2][j] ^ self.keymatrix[i - 1][j])
            i += 1
    def __add_round_key(matrix, keymatrix):
        for j in range(len(matrix)):
            for i in range(4):
                matrix[j][i] ^= keymatrix[j][i]

    def __encrypt_block(self, data):
        def sub_bytes(matrix):
            for j in range(len(matrix)):
                for i in range(4):
                    matrix[j][i] = _Rijndael.__sbox[matrix[j][i]]
        def shift_rows(s):
            for row in range(1, 4):
                temp = []
                for col in range(len(s)):
                    temp.append(s[col][row])
                temp = temp[self.shift[row-1]:] + temp[:self.shift[row-1]]
                for col in range(len(s)):
                    s[col][row] = temp[col]
        def mix_columns(matrix):
            for j in range(len(matrix)):
                a, b, c, d = matrix[j]
                t = a ^ b ^ c ^ d
                matrix[j] = [
                    a ^ t ^ _Rijndael.__xtime(a ^ b),
                    b ^ t ^ _Rijndael.__xtime(b ^ c),
                    c ^ t ^ _Rijndael.__xtime(c ^ d),
                    d ^ t ^ _Rijndael.__xtime(d ^ a),
                ]
        assert len(data) << 3 == self.blocksize
        matrix = _Rijndael.__bytes2matrix(data)
        _Rijndael.__add_round_key(matrix, self.keymatrix[:self.nk])
        for i in range(1, self.n_rounds):
            sub_bytes(matrix)
            shift_rows(matrix)
            mix_columns(matrix)
            _Rijndael.__add_round_key(matrix, self.keymatrix[i * self.nk: (i + 1) * self.nk])
        sub_bytes(matrix)
        shift_rows(matrix)
        _Rijndael.__add_round_key(matrix, self.keymatrix[self.n_rounds * self.nk:])
        return _Rijndael.__matrix2bytes(matrix)

    def __decrypt_block(self, data):
        def sub_bytes_inv(matrix):
            for j in range(len(matrix)):
                for i in range(4):
                    matrix[j][i] = _Rijndael.__sbox_inv[matrix[j][i]]
        def shift_rows_inv(s):
            for row in range(1, 4):
                temp = []
                for col in range(len(s)):
                    temp.append(s[col][row])
                temp = temp[-self.shift[row-1]:] + temp[:-self.shift[row-1]]
                for col in range(len(s)):
                    s[col][row] = temp[col]
        def mix_columns_inv(matrix):
            for j in range(len(matrix)):
                a, b, c, d = matrix[j]
                u, v = _Rijndael.__xtime(_Rijndael.__xtime(a ^ c)), _Rijndael.__xtime(_Rijndael.__xtime(b ^ d))
                a, b, c, d = a ^ u, b ^ v, c ^ u, d ^ v
                t = a ^ b ^ c ^ d
                matrix[j] = [
                    a ^ t ^ _Rijndael.__xtime(a ^ b),
                    b ^ t ^ _Rijndael.__xtime(b ^ c),
                    c ^ t ^ _Rijndael.__xtime(c ^ d),
                    d ^ t ^ _Rijndael.__xtime(d ^ a),
                ]
        matrix = _Rijndael.__bytes2matrix(data)
        _Rijndael.__add_round_key(matrix, self.keymatrix[self.n_rounds * self.nk:])
        shift_rows_inv(matrix)
        sub_bytes_inv(matrix)
        for i in range(self.n_rounds - 1, 0, -1):
            _Rijndael.__add_round_key(matrix, self.keymatrix[i * self.nk: (i + 1) * self.nk])
            mix_columns_inv(matrix)
            shift_rows_inv(matrix)
            sub_bytes_inv(matrix)
        _Rijndael.__add_round_key(matrix, self.keymatrix[:self.nk])
        return _Rijndael.__matrix2bytes(matrix)

    def __encrypt_ecb(self, plaintext):
        assert (len(plaintext) << 3) % self.blocksize == 0
        return b"".join([self.__encrypt_block(plaintext[x:x+self.nc]) for x in range(0, len(plaintext), self.nc)])
    def __decrypt_ecb(self, ciphertext):
        assert (len(ciphertext) << 3) % self.blocksize == 0
        return b"".join([self.__decrypt_block(ciphertext[x:x+self.nc]) for x in range(0, len(ciphertext), self.nc)])

    def __encrypt_cbc(self, plaintext):
        assert (len(plaintext) << 3) % self.blocksize == 0
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = self.__encrypt_block(_Rijndael.__xor(plaintext[x:x+self.nc], self.__iv))
            result += self.__iv
        return result
    def __decrypt_cbc(self, ciphertext):
        assert (len(ciphertext) << 3) % self.blocksize == 0
        result = b""
        for x in range(0, len(ciphertext), self.nc):
            result += _Rijndael.__xor(self.__decrypt_block(ciphertext[x:x+self.nc]), self.__iv)
            self.__iv = ciphertext[x:x+self.nc]
        return result

    def __encrypt_cfb(self, plaintext):
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = _Rijndael.__xor(self.__encrypt_block(self.__iv), plaintext[x:x+self.nc])
            result += self.__iv
        return result
    def __decrypt_cfb(self, ciphertext):
        result = b""
        for x in range(0, len(ciphertext), self.nc):
            result += _Rijndael.__xor(self.__encrypt_block(self.__iv), ciphertext[x:x+self.nc])
            self.__iv = ciphertext[x:x+self.nc]
        return result

    def __encrypt_ofb(self, plaintext):
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = self.__encrypt_block(self.__iv)
            result += _Rijndael.__xor(self.__iv, plaintext[x:x+self.nc])
        return result
    def __decrypt_ofb(self, ciphertext):
        result = b""
        for x in range(0, len(ciphertext), self.nc):
            self.__iv = self.__encrypt_block(self.__iv)
            result += _Rijndael.__xor(self.__iv, ciphertext[x:x+self.nc])
        return result
# """

import numpy as np
class Rijndael:
    __sbox = np.array([
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
    ], np.uint8)

    __sbox_inv = np.array([
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
    ], np.uint8)

    __r_con = np.array([
        0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
    ], np.uint8)
    __xtimearr = np.array([
        0x00, 0x02, 0x04, 0x06, 0x08, 0x0a, 0x0c, 0x0e, 0x10, 0x12, 0x14, 0x16, 0x18, 0x1a, 0x1c, 0x1e, 0x20, 0x22, 0x24, 0x26, 0x28, 0x2a, 0x2c, 0x2e, 0x30, 0x32, 0x34, 0x36, 0x38, 0x3a, 0x3c, 0x3e, 0x40, 0x42, 0x44, 0x46, 0x48, 0x4a, 0x4c, 0x4e, 0x50, 0x52, 0x54, 0x56, 0x58, 0x5a, 0x5c, 0x5e, 0x60, 0x62, 0x64, 0x66, 0x68, 0x6a, 0x6c, 0x6e, 0x70, 0x72, 0x74, 0x76, 0x78, 0x7a, 0x7c, 0x7e, 0x80, 0x82, 0x84, 0x86, 0x88, 0x8a, 0x8c, 0x8e, 0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e, 0xa0, 0xa2, 0xa4, 0xa6, 0xa8, 0xaa, 0xac, 0xae, 0xb0, 0xb2, 0xb4, 0xb6, 0xb8, 0xba, 0xbc, 0xbe, 0xc0, 0xc2, 0xc4, 0xc6, 0xc8, 0xca, 0xcc, 0xce, 0xd0, 0xd2, 0xd4, 0xd6, 0xd8, 0xda, 0xdc, 0xde, 0xe0, 0xe2, 0xe4, 0xe6, 0xe8, 0xea, 0xec, 0xee, 0xf0, 0xf2, 0xf4, 0xf6, 0xf8, 0xfa, 0xfc, 0xfe, 0x1b, 0x19, 0x1f, 0x1d, 0x13, 0x11, 0x17, 0x15, 0x0b, 0x09, 0x0f, 0x0d, 0x03, 0x01, 0x07, 0x05, 0x3b, 0x39, 0x3f, 0x3d, 0x33, 0x31, 0x37, 0x35, 0x2b, 0x29, 0x2f, 0x2d, 0x23, 0x21, 0x27, 0x25, 0x5b, 0x59, 0x5f, 0x5d, 0x53, 0x51, 0x57, 0x55, 0x4b, 0x49, 0x4f, 0x4d, 0x43, 0x41, 0x47, 0x45, 0x7b, 0x79, 0x7f, 0x7d, 0x73, 0x71, 0x77, 0x75, 0x6b, 0x69, 0x6f, 0x6d, 0x63, 0x61, 0x67, 0x65, 0x9b, 0x99, 0x9f, 0x9d, 0x93, 0x91, 0x97, 0x95, 0x8b, 0x89, 0x8f, 0x8d, 0x83, 0x81, 0x87, 0x85, 0xbb, 0xb9, 0xbf, 0xbd, 0xb3, 0xb1, 0xb7, 0xb5, 0xab, 0xa9, 0xaf, 0xad, 0xa3, 0xa1, 0xa7, 0xa5, 0xdb, 0xd9, 0xdf, 0xdd, 0xd3, 0xd1, 0xd7, 0xd5, 0xcb, 0xc9, 0xcf, 0xcd, 0xc3, 0xc1, 0xc7, 0xc5, 0xfb, 0xf9, 0xff, 0xfd, 0xf3, 0xf1, 0xf7, 0xf5, 0xeb, 0xe9, 0xef, 0xed, 0xe3, 0xe1, 0xe7, 0xe5
    ], np.uint8)
    # __xtime = lambda a: ((a << 1) ^ 0x11B) if (a & 0x80) else (a << 1)
    __xor = lambda a, b: bytes([ac ^ bc for ac, bc in zip(a, b)])

    def __bytes2matrix(bs: bytes):
        return np.ndarray((len(bs) >> 2, 4), np.uint8, bytearray(bs))
    def __bytes2matrix2(bs: bytes, col: int):
        return np.ndarray(((len(bs) >> 2) // col, col, 4), np.uint8, bytearray(bs))
    def __matrix2bytes(bs) -> bytes:
        return bs.tobytes()

    def __init__(self, key, mode, blocksize=128, *args, **kwargs):
        assert blocksize % 32 == 0
        assert blocksize >> 3 in block_size
        if mode in [MODE_CBC, MODE_CFB, MODE_OFB]:
            if "iv" in kwargs:
                self.iv = kwargs["iv"]
                assert len(self.iv) << 3 == blocksize
            else:
                import os
                self.iv = os.urandom(blocksize >> 3)
            self.__iv = self.iv
        self.nc = blocksize >> 3 # number of chars
        self.nk = blocksize >> 5 # number of cols
        self.blocksize = blocksize
        self.n_rounds = 6 + max(self.nk, len(key) >> 2)
        self.keymatrix = Rijndael.__bytes2matrix(key)
        self.extend_key()
        if blocksize == 128:
            self.shift = [1, 2, 3]
        elif blocksize == 160:
            self.shift = [1, 2, 3]
        elif blocksize == 192:
            self.shift = [1, 2, 3]
        elif blocksize == 224:
            self.shift = [1, 2, 4]
        elif blocksize == 256:
            self.shift = [1, 3, 4]
        else:
            assert False
        if mode == MODE_ECB:
            self.encrypt = self.__encrypt_ecb
            self.decrypt = self.__decrypt_ecb
        elif mode == MODE_CBC:
            self.encrypt = self.__encrypt_cbc
            self.decrypt = self.__decrypt_cbc
        elif mode == MODE_CFB:
            self.encrypt = self.__encrypt_cfb
            self.decrypt = self.__decrypt_cfb
        elif mode == MODE_OFB:
            self.encrypt = self.__encrypt_ofb
            self.decrypt = self.__decrypt_ofb

    def extend_key(self) -> None:
        i = len(self.keymatrix)
        i2 = i
        n_rounds = 6 + max(self.nk, i)
        self.keymatrix = np.pad(self.keymatrix, ((0, (n_rounds + 1) * self.nk - i), (0, 0)))
        while i < (n_rounds + 1) * self.nk:
            if i % i2 == 0:
                for j in range(4):
                    self.keymatrix[i][j] = self.keymatrix[i - i2][j] ^ Rijndael.__sbox[self.keymatrix[i - 1][(j + 1) % 4]] ^ (Rijndael.__r_con[(i // i2) - 1] if j == 0 else 0)
            elif i2 > 6 and i % i2 == 4:
                for j in range(4):
                    self.keymatrix[i][j] = self.keymatrix[i - i2][j] ^ Rijndael.__sbox[self.keymatrix[i - 1][j]]
            else:
                for j in range(4):
                    self.keymatrix[i][j] = self.keymatrix[i - i2][j] ^ self.keymatrix[i - 1][j]
            i += 1

    def __add_round_key(matrix, keymatrix):
        matrix ^= keymatrix

    def __encrypt_blocks(self, data: bytes) -> bytes:
        def sub_bytes(matrix):
            return Rijndael.__sbox[matrix]
        def shift_rows(s):
            s[:,:,1] = np.roll(s[:,:,1], -self.shift[0], axis=1)
            s[:,:,2] = np.roll(s[:,:,2], -self.shift[1], axis=1)
            s[:,:,3] = np.roll(s[:,:,3], -self.shift[2], axis=1)
        def mix_columns(matrix):
            t = matrix[:,:,0] ^ matrix[:,:,1] ^ matrix[:,:,2] ^ matrix[:,:,3]
            s = matrix[:,:,0].copy()
            matrix[:,:,0] ^= t ^ Rijndael.__xtimearr[matrix[:,:,0] ^ matrix[:,:,1]]
            matrix[:,:,1] ^= t ^ Rijndael.__xtimearr[matrix[:,:,1] ^ matrix[:,:,2]]
            matrix[:,:,2] ^= t ^ Rijndael.__xtimearr[matrix[:,:,2] ^ matrix[:,:,3]]
            matrix[:,:,3] ^= t ^ Rijndael.__xtimearr[matrix[:,:,3] ^ s]
        matrix = Rijndael.__bytes2matrix2(data, self.nk)
        Rijndael.__add_round_key(matrix, self.keymatrix[:self.nk])
        for i in range(1, self.n_rounds):
            matrix = sub_bytes(matrix)
            shift_rows(matrix)
            mix_columns(matrix)
            Rijndael.__add_round_key(matrix, self.keymatrix[i * self.nk: (i + 1) * self.nk])
        matrix = sub_bytes(matrix)
        shift_rows(matrix)
        Rijndael.__add_round_key(matrix, self.keymatrix[self.n_rounds * self.nk:])
        return Rijndael.__matrix2bytes(matrix)

    def __decrypt_blocks(self, data: bytes) -> bytes:
        def sub_bytes_inv(matrix):
            return Rijndael.__sbox_inv[matrix]
        def shift_rows_inv(s):
            s[:,:,1] = np.roll(s[:,:,1], self.shift[0], axis=1)
            s[:,:,2] = np.roll(s[:,:,2], self.shift[1], axis=1)
            s[:,:,3] = np.roll(s[:,:,3], self.shift[2], axis=1)
        def mix_columns_inv(matrix):
            u = Rijndael.__xtimearr[Rijndael.__xtimearr[matrix[:,:,0] ^ matrix[:,:,2]]]
            v = Rijndael.__xtimearr[Rijndael.__xtimearr[matrix[:,:,1] ^ matrix[:,:,3]]]
            matrix[:,:,0] ^= u
            matrix[:,:,1] ^= v
            matrix[:,:,2] ^= u
            matrix[:,:,3] ^= v
            t = matrix[:,:,0] ^ matrix[:,:,1] ^ matrix[:,:,2] ^ matrix[:,:,3]
            s = matrix[:,:,0].copy()
            matrix[:,:,0] ^= t ^ Rijndael.__xtimearr[matrix[:,:,0] ^ matrix[:,:,1]]
            matrix[:,:,1] ^= t ^ Rijndael.__xtimearr[matrix[:,:,1] ^ matrix[:,:,2]]
            matrix[:,:,2] ^= t ^ Rijndael.__xtimearr[matrix[:,:,2] ^ matrix[:,:,3]]
            matrix[:,:,3] ^= t ^ Rijndael.__xtimearr[matrix[:,:,3] ^ s]
        matrix = Rijndael.__bytes2matrix2(data, self.nk)
        Rijndael.__add_round_key(matrix, self.keymatrix[self.n_rounds * self.nk:])
        shift_rows_inv(matrix)
        matrix = sub_bytes_inv(matrix)
        for i in range(self.n_rounds - 1, 0, -1):
            Rijndael.__add_round_key(matrix, self.keymatrix[i * self.nk: (i + 1) * self.nk])
            mix_columns_inv(matrix)
            shift_rows_inv(matrix)
            matrix = sub_bytes_inv(matrix)
        Rijndael.__add_round_key(matrix, self.keymatrix[:self.nk])
        return Rijndael.__matrix2bytes(matrix)

    def __encrypt_ecb(self, plaintext: bytes) -> bytes:
        assert (len(plaintext) << 3) % self.blocksize == 0
        return self.__encrypt_blocks(plaintext)
    def __decrypt_ecb(self, ciphertext: bytes) -> bytes:
        assert (len(ciphertext) << 3) % self.blocksize == 0
        return self.__decrypt_blocks(ciphertext)

    def __encrypt_cbc(self, plaintext: bytes) -> bytes:
        assert (len(plaintext) << 3) % self.blocksize == 0
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = self.__encrypt_blocks(Rijndael.__xor(plaintext[x:x+self.nc], self.__iv))
            result += self.__iv
        return result
    def __decrypt_cbc(self, ciphertext: bytes) -> bytes:
        assert (len(ciphertext) << 3) % self.blocksize == 0
        result = Rijndael.__xor(self.__decrypt_blocks(ciphertext), self.__iv + ciphertext[:-self.nc])
        self.__iv = ciphertext[-self.nc:]
        return result

    def __encrypt_cfb(self, plaintext: bytes) -> bytes:
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = Rijndael.__xor(self.__encrypt_blocks(self.__iv), plaintext[x:x+self.nc])
            result += self.__iv
        return result
    def __decrypt_cfb(self, ciphertext: bytes) -> bytes:
        result = b""
        blocklen = len(ciphertext)
        result = Rijndael.__xor(self.__encrypt_blocks(self.__iv + ciphertext[:blocklen-blocklen%self.nc]), ciphertext)
        self.__iv = ciphertext[-self.nc:]
        return result

    def __encrypt_ofb(self, plaintext: bytes) -> bytes:
        result = b""
        for x in range(0, len(plaintext), self.nc):
            self.__iv = self.__encrypt_blocks(self.__iv)
            result += Rijndael.__xor(self.__iv, plaintext[x:x+self.nc])
        return result
    def __decrypt_ofb(self, ciphertext: bytes) -> bytes:
        result = b""
        for x in range(0, len(ciphertext), self.nc):
            self.__iv = self.__encrypt_blocks(self.__iv)
            result += Rijndael.__xor(self.__iv, ciphertext[x:x+self.nc])
        return result

def new(*args, **kwargs):
    return Rijndael(*args, **kwargs)

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
#MODE_CTR = 6
#MODE_OPENPGP = 7
#MODE_CCM = 8
#MODE_EAX = 9
#MODE_SIV = 10
#MODE_GCM = 11
#MODE_OCB = 12

# Size of a data block (in bytes)
block_size = (16, 20, 24, 28, 32)
# Size of a key (in bytes)
key_size = (16, 20, 24, 28, 32)

leng = 16

def test():
    from time import time
    start = time()
    print("Tests Start")
    try:
        # https://csrc.nist.gov/csrc/media/publications/fips/197/final/documents/fips-197.pdf
        # dummy = new()
        # keymatrix = Rijndael.bytes2matrix(bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"))
        # dummy.extend_key(keymatrix)
        # output = "\n".join(["".join([hex(y)[2:].zfill(2) for y in x]) for x in keymatrix])
        # assert output[-8:] == "b6630ca6"
        # keymatrix = Rijndael.bytes2matrix(bytes.fromhex("8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"))
        # dummy.extend_key(keymatrix)
        # output = "\n".join(["".join([hex(y)[2:].zfill(2) for y in x]) for x in keymatrix])
        # assert output[-8:] == "01002202"
        # keymatrix = Rijndael.bytes2matrix(bytes.fromhex("603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"))
        # dummy.extend_key(keymatrix)
        # output = "\n".join(["".join([hex(y)[2:].zfill(2) for y in x]) for x in keymatrix])
        # assert output[-8:] == "706c631e"
        # test known pairs from https://link.springer.com/content/pdf/bbm:978-3-662-60769-5/1.pdf
        tests = [
            [
                ("66e94bd4ef8a2c3b884cfa59ca342b2e", "f795bd4a52e29ed713d313fa20e98dbc"),
                ("94b434f8f57b9780f0eff1a9ec4c112c", "35a00ec955df43417ceac2ab2b3f3e76"),
                ("aae06992acbf52a3e8f4a96ec9300bd7", "52f674b7b9030fdab13d18dc214eb331"),
                ("73f8dff62a36f3ebf31d6f73a56ff279", "3a72f21e10b6473ea9ff14a232e675b4"),
                ("dc95c078a2408989ad48a21492842087", "08c374848c228233c2b34f332bd2e9d3"),
            ],
            [
                ("9e38b8eb1d2025a1665ad4b1f5438bb5cae1ac3f", "939c167e7f916d45670ee21bfc939e1055054a96"),
                ("33b12ab81db7972e8fdc529dda46fcb529b31826", "97f03eb018c0bb9195bf37c6a0aece8e4cb8de5f"),
                ("33060f9d4705ddd2c7675f0099140e5a98729257", "012cab64982156a5710e790f85ec442ce13c520f"),
                ("e9f5ea0fa39bb6ad7339f28e58e2e7535f261827", "06ef9bc82905306d45810e12d0807796a3d338f9"),
                ("30991844f72973b3b2161f1f11e7f8d9863c5118", "eef8b7cc9dbe0f03a1fe9d82e9a759fd281c67e0"),
            ],
            [
                ("a92732eb488d8bb98ecd8d95dc9c02e052f250ad369b3849", "106f34179c3982ddc6750aa01936b7a180e6b0b9d8d690ec"),
                ("528e2fff6005427b67bb1ed31ecc09a69ef41531df5ba5b2", "71c7687a4c93ebc35601e3662256e10115beed56a410d7ac"),
                ("c6348be20007bac4a8bd62890c8147a2432e760e9a9f9ab8", "eb9def13c253f81c1fc2829426ed166a65a105c6a04ca33d"),
                ("ecbe9942cd6703e16d358a829d542456d71bd3408eb23c56", "fd10458ed034368a34047905165b78a6f0591ffeebf47cc7"),
                ("17004e806faef168fc9cd56f98f070982075c70c8132b945", "bed33b0af364dbf15f9c2f3fb24fbdf1d36129c586eea6b7"),
            ],
            [
                ("0623522d88f7b9c63437537157f625dd5697ab628a3b9be2549895c8", "93f93cbdabe23415620e6990b0443d621f6afbd6edefd6990a1965a8"),
                ("58a0c53f3822a32464704d409c2fd0521f3a93e1f6fcfd4c87f1c551", "d8e93ef2eb49857049d6f6e0f40b67516d2696f94013c065283f7f01"),
                ("3856b17bea77c4611e3397066828aadda004706a2c8009df40a811fe", "160ad76a97ae2c1e05942fde3da2962684a92ccc74b8dc23bde4f469"),
                ("fe1cf0c8ddad24e3d751933100e8e89b61cd5d31c96abff7209c495c", "515d8e2f2b9c5708f112c6de31caca47afb86838b716975a24a09cd4"),
                ("9bf26fad5680d56b572067ec2fe162f449404c86303f8be38fab6e02", "658f144a34af44aae66cfddab955c483dfbcb4ee9a19a6701f158a66"),
            ],
            [
                ("a693b288df7dae5b1757640276439230db77c4cd7a871e24d6162e54af434891", "5f05857c80b68ea42ccbc759d42c28d5cd490f1d180c7a9397ee585bea770391"),
                ("938d36e0cb6b7937841dab7f1668e47b485d3acd6b3f6d598b0a9f923823331d", "7b44491d1b24a93b904d171f074ad69669c2b70b134a4d2d773250a4414d78be"),
                ("f927363ef5b3b4984a9eb9109844152ec167f08102644e3f9028070433df9f2a", "4e03389c68b2e3f623ad8f7f6bfc88613b86f334f4148029ae25f50db144b80c"),
                ("bc18bf6d369c955bbb271cbcdd66c368356dba5b33c0005550d2320b1c617e21", "60aba1d2be45d8abfdcf97bcb39f6c17df29985cf321bab75e26a26100ac00af"),
                ("c6227e7740b7e53b5cb77865278eab0726f62366d9aabad908936123a1fc8af3", "9843e807319c32ad1ea3935ef56a2ba96e4bf19c30e47d88a2b97cbbf2e159e7"),
            ],
        ]
        for i in range(5):
            for j in range(5):
                key = b"\0" * (16 + (j << 2))
                plaintext = b"\0" * (16 + (i << 2))
                blocksize = (i + 4) << 5

                test = plaintext
                test = new(key, MODE_ECB, blocksize=blocksize).encrypt(test)
                assert test.hex() == tests[i][j][0]
                test = new(key, MODE_ECB, blocksize=blocksize).encrypt(test)
                assert test.hex() == tests[i][j][1]
                test = new(key, MODE_ECB, blocksize=blocksize).decrypt(test)
                assert test.hex() == tests[i][j][0]
                test = new(key, MODE_ECB, blocksize=blocksize).decrypt(test)
                assert test == plaintext
        # test reversibility
        for mode in [MODE_ECB, MODE_CBC, MODE_CFB, MODE_OFB]:
            for bst in block_size:
                for kst in key_size:
                    bs = bst << 3
                    test_cases = [bst, bst*3]
                    if mode in [MODE_CFB, MODE_OFB]:
                        test_cases.append(127)
                        test_cases.append(1237)
                    for tc in test_cases:
                        plaintext = bytes([x & 0xff for x in range(tc)])
                        key = bytes([x for x in range(kst)])
                        kwargs = {}
                        if mode in [MODE_CBC, MODE_CFB, MODE_OFB]:
                            kwargs["iv"] = bytes([x for x in range(16, 16 + (bs >> 3))])
                        test = new(key, mode, blocksize=bs, **kwargs).encrypt(plaintext)
                        test = new(key, mode, blocksize=bs, **kwargs).decrypt(test)
                        assert test == plaintext
        print("Tests Succeed")
        print("Time Elapsed: {}s".format(time() - start))
    except:
        print("Tests Fail")
        import traceback
        traceback.print_exc()
    start = time()
    print("Speed Test Start")
    try:
        for mode in [MODE_ECB, MODE_CBC, MODE_CFB, MODE_OFB]:
            for block_count in [1, 5, 10, 100, 1000, 10000]:
                cipher = _Rijndael(b'Hello World! xxx', blocksize=160, mode=MODE_ECB)
                plaintext: bytes = b"Hello World!\x08\x08\x08\x08\x08\x08\x08\x08" * block_count
                start = time()
                cipher.encrypt(plaintext)
                print("{}, {} blocks, Normal encrypt: Time Elapsed: {}s".format(mode, block_count, time() - start))
                start = time()
                cipher.decrypt(plaintext)
                print("{}, {} blocks, Normal decrypt: Time Elapsed: {}s".format(mode, block_count, time() - start))
                cipher = Rijndael(b'Hello World! xxx', blocksize=160, mode=MODE_ECB)
                plaintext: bytes = b"Hello World!\x08\x08\x08\x08\x08\x08\x08\x08" * block_count
                start = time()
                cipher.encrypt(plaintext)
                print("{}, {} blocks, Numpy encrypt: Time Elapsed: {}s".format(mode, block_count, time() - start))
                start = time()
                cipher.decrypt(plaintext)
                print("{}, {} blocks, Numpy decrypt: Time Elapsed: {}s".format(mode, block_count, time() - start))
        print("Speed Test Succeed")
    except:
        print("Speed Tests Fail")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test()
