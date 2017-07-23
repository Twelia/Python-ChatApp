from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import hashlib, base64

class AESCipher:
    BS = 16
    pad = lambda s: s+(BS-len(s)%BS)*chr(BS-len(s)%BS)
    unpad = lambda s: s[0:-ord(s[-1])]

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.base64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))