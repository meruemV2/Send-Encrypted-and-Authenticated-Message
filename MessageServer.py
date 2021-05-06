import socketserver
import hmac, hashlib
import Encryption


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request	is	the	TCP	socket	connected	to	the	client

        def verify(msg, sig):
            secret = b'1234'
            computed_sha = hmac.new(secret, msg,
                                    digestmod=hashlib.sha3_512).digest()
            if sig != computed_sha:
                return False
            else:
                return True

        self.data = self.request.recv(1024).strip()
        print("{}	sent message:	".format(self.client_address[0]))

        sentMessage = self.data
        messageEncrypted = sentMessage[:len(sentMessage) - 64]

        message = bytes(Encryption.cipher.decrypt(messageEncrypted), encoding='utf-8')
        tag = self.data[-64:]

        if verify(message, tag):
            print("message received = ", message)
        else:
            print("Unauthenticated message received! Be on alert! Watch out for bad guys !!")

        print(self.data)


if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 8888
        # Create	the	server,	binding	to	localhost	on	port	9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # Activate	the	server;	this	will	keep	running	until	you
        # interrupt	the	program	with	Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:", e)
        exit(1)
    finally:
        server.close()
