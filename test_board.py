data = (
    1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1,
    0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0,
    1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0,
    0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
    0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
    1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
    0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0,
    1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1,
    0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1,
    1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1,
    1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1,
    0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1,
    1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1,
    0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1,
    1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
)


def num2bits(num, bitlength):
    bits = []
    for i in range(bitlength):
        bits.append(num & 1)
        num >>= 1
    return bits


def bits2num(bits):
    num = 0
    for i, x in enumerate(bits):
        assert x == 0 or x == 1
        num += (x << i)
    return num


class KATAN():
    def __init__(self, master_key=0, version=32):
        assert version in (32, 48, 64)
        self.version = version

        if 32 == self.version:
            self.len_l1 = 13
            self.len_l2 = 19
            self.X = (None, 12, 7, 8, 5, 3)
            self.Y = (None, 18, 7, 12, 10, 8, 3)
        elif 48 == self.version:
            self.len_l1 = 19
            self.len_l2 = 29
            self.X = (None, 18, 12, 15, 7, 6)
            self.Y = (None, 28, 19, 21, 13, 15, 6)
        else:
            self.len_l1 = 25
            self.len_l2 = 39
            self.X = (None, 24, 15, 20, 11, 9)
            self.Y = (None, 38, 25, 33, 21, 14, 9)

        self.key = num2bits(master_key, 80)

        for i in range(80, 2 * 254):
            self.key.append(self.key[i - 80] ^ self.key[i - 61] ^ self.key[i - 50] ^ self.key[i - 13])

    def one_round_enc(self, round):
        self.f_a = self.l1[self.X[1]] ^ self.l1[self.X[2]] \
                   ^ (self.l1[self.X[3]] & self.l1[self.X[4]]) \
                   ^ (self.l1[self.X[5]] & data[round]) \
                   ^ self.key[2 * round]

        self.f_b = self.l2[self.Y[1]] ^ self.l2[self.Y[2]] \
                   ^ (self.l2[self.Y[3]] & self.l2[self.Y[4]]) \
                   ^ (self.l2[self.Y[5]] & self.l2[self.Y[6]]) \
                   ^ self.key[2 * round + 1]

        self.l1.pop()
        self.l1.insert(0, self.f_b)

        self.l2.pop()
        self.l2.insert(0, self.f_a)

    def enc(self, plaintext, from_round=0, to_round=253):
        self.plaintext_bits = num2bits(plaintext, self.version)
        self.l2 = self.plaintext_bits[:self.len_l2]
        self.l1 = self.plaintext_bits[self.len_l2:]

        for round in range(from_round, to_round + 1):
            self.one_round_enc(round)
            if self.version > 32:
                self.one_round_enc(round)
                if self.version > 48:
                    self.one_round_enc(round)
        return bits2num(self.l2 + self.l1)

    def one_round_dec(self, round):
        self.f_a = self.l2[0] ^ self.l1[self.X[2] + 1] \
                   ^ (self.l1[self.X[3] + 1] & self.l1[self.X[4] + 1]) \
                   ^ (self.l1[self.X[5] + 1] & data[round]) \
                   ^ self.key[2 * round]

        self.f_b = self.l1[0] ^ self.l2[self.Y[2] + 1] \
                   ^ (self.l2[self.Y[3] + 1] & self.l2[self.Y[4] + 1]) \
                   ^ (self.l2[self.Y[5] + 1] & self.l2[self.Y[6] + 1]) \
                   ^ self.key[2 * round + 1]

        self.l1.pop(0)
        self.l1.append(self.f_a)

        self.l2.pop(0)
        self.l2.append(self.f_b)

    def dec(self, ciphertext, from_round=253, to_round=0):
        self.ciphertext_bits = num2bits(ciphertext, self.version)
        self.l2 = self.ciphertext_bits[:self.len_l2]
        self.l1 = self.ciphertext_bits[self.len_l2:]

        for round in range(from_round, to_round - 1, -1):
            self.one_round_dec(round)
            if self.version > 32:
                self.one_round_dec(round)
                if self.version > 48:
                    self.one_round_dec(round)
        return bits2num(self.l2 + self.l1)


if __name__ == '__main__':
    key = 0xFFFFFFFFFFFFFFFFFFFF
    plaintext = 0x00000000

    myKATAN = KATAN(key)

    print('key =', hex(key))
    print('plain =', hex(plaintext))

    encrypted = myKATAN.enc(plaintext)
    print('encrypted =', hex(encrypted))
    decrypted = myKATAN.dec(encrypted)
    print('decrypted =', hex(decrypted))
