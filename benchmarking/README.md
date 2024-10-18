# 📊 System Evaluation and Load Testing

To evaluate the system's performance under different user loads, we provide a load testing tool based on the **Locust** package. This tool allows you to simulate multiple users interacting with the server, helping you to analyze and optimize the system’s performance.

---

## 🛠️ Installation

Ensure all necessary dependencies are installed by running:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Load Test

To start the load test, execute the following command:

```bash
locust -f locustfile.py --host=http://localhost:5000 --web-host=0.0.0.0
```

### Command Breakdown:
- `--host=http://localhost:5000`: Specifies the server URL to test. Replace `localhost:5000` with the actual host if your server is running elsewhere.
- `--web-host=0.0.0.0`: Allows access to the Locust web interface from any network interface.

Once the command is running, open your browser and navigate to:

```
http://<your-server-ip>:8089
```

This will open the **Locust web interface**, where you can configure the number of users and the spawn rate to simulate different user loads.

---

## ⚙️ Configuring the Load Test

In the **Locust web interface**, you can set the following parameters:

- **Number of Users**: Total number of simulated users to spawn.
- **Spawn Rate**: Rate at which users are added (e.g., 10 users per second).

Once configured, you can start the load test and monitor the system's performance in real time as different loads are applied.

---

## 📈 Local Benchmarking Results and Analysis

### **Test Environment**:
- **Hardware**: 2x Nvidia RTX 3090 GPUs

### **Load Configuration**:
- **Concurrent Users**: The server was tested with a maximum of 5 concurrent users.
- **Request Variety**: Each user sent requests with 5 different input lengths.
- **Spawn Rate**: 1 user per second.
- **Wait Time**: Each user waited between 3 to 10 seconds between consecutive requests.

### **Performance**:
- **Average Response Time**: Approximately 6 seconds under this load.

![Benchmarking Results](local_results.png)
