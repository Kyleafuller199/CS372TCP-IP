import socket
import json
import time

class MonitoringService:
    def __init__(self, unique_identifier, management_ip, management_port):
        self.unique_identifier = unique_identifier
        self.management_ip = management_ip
        self.management_port = management_port
        self.connected = False

    def start(self):
        while True:
            if not self.connected:
                self.connect_to_management_service()

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as management_socket:
                    management_socket.connect((self.management_ip, self.management_port))
                    self.connected = True

                    # Receive monitoring tasks from management service
                    tasks = self.receive_tasks(management_socket)
                    print(f"Received tasks from management service: {tasks}")

                    # Perform monitoring
                    results = self.perform_monitoring(tasks)
                    print(f"Monitoring results: {results}")

                    # Send results back to management service
                    self.send_results(management_socket, results)
            except ConnectionRefusedError:
                print("Connection to management service refused. Retrying in 5 seconds...")
                self.connected = False
                time.sleep(5)
            except ConnectionResetError:
                print("Lost connection with the management service. Attempting to reconnect...")
                self.connected = False

    def connect_to_management_service(self):
        print("Attempting to connect to the management service...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as management_socket:
                management_socket.connect((self.management_ip, self.management_port))
                self.connected = True
                print("Connected to the management service.")
        except ConnectionRefusedError:
            print("Connection to management service refused. Retrying in 5 seconds...")
            time.sleep(5)

    def receive_tasks(self, management_socket):
        data = management_socket.recv(1024)
        return json.loads(data.decode())

    def perform_monitoring(self, tasks):
        # Placeholder for monitoring tasks
        results = {}
        for task_id, task_details in tasks.items():
            # Perform monitoring and populate results
            result = {"task_id": task_id, "status": "Online"}
            results[task_id] = result
        return results

    def send_results(self, management_socket, results):
        results_with_id = {"unique_identifier": self.unique_identifier, "results": results}
        results_json = json.dumps(results_with_id)
        management_socket.sendall(results_json.encode())

if __name__ == "__main__":
    monitoring_service1 = MonitoringService("Moni1", "127.0.0.1", 8888)  # First monitoring service
    monitoring_service1.start()

    monitoring_service2 = MonitoringService("Moni2", "127.0.0.1", 8889)  # Second monitoring service
    monitoring_service2.start()
