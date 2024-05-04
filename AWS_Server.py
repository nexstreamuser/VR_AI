import socket
import threading

class AudioServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chunk_size = 4096
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def start(self):
        self.server_socket.listen(3)
        print("Server listening on {}:{}".format(self.host, self.port))
        while True:
            conn, addr = self.server_socket.accept()
            print("Connected to client:", addr)
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(self.chunk_size)
                if not data:
                    break
                self.broadcast(data, conn)
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            self.remove_client(conn)
            conn.close()

    def broadcast(self, data, sender_conn):
        for client_conn in self.clients:
            if client_conn != sender_conn:
                try:
                    client_conn.sendall(data)
                except Exception as e:
                    print(f"Error broadcasting to a client: {e}")

    def remove_client(self, conn):
        if conn in self.clients:
            self.clients.remove(conn)
            print("Client disconnected.")

    def stop(self):
        print("Closing server.")
        self.server_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    server = AudioServer(host, port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
