# Car Monitoring Blockchain System

A comprehensive vehicle monitoring system that leverages blockchain technology to securely track and store vehicle state data. This project demonstrates how blockchain can be applied to ensure data integrity in automotive diagnostics and maintenance systems.

## Overview

This system consists of a vehicle simulator interface and a blockchain backend that records vehicle parameters over time, providing an immutable record of a vehicle's history. The system is designed for educational purposes to showcase blockchain concepts applied to real-world scenarios.

## Features

- **Vehicle State Simulation**: Simulate various vehicle conditions including tire pressure, engine temperature, battery status, oil level, brake wear, fuel level, and fault detection
- **Dual Vehicle Monitoring**: Track and compare state data for two different vehicles simultaneously
- **Blockchain Data Storage**: All vehicle state changes are recorded in a secure, tamper-proof blockchain
- **Historical Data Retrieval**: View the complete history of a vehicle's state changes
- **Date Filtering**: Filter historical data by specific dates
- **Blockchain Integrity Verification**: Verify that the blockchain has not been tampered with
- **Real-time Updates**: Vehicle state changes are immediately recorded to the blockchain

## Technologies Used

- **Backend**: Python with Flask for the blockchain server
- **Frontend**: HTML, CSS, and JavaScript for the vehicle simulator
- **Blockchain Implementation**: Custom blockchain implementation with SHA-256 hashing
- **Data Storage**: JSON-based persistent storage for the blockchain

## Installation and Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/car-monitoring-blockchain.git
cd car-monitoring-blockchain
```

2. Install required Python packages
```bash
pip install flask flask_cors
```

3. Start the blockchain server
```bash
python Blockchain.py
```

4. Open the Car.html file in your browser
```bash
# Simply open the file in your web browser or use a local server
```

## Project Structure

- `Blockchain.py`: The backend server that implements the blockchain and provides API endpoints
- `Car.html`: The frontend interface for simulating vehicle states and viewing blockchain data
- `car_blockchain.json`: The file where blockchain data is persistently stored

## How It Works

1. The blockchain server starts and either loads an existing blockchain from disk or creates a new one with a genesis block
2. The web interface simulates two vehicles with various parameters (pressure, temperature, battery status, etc.)
3. When vehicle parameters change, the data is sent to the blockchain server
4. The server creates a new block containing the vehicle data and adds it to the chain
5. Users can view the history of any vehicle, filtered by date if desired
6. The integrity of the blockchain can be verified at any time

## API Endpoints

- `POST /add_car_data`: Add new vehicle state data to the blockchain
- `GET /get_car_history/<car_id>`: Get the complete history for a specific vehicle (can be filtered by date)
- `GET /get_all_blocks`: Get all blocks in the blockchain
- `GET /validate_chain`: Verify the integrity of the blockchain
- `GET /status`: Get the current status of the blockchain server

## Use Cases

- **Vehicle Service Centers**: Track maintenance history with tamper-proof records
- **Fleet Management**: Monitor vehicle conditions over time with secure data storage
- **Insurance Companies**: Access reliable vehicle history for claims processing
- **Vehicle Owners**: Maintain a trusted record of vehicle maintenance and conditions
- **Educational Tool**: Learn about blockchain technology with a practical application

## Future Enhancements

- Add user authentication and authorization
- Implement a distributed blockchain with peer-to-peer networking
- Create a more sophisticated consensus algorithm
- Add more advanced data visualization tools
- Develop a mobile application for remote vehicle monitoring

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
