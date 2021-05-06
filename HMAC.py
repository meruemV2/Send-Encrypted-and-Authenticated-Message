import hmac, hashlib
import Encryption

#sender
body = b'test Message...'
print("Orig message = ",body)
bodyEncrypted = Encryption.cipher.encrypt(body)
print("Orig message encrypted = ",bodyEncrypted)

secret = b'1234'

computedSig = hmac.new(secret, body,
                    digestmod=hashlib.sha3_512).digest()
print("tag of message=",computedSig)
print("length of tag of message=",len(computedSig))
sentMessage = bodyEncrypted+computedSig
print("sent message=",sentMessage)

"""
#reciever Authenticated sender
def verify(msg,sig):
    secret = b'1234'
    computed_sha = hmac.new(secret,
                            msg,
                            digestmod=hashlib.sha3_512).digest()
    if sig != computed_sha:
        return False
    else:
        return True


messageEncrypted = sentMessage[:len(sentMessage)-64]
message  = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
tag =sentMessage[-64:]

if verify(message, tag):
    print("message received = ",message)
else:
    print("unauthenticated message")

"""



#reciever Unauthenticated sender
def verify(msg,sig):
    secret = b'12345'
    computed_sha = hmac.new(secret,
                            msg,
                            digestmod=hashlib.sha3_512).digest()
    if sig != computed_sha:
        return False
    else:
        return True


messageEncrypted = sentMessage[:len(sentMessage)-64]
message  = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
message = message+b'added letters'
tag =sentMessage[-64:]

if verify(message, tag):
    print("message received = ",message)
else:
    print("unauthenticated message")
