# CS372TCP-IP

# Management and Monitoring Services

This repository contains the source code for Management and Monitoring services implemented in Python using socket programming.

## Prerequisites

- Python 3.x
- Basic understanding of socket programming

## Installation

1. Clone the repository to your local machine:


2. Navigate to the project directory:


3. Install the required dependencies using pip:


## Usage

### Management Service

1. Open a terminal or command prompt.

2. Navigate to the `management` directory:


3. Run the management service:


### Monitoring Service

1. Open another terminal or command prompt.

2. Navigate to the `monitoring` directory:


3. Run the monitoring service:


## Configuration

### Management Service

- The Management Service listens on port 8888 by default. You can change this port by modifying the `listening_port` variable in `management.py`.

### Monitoring Service

- The Monitoring Service connects to the Management Service on port 8888 by default. You can change this port and IP address by modifying the `management_ip` and `management_port` variables in `monitoring.py`.

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
