from Crypto.Hash import SHA256
from Crypto.Cipher import DES

password = 'jazz-all'
des = DES.new('01234567', DES.MODE_ECB)
on_password_DES = des.encrypt(password)
print on_password_DES

validation = raw_input('ingrese password')

if validation == des.decrypt(on_password_DES):
    print 'yes'
else:
    print 'not'
