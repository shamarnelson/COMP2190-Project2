import socket
import AES
import random
import RSA

PORT = 7000
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

client = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    client.send(bytes(msg,FORMAT))

def getConCode():
    """Prompts the Agent to enter connection code and returns said code"""
    connCode = input("Enter Connection Code - ")
    return connCode

def getAnswer(question):
    print(question)
    answer = input("Enter Answer To secret Question - ")
    return answer

def computeSessionKey(n):
	"""Computes this node's session key"""
	sessionKey = random.randint(1, n-10)
	return sessionKey

def receive():
    response = client.recv(1024).decode(FORMAT)
    return response

# Write Code that allows the Client to send a "100 Hello" message to the Server.
"""Your Code here."""
msg = "100 Hello"
send(msg)

# Write Code that allows the Client to receive the server's public key and a nonce (e,n and nonce).
"""Your Code here."""
msg = receive().split(" ")
e = int(msg[0])
n = int(msg[1])
nonce = int(msg[2])
print(f"Server's Public key (e, n) : ({e}, {n})")

# Write Code that allows the Client to compute the Symmetric Key.
"""Your Code here."""
sessionKey = computeSessionKey(n)
print(f"Session Key: {sessionKey}")


# Write Code that allows the Client to encrypt the compted session key using the server's public key.
"""Your Code here."""
eKey = RSA.RSAencrypt(sessionKey, e, n)

# Write Code that allows the Client to send a "103 Session Key" message and the computed session Key to the Server.
"""Your Code here."""
msg = f"103 Session Key {eKey}"
send(msg)

# Write Code to set up the Agent's Symmetric Key.
AES.keyExp(sessionKey)

# Write Code that allows the Agent's to send the nonce (encrypted with the Agent's symmetric key) to the server.
"""Your Code here."""
msg = str(AES.encrypt(nonce))
send(msg)

# Write Code that allows the Client to receive the server's "200 ok" message.
"""Your Code here."""
msg = receive()
if not "OK" in msg:
    print("Closing socket connection")
    client.close()
    sys.exit("Handshake failed")

# Write Code that allows the Client to send its encrypted connection code.
"""Your Code here."""
code = getConCode()
msg = AES.encryptMessage(AES.strToASCI(code))
send(msg)

# Write Code that allows the Client to receive the server's encrypted secret question.
"""Your Code here."""
msg = AES.decryptMessage(receive())
if msg == None or msg == "" or len(msg) == 0:
    print("Closing socket connection")
    client.close()
    sys.exit("Wrong code supplied.")

answer = getAnswer(msg)

# Write Code that allows the Client to send its encrypted answer to the server.
"""Your Code here."""
msg = AES.encryptMessage(AES.strToASCI(answer))
send(msg)

# Write Code that allows the Client to receive the server's encrypted welcome message.
msg = AES.decryptMessage(receive())
if msg == None or msg == "" or len(msg) == 0:
    print("Closing socket connection")
    client.close()
    sys.exit("Wrong answer supplied.")

print(msg)
client.close()

# AJK782975 - Agent A
# AJK786144 - Agent B
