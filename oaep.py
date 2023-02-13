from hashlib import sha3_256, sha3_512
import random


class OAEP():
    size = 0
    #P1 = msg_padded = msg_len + padding_size = 768
    padding_size = 0
    P2_size = 256
    #P1 + P2 = 1024

    def __init__(self, size):
        self.size = size

    def padding(self, m):
        msg_padded_bits = m
        msg_padded_bits <<= self.padding_size
        return msg_padded_bits

    def unpadding(self, m_padded):
        m_bits = int(m_padded)
        m_bits >>= self.padding_size
        return m_bits
    
    def define_padding_size(self, msg_size):
        self.padding_size = self.size - self.P2_size - msg_size

    def oaep_mask(self, m):
        P1_bl = 0 #P1 bit length
        P2_bl = 0 #P2 bit length
        self.define_padding_size(len(str(m)))
        m_padded_bits = self.padding(m)
        r = random.getrandbits(self.P2_size) #Número aleatório r de 256 bits
        G = sha3_512(str.encode(str(r))).hexdigest() + sha3_256(str.encode(str(r))).hexdigest()
        P1 = m_padded_bits ^ int(G, 16)

        H = sha3_256(str.encode(str(P1))).hexdigest()

        P2 = int(H, 16) ^ r

        P1_bl = len(str(P1))
        P2_bl = len(str(P2))
        return int(str(P1)+str(P2)), P1_bl

    def oaep_unmask(self, m_masked, P1_Size):
        m_masked = str(m_masked)
        P1 = m_masked[:P1_Size]
        P2 = m_masked[P1_Size:]
        H = sha3_256(str.encode(P1)).hexdigest()
        r = int(P2) ^ int(H, 16)
        
        G = sha3_512(str.encode(str(r))).hexdigest() + sha3_256(str.encode(str(r))).hexdigest()
        m_padded = int(P1) ^ int(G, 16)
        m_bits = self.unpadding(m_padded)

        return m_bits