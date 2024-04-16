import random


def _pad_for_encryption(s, target_length):
    max_msglength = target_length - 11
    msglength = len(s)
    padding = b''
    padding_length = target_length - msglength - 3
    for i in range(padding_length):
        padding += b'\x00'
    return b''.join([b'\x00\x00',padding,b'\x00', s])


def encrypt(s, pub_key):
    import rsa
    import binascii
    keylength = rsa.common.byte_size(pub_key.n)
    padded = _pad_for_encryption(s, keylength)
    payload = rsa.transform.bytes2int(padded)
    encrypted = rsa.core.encrypt_int(payload, pub_key.e, pub_key.n)
    encrypted = rsa.transform.int2bytes(encrypted, keylength)
    encrypted = binascii.b2a_hex(encrypted).decode()
    return encrypted


def getScriptSessionId():
    _origScriptSessionId = "8A22AEE4C7B3F9CA3A094735175A6B14"
    return _origScriptSessionId + str(int(1000 * random.random()))