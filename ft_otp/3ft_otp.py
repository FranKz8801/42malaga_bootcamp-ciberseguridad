import hmac
import hashlib
import struct
import time
import argparse
import os
from Crypto.Cipher import AES
import pyotp
import base64

def generate_totp(key, time_step=30, totp_length=6):
    time_now = int(time.time()) // time_step
    msg = struct.pack('>Q', time_now)
    h = hmac.new(key.encode(), msg, hashlib.sha1).digest()
    o = h[-1] & 0x0f
    h = (struct.unpack('>I', h[o:o+4])[0] & 0x7fffffff) % (10 ** totp_length)
    return str(h).zfill(totp_length)

def save_key(key):
    # Generar una clave para cifrar la clave maestra
    cipher_key = os.urandom(16)
    cipher = AES.new(cipher_key, AES.MODE_EAX)
    nonce = cipher.nonce

    # Cifrar la clave maestra
    ciphertext, tag = cipher.encrypt_and_digest(key.encode('utf-8'))

    # Guardar la clave cifrada y el nonce en un archivo
    with open('ft_otp.key', 'wb') as f:
        f.write(tag)
        f.write(cipher_key)
        f.write(nonce)
        f.write(ciphertext)

def load_key():
    # Cargar la clave cifrada y el nonce desde el archivo
    with open('ft_otp.key', 'rb') as f:
        tag = f.read(16)
        cipher_key = f.read(16)
        nonce = f.read(16)
        ciphertext = f.read()

    # Descifrar la clave maestra
    cipher = AES.new(cipher_key, AES.MODE_EAX, nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    # Devolver la clave maestra en formato bytes
    return plaintext

parser = argparse.ArgumentParser(prog='ft_otp')
subparsers = parser.add_subparsers(dest='command')

parser_g = subparsers.add_parser('g')
parser_g.add_argument('key')

parser_k = subparsers.add_parser('k')
parser_k.add_argument('keyfile')

args = parser.parse_args()

if args.command == 'g':
    if len(args.key) != 64 or not all(c in '0123456789abcdefABCDEF' for c in args.key):
        parser_g.error('key must be 64 hexadecimal characters')
    save_key(args.key)
    print('Key was successfully saved in ft_otp.key.')
elif args.command == 'k':
    key_hex = load_key().decode('utf-8')
    totp = generate_totp(key_hex)
    print(totp)
    print(pyotp.TOTP(base64.b32encode(key_hex.encode())).now())
