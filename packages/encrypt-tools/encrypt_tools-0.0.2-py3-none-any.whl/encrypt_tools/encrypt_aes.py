from base64 import b64encode, b64decode

from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class CryptoAes(object):

    def encrypt(self, message, key, iv):
        """
           :params message: String
           :params key: String Bytes
           :params iv: String Bytes
           Returns: String
        """
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        enc = cipher.encrypt(raw)
        return b64encode(enc).decode('utf-8')

    def decrypt(self, encrypted_data, key, iv):
        """
           :params encrypted_data: String
           :params key: String Bytes
           :params iv: String Bytes
           Returns: String
        """
        encrypted_data = b64decode(encrypted_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = cipher.decrypt(encrypted_data)
        return unpad(dec).decode('utf-8')
