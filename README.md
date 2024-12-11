# Data Engineering Coding Challenge Demyst 

---

##### The purpose of this repo is to provide solutions to problem 1 of the coding challenge provided by Demyst.


### Prerequisites

- **Docker**: Ensure Docker is installed and running on your system. You can use local but for ease of use it's highly recommended that you use Docker.

### Setup

#### **Option 1: Running with Docker (Recommended)**
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and Run the Program with Docker**:
   Ensure Docker is installed and running, then build and run the application:
   ```bash
   docker compose build
   docker compose up
   ```

3. **Running Tests** (Optional):
   To run tests, use the following command:
   ```bash
   docker compose run test
   ```
   
#### **Option 2: Running on Local (NOT Recommended)**
1. **If you want to run on local w/o Docker you will need to setup a virtual env with Python 3.10.**
2. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```**
3. **python -m venv venv** source venv/bin/activate on macOS/Linux
4. **pip install -r requirements.txt** 
5. **Run the program with - python main.py**
6. **Run tests - pytest --maxfail=5 --disable-warnings**
7. **deactivate** This will deactivate the virtual env