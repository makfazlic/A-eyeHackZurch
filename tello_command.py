import socket

sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ("192.168.10.1",8889)
sock.bind(("", 9000))

while True:
    try:
        msg = input("Command: ")
        if not msg:
            break
        if "end" in msg:
            sock.close()
            break
        msg = msg.encode()
        sent = sock.sendto(msg, tello_address)
        response = sock.recv(1024)
        print("Return:", response.decode())
    except Exception as err:
        print("error")
        sock.close()
        break