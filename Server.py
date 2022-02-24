from math import e
import socket
import datetime as dt
import threading
import RSA
import AES
import Verify as av

PORT = 7000 
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def clientHelloResp(n, e):
    """Responds to client's hello message with modulus and exponent"""
    status = "101 Hello "+ str(n) + " " + str(e)
    return status

def SessionKeyResp(nonce):
    """Responds to session key with nonce"""
    status = "120 Nonce "+ str(nonce)
    return status

def clientHandler(conn, addr, state):
    print(f"[NEW CONNCETION] {addr} connected.")

    n = int(state["n"])
    e = int(state["e"])
    d = int(state["d"])

    
    while True:
        #Receive hello message "100 Hello" from Agent
        print(conn.recv(1024).decode()) 

        #Send public key and nonce to Agent "e n nonce"
        stateInfo = ""+str(e)+" "+str(n)+" "+str(state["nonce"]) #(2)
        conn.send(bytes(stateInfo,FORMAT))

        print(stateInfo)

        #Receive Session key message "103 Session Key" from Agent and Encrypted Symmetric 
        # Key from Agent "SymmKey"
        sess = conn.recv(1024).decode().split()
        e_SymmKey = int(sess[-1])
        d_SymmKey = RSA.RSAdecrypt(int(e_SymmKey),d,n) #(2)
        print(f"sess - {sess}")
        print(f"e_SymmKey - {e_SymmKey}")
        print(f"d_SymmKey - {d_SymmKey}")
        state["SymmKey"] = d_SymmKey

        #Receive nonce Encrypted with Symmetric key
        e_nonce = conn.recv(1024).decode()
        j = state["nonce"]
        print(f"nonce - {j}")
        print(f"e_nonce - {e_nonce}")
        AES.keyExp(d_SymmKey)
        decypted_nonce = AES.decrypt(int(e_nonce)) #(1)
        print(f"decypted_nonce - {decypted_nonce}")

        #Check nonce
        if(decypted_nonce == int(state["nonce"])):
            print("Correct Nonce")
            #Send "200 OK" to Agent
            conn.send(bytes("200 OK",FORMAT))

            #Receive encrypted connection code from Agent
            e_connCode = conn.recv(1024).decode()

            #decrypt Encrypted conn_code with AES
            connCode = AES.decryptMessage(e_connCode)

            print(f"e_conncode - {e_connCode}")
            print(f"connCode - {connCode}")

            agent_name = av.check_conn_codes(connCode)

            #Check connection code.
        
            if agent_name == -1:
                print("Invalid Connection Code!")
            else:
                #get random Secret question
                question = av.getSecretQuestion()
                #send encrypted secret question question to Agent
                ASCI_question = AES.strToASCI(question[0])
                e_question = AES.encryptMessage(ASCI_question)

                conn.send(bytes(e_question, FORMAT))
                print(f"question - {question}")
                print(f"e_question - {e_question}") 
                print(f"ASCI_question - {ASCI_question}") 

                #receive encrypted answer from agent
                e_ans = conn.recv(1024).decode()
                #decrypt encrypted answer
                ans = AES.decryptMessage(e_ans)

                print(f"e_ans - {e_ans}")
                print(f"ans - {ans}")

                #check answer.
                if ans == question[1]:
                    #Send Encrypted Welcome message to agent -> "Welcome Agent X"
                    dateNow = dt.datetime.now()
                    welcomeMessage = f"Welcome {agent_name} Time Logged - {dateNow}"
                    ASCI_welcomeMessage = AES.strToASCI(welcomeMessage)
                    e_welcomeMessage = AES.encryptMessage(ASCI_welcomeMessage)
                    conn.send(bytes(e_welcomeMessage, FORMAT))
                    print(welcomeMessage)
                else:
                    print("Invalid Answer")
        else:
            print("Invalid Nonce")
            connected = False

        connected = False
    conn.close()
    print(f"{addr} Connection Closed") 

def runServer():
    p = int(input('Enter P : '))
    q = int(input('Enter Q: '))
    n, e, d = RSA.genKeys(p, q)

    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")

    SymmKey = 1013	# Initializing symmetric key with a bogus value.
    nonce = RSA.generateNonce()

    state = {'nonce': nonce, 'n': n, 'e': e, 'd': d,'SymmetricKey': SymmKey}

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=clientHandler, args=(conn,addr,state) )
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.active_count() - 1}")

print("[STARTING] Server is Starting...")
runServer()
