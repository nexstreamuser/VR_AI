import socket
import threading
import pyaudio

AWS_IP = ""
AWS_PORT = 5000

class AudioClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.chunk_size = 4096
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(format=self.format,
                                             channels=self.channels,
                                             rate=self.rate,
                                             input=True,
                                             frames_per_buffer=self.chunk_size)
        self.output_stream = self.audio.open(format=self.format,
                                              channels=self.channels,
                                              rate=self.rate,
                                              output=True,
                                              frames_per_buffer=self.chunk_size)

    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Connected to server.")
            threading.Thread(target=self.send_audio).start()
            threading.Thread(target=self.receive_audio).start()
        except Exception as e:
            print(f"Failed to connect: {e}")
            self.cleanup()

    def send_audio(self):
        try:
            while True:
                data = self.input_stream.read(self.chunk_size)
                self.client_socket.sendall(data)
        except Exception as e:
            print(f"Error sending audio: {e}")
            self.cleanup()

    def receive_audio(self):
        try:
            while True:
                data = self.client_socket.recv(self.chunk_size)
                self.output_stream.write(data)
        except Exception as e:
            print(f"Error receiving audio: {e}")
            self.cleanup()

    def cleanup(self):
        print("Closing streams and terminating PyAudio.")
        self.input_stream.stop_stream()
        self.output_stream.stop_stream()
        self.input_stream.close()
        self.output_stream.close()
        self.audio.terminate()
        self.client_socket.close()

if __name__ == "__main__":
    client = AudioClient(AWS_IP, AWS_PORT)
    client.connect()
