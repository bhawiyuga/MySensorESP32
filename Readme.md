# ESP32 Client-Server WiFi Demo

This project consists of an ESP32 client that reads sensor data and sends it to a Python-based server over HTTPS. The project is structured using the PlatformIO directory structure, and the server is located in the `server` directory. This guide will walk you through setting up both the client and server environments.

## Table of Contents

- [Preparing the Client](#preparing-the-client)
- [Preparing the Server](#preparing-the-server)

## Preparing the Client

### Prerequisites

Before you begin, ensure you have the following installed:

- [PlatformIO](https://platformio.org/install) (PlatformIO IDE or PlatformIO Core)
- ESP32 development board

### Project Structure

Your PlatformIO project should have a structure similar to this:

```
.
├── include
├── lib
├── src
│   └── main.cpp
├── platformio.ini
└── server
    ├── server.py
    └── requirements.txt
```

### Installing Dependencies

1. **Clone the Repository** (if you haven’t already):

   ```sh
   git clone https://github.com/bhawiyuga/MySensorESP32.git
   cd MySensorESP32
   ```

2. **Install ArduinoJson Library**:

   The `ArduinoJson` library is required for parsing and generating JSON data on the ESP32.

   Open the `platformio.ini` file and ensure the following is added under your environment section (e.g., `[env:esp32dev]`):

   ```ini
    [env:ttgo-t-oi-plus]
    platform = espressif32
    board = ttgo-t-oi-plus
    framework = arduino

    lib_deps =
        bblanchon/ArduinoJson @ ^7.1.0
   ```

   When you build the project, PlatformIO will automatically download and install this library.

### Configuring the Client

1. **Configure Wi-Fi Credentials**:

   In your `src/main.cpp`, update the following lines with your Wi-Fi network credentials:

   ```cpp
   const char* ssid = "your_SSID";
   const char* password = "your_PASSWORD";
   ```

2. **Update Server URL**:

   Ensure the server URL in `main.cpp` matches the address where your Python server will be hosted:

   ```cpp
   const char* serverName = "https://your-server.com/api/endpoint";
   ```

3. **Build and Upload**:

   After configuring the client code:

   ```sh
   platformio run --target upload
   ```

   This command will compile and upload the firmware to your ESP32.

### Running the Client

Once the firmware is uploaded, your ESP32 will automatically connect to the specified Wi-Fi network and start sending sensor data to the server at regular intervals.

## Preparing the Server

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
- [virtualenv](https://pypi.org/project/virtualenv/) (recommended but not mandatory)

### Setting Up the Server

1. **Navigate to the Server Directory**:

   ```sh
   cd server
   ```

2. **Create and Activate a Virtual Environment** (optional but recommended):

   ```sh
   python -m venv .venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Required Packages**:

   Install the necessary Python packages using the `requirements.txt` file:

   ```sh
   pip install -r requirements.txt
   ```

4. **(Optional) Generate SSL Certificates** (for HTTPS):

   You can generate a self-signed SSL certificate using OpenSSL:

   ```sh
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```

   Place the `cert.pem` and `key.pem` files in the `server` directory.

5. **Run the Server**:

   Start the server with HTTPS:

   ```sh
   python server.py
   ```

   The server will listen for incoming HTTPS POST requests from the ESP32 client on port 5000.

### Accessing the Server

- **Data Submission Endpoint**: The ESP32 client will send data to `https://your-server-ip:5000/api/endpoint`.
- **View Data**: You can access the stored data by navigating to `https://your-server-ip:5000/api/data`.

### Troubleshooting

If you encounter SSL certificate warnings when accessing the server, this is expected behavior when using a self-signed certificate. You can bypass these warnings for testing purposes.

---

This `README.md` provides the necessary steps to set up and run both the client and server components of your project. Adjust paths, names, and configurations according to your specific project setup.
