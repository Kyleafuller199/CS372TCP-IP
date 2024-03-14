import socket
import threading
import json
import time

class ManagementService:
    def __init__(self, unique_identifier, listening_ip, listening_port):
        self.unique_identifier = unique_identifier
        self.listening_ip = listening_ip
        self.listening_port = listening_port
        self.clients = {}  # Dictionary to store connected monitoring services and sockets
        self.client_lock = threading.Lock()
        self.connected = False

    def start(self):
        # Continuously attempt to listen for connections
        while True:
            if not self.connected:
                self.start_listening()

            time.sleep(5)  # Wait for 5 seconds before attempting to listen again

    def start_listening(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as management_socket:
                management_socket.bind((self.listening_ip, self.listening_port))
                management_socket.listen()

                print(f"Management Service '{self.unique_identifier}' is listening for connections.")

                while True:
                    client_socket, client_address = management_socket.accept()
                    threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        except OSError as e:
            print(f"Error: {e}")

    def handle_client(self, client_socket, client_address):
        with self.client_lock:
            self.clients[client_address] = client_socket

        print(f"Connected to monitoring service at {client_address}")

        try:
            # Generate monitoring tasks with a random delay before sending
            tasks = self.generate_monitoring_tasks_with_delay()
            self.send_tasks(client_socket, tasks)

            # Receive results from monitoring service
            results = self.receive_results(client_socket)
            print(f"Received results from monitoring service at {client_address}: {results}")

            # Validate received results
            self.validate_results(client_address, results)

        except ConnectionAbortedError:
            print(f"The connection was unexpectedly lost by the monitoring service at {client_address}.")
            with self.client_lock:
                del self.clients[client_address]  # Remove the disconnected client
            self.connected = False  # Set connected to False to attempt reconnect
        except ConnectionResetError:
            print(f"Lost connection with the monitoring service at {client_address}. Attempting to reconnect...")
            with self.client_lock:
                del self.clients[client_address]  # Remove the disconnected client
            self.connected = False  # Set connected to False to attempt reconnect
            time.sleep(5)

        # Close the connection
        client_socket.close()

    def generate_monitoring_tasks_with_delay(self):
        # Hardcoded example tasks
        tasks = {
            1: {"service_type": "HTTP", "parameters": {"url": "http://example.com", "port": 80}, "frequency": 60},
            2: {"service_type": "HTTPS", "parameters": {"url": "https://example.com", "port": 443}, "frequency": 120}
        }

        # Generate a random delay between 10 to 15 seconds
        delay = 5
        print(f"Rechecking connection in {delay} seconds...")
        time.sleep(delay)

        return tasks

    def send_tasks(self, client_socket, tasks):
        tasks_json = json.dumps(tasks)
        client_socket.sendall(tasks_json.encode())

    def receive_results(self, client_socket):
        data = client_socket.recv(1024)
        return json.loads(data.decode())

    def validate_results(self, client_address, results):
        # Placeholder for result validation logic
        pass

if __name__ == "__main__":
    management_service = ManagementService("Manager1", "127.0.0.1", 8888)  # Example unique identifier and listening IP/port
    management_service.start()
