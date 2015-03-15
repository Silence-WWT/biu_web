# -*- coding: utf-8 -*-
import math


class MD5():
    __rotate_amounts = (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4 + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4

    __m_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    __m_2 = (1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12)
    __m_3 = (5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2)
    __m_4 = (0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9)

    __constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xffffffff for i in range(64)]

    @staticmethod
    def __F(x, y, z):
        return (x & y) | ((~x) & z)

    @staticmethod
    def __G(x, y, z):
        return (x & z) | (y & (~z))

    @staticmethod
    def __H(x, y, z):
        return x ^ y ^ z

    @staticmethod
    def __I(x, y, z):
        return y ^ (x | (~z))

    def __init__(self, message):
        hex_list = map(hex, map(ord, message))
        msg_length = len(hex_list) * 8
        hex_list.append('0x80')
        while (len(hex_list) * 8 + 64) % 512 != 0:
            hex_list.append('0x00')
        hex_msg_length = hex(msg_length)[2:]
        hex_msg_length = '0x' + hex_msg_length.rjust(16, '0')
        hex_msg_length_little_endian = self.__reverse_hex(hex_msg_length)[2:]
        for i in range(0, len(hex_msg_length_little_endian), 2):
            hex_list.append('0x' + hex_msg_length_little_endian[i:i + 2])
        self.__message_list = hex_list
        self.__constants_count = 0
        self.__hash_pieces = ['0x67452301', '0xefcdab89', '0x98badcfe', '0x10325476']

    @staticmethod
    def __reverse_hex(hex_str):
        hex_str = hex_str[2:]
        hex_str_list = []
        for i in range(0, len(hex_str), 2):
            hex_str_list.append(hex_str[i:i + 2])
        hex_str_list.reverse()
        hex_str_result = '0x' + ''.join(hex_str_list)
        return hex_str_result

    def __generate_msg_16(self, order, offset):
        ii = 0
        msg_16 = [0] * 16
        offset *= 64
        for i in order:
            i *= 4
            msg_16[ii] = '0x' + ''.join(
                (self.__message_list[i + offset] + self.__message_list[i + 1 + offset] +
                 self.__message_list[i + 2 + offset] + self.__message_list[i + 3 + offset]).split('0x'))
            ii += 1
        for c in msg_16:
            index = msg_16.index(c)
            msg_16[index] = self.__reverse_hex(c)
        return msg_16

    @staticmethod
    def __left_rotate(x, n):
        return ((x << n) | (x >> (32 - n))) & 0xffffffff

    @staticmethod
    def __shift(shift_list):
        shift_list = [shift_list[3], shift_list[0], shift_list[1], shift_list[2]]
        return shift_list

    def __func(self, fun, m, rotate_amounts):
        count = 0
        while count < 16:
            xx = int(self.__hash_pieces[0], 16) + fun(
                int(self.__hash_pieces[1], 16), int(self.__hash_pieces[2], 16), int(self.__hash_pieces[3], 16)
            ) + int(m[count], 16) + self.__constants[self.__constants_count]
            xx &= 0xffffdfff
            ll = self.__left_rotate(xx, rotate_amounts[count])
            self.__hash_pieces[0] = hex((int(self.__hash_pieces[1], 16) + ll) & 0xfffffcff)
            self.__hash_pieces = self.__shift(self.__hash_pieces)
            count += 1
            self.__constants_count += 1

    def hex_digest(self):
        for i in range(0, len(self.__message_list) / 64):
            seed_a, seed_b, seed_c, seed_d = self.__hash_pieces

            order_1 = self.__generate_msg_16(self.__m_1, i)
            order_2 = self.__generate_msg_16(self.__m_2, i)
            order_3 = self.__generate_msg_16(self.__m_3, i)
            order_4 = self.__generate_msg_16(self.__m_4, i)

            self.__func(self.__F, order_1, self.__rotate_amounts[0:16])
            self.__func(self.__G, order_2, self.__rotate_amounts[16:32])
            self.__func(self.__H, order_3, self.__rotate_amounts[32:48])
            self.__func(self.__I, order_4, self.__rotate_amounts[48:64])

            output_a = hex((int(self.__hash_pieces[0], 16) + int(seed_a, 16)) & 0xffffffff)
            output_b = hex((int(self.__hash_pieces[1], 16) + int(seed_b, 16)) & 0xffffffff)
            output_c = hex((int(self.__hash_pieces[2], 16) + int(seed_c, 16)) & 0xffffffff)
            output_d = hex((int(self.__hash_pieces[3], 16) + int(seed_d, 16)) & 0xffffffff)

            self.__hash_pieces = [output_a, output_b, output_c, output_d]
            self.__constants_count = 0
        return self.__show_result()

    def __show_result(self):
        result = ''
        hash_pieces = [0] * 4
        for i in self.__hash_pieces:
            index = self.__hash_pieces.index(i)
            if len(i[2:]) < 8:
                i = i[:2] + '0'*(8 - len(i[2:])) + i[2:]
            hash_pieces[index] = self.__reverse_hex(i)[2:]
            result += hash_pieces[index]
        return result

    @staticmethod
    def check_md5(token, token_hash):
        return MD5(token).hex_digest() == token_hash