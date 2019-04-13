import os
import numpy as np
import binascii
from Crypto.Cipher import AES

def pad(text):
    while len(text) % 16 != 0:
        text += '\0'
    return text
def encrp(key,fi):
    aes = AES.new(key, AES.MODE_ECB)
    fr = open(fi,'rb')
    fw = open(fi+'.en', 'wb')
    block_sz = 512
    while True:
        buffer = fr.read(block_sz)
        if not buffer:
            break
        # TODO encryption without doubled volume
        buffer = buffer.hex()   
        buffer = pad(buffer)
        buffer = aes.encrypt(buffer) 
        fw.write(buffer)
    fr.close()
    fw.close()

def decrp(key,fi):
    aes = AES.new(key, AES.MODE_ECB)
    fr = open(fi, 'rb')
    fn = fi.split(".en")[0] + '.de' 
    fw = open(fn, 'wb')
    print(fi,fn)
    block_sz = 512
    while True:
        buffer = fr.read(block_sz)
        if not buffer:
            break
        buffer = aes.decrypt(buffer).decode() # bytes to str
        buffer = buffer.rstrip('\0')
        buffer = binascii.a2b_hex(buffer)
        fw.write(buffer)
    fr.close()
    fw.close()

def keybox(key,fi):
   key_hex = key.hex()
   f = open('keybox.'+ fi +'.key', 'w')
   f.write(key_hex)
   f.close()

def main():
    mode = input('encrypt or decrypt? (enter "e" or "d") \n')
    if (mode == 'e'):
        fi = input('enter the file name:\n')
        # random bytes
        key = np.random.bytes(16)
        try:
            encrp(key,fi)
            keybox(key,fi)
            print ('Successfully encypted!')
        except:
            print('A error has occured!')
            input('Enter to exist...')
    elif (mode == 'd'):
        fi = input('enter the file name:\n')
        itor = os.scandir(os.getcwd())
        lst = []
        for entry in itor:
            if entry.name.split('.')[-1] == 'key':
                lst.append(entry.name)
        print(lst[0])
        f = open(lst[0],'r')
        key = f.read(512)
        if (len(key) == 32):
            key = binascii.a2b_hex(key)
            try:
                decrp(key,fi)
                print('Successfully decypted!')
            except:
                print('A error has occured!')
                input('Enter to exist...')   
            finally:
                f.close()             
        else: 
            print(len(key))
            print('A 16 bytes key is neccessary!')
            input('Enter to exist...')
    else:
        print('incorrect input!')
        input('Enter to exist...')

if __name__ == '__main__':
    main()

        


