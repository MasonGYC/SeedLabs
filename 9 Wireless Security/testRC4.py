from skeleton import *
import unittest

#     Several test cases: (to test RC4 implementation only)
#     1. key = '1A2B3C', cipertext = '00112233' -> plaintext = '0F6D13BC'
#     2. key = '000000', cipertext = '00112233' -> plaintext = 'DE09AB72'
#     3. key = '012345', cipertext = '00112233' -> plaintext = '6F914F8F'

def crack(key, ciphertext):
    keystream = RC4(key)
    plaintext = ""
    for i in ciphertext:
        plaintext += ('{:02X}'.format(i ^ next(keystream)))
    return plaintext

class TestRC4(unittest.TestCase):
    ciphertext = binascii.unhexlify("00112233") 

    def test1(self):
        key =binascii.unhexlify("1A2B3C") 
        plaintext = crack(key,self.ciphertext)
        self.assertEqual(plaintext, '0F6D13BC', f"Plaintext should be 0F6D13BC")

    def test2(self):
        key =binascii.unhexlify("000000") 
        plaintext = crack(key,self.ciphertext)
        self.assertEqual(plaintext, 'DE09AB72', f"Plaintext should be DE09AB72")

    def test3(self):
        key =binascii.unhexlify("012345") 
        plaintext = crack(key,self.ciphertext)
        self.assertEqual(plaintext, '6F914F8F', f"Plaintext should be 6F914F8F")

if __name__ == '__main__':
    unittest.main()
