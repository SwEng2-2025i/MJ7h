# Quick Start Guide - Integration Testing Project

## 📋 Project Overview

This is a simple integration testing example that demonstrates how to test a microservices architecture with a frontend application. The project consists of:

- **Users Service** (Port 5001): Manages user data
- **Task Service** (Port 5002): Manages tasks and integrates with Users Service
- **Frontend** (Port 5000): Web interface for creating users and tasks
- **Test Suite**: Backend and Frontend integration tests with data cleanup and PDF reporting

## 🚀 Quick Setup

### Prerequisites
- Python 3.7+
- Firefox browser (for frontend tests)
- GeckoDriver (automatically managed by webdriver-manager)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start all services (Option 1 - Automated):**
   ```bash
   python start_services.py
   ```
   This will start all services automatically and keep them running until you press Ctrl+C.

3. **Start all services (Option 2 - Manual):**
   ```bash
   # Terminal 1 - Users Service
   cd Users_Service
   python main.py
   
   # Terminal 2 - Task Service  
   cd Task_Service
   python main.py
   
   # Terminal 3 - Frontend
   cd Front-End
   python main.py
   ```

4. **Run tests (Option 1 - All tests):**
   ```bash
   cd Test
   python run_all_tests.py
   ```

5. **Run tests (Option 2 - Individual tests):**
   ```bash
   # Backend integration tests
   cd Test
   python BackEnd-Test.py
   
   # Frontend integration tests
   python FrontEnd-Test.py
   ```

## 🏗️ Project Structure

```
100036144/
├── Users_Service/
│   └── main.py              # User management API
├── Task_Service/
│   └── main.py              # Task management API
├── Front-End/
│   └── main.py              # Web interface
├── Test/
│   ├── BackEnd-Test.py      # Backend integration tests
│   ├── FrontEnd-Test.py     # Frontend integration tests
│   └── run_all_tests.py     # Test runner script
├── reports/                 # Generated PDF reports (auto-created)
├── start_services.py        # Service startup script
├── requirements.txt         # Python dependencies
├── README.md               # Project instructions
└── QUICKSTART.md           # This file
```

## 🔧 API Endpoints

### Users Service (Port 5001)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/users` | Create a new user | `{"name": "string"}` | `{"id": int, "name": "string"}` |
| GET | `/users/<id>` | Get user by ID | - | `{"id": int, "name": "string"}` |
| GET | `/users` | List all users | - | `[{"id": int, "name": "string"}]` |
| DELETE | `/users/<id>` | Delete user by ID | - | `{"message": "string"}` |

### Task Service (Port 5002)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/tasks` | Create a new task | `{"title": "string", "user_id": int}` | `{"id": int, "title": "string", "user_id": int}` |
| GET | `/tasks` | List all tasks | - | `[{"id": int, "title": "string", "user_id": int}]` |
| DELETE | `/tasks/<id>` | Delete task by ID | - | `{"message": "string"}` |
| DELETE | `/tasks/user/<user_id>` | Delete all tasks for a user | - | `{"message": "string"}` |

## 🧪 Testing Features

### New Features Implemented

#### 1. Data Cleanup
- **Backend Tests**: Automatically delete test data after each test run
- **Frontend Tests**: Clean up data created during UI testing
- **Verification**: Tests verify that cleanup was successful

#### 2. PDF Report Generation
- **Sequential Numbering**: Reports are numbered sequentially (001, 002, etc.)
- **No Overwriting**: Previous reports are preserved
- **Comprehensive Results**: Includes all test steps and outcomes
- **Separate Reports**: Backend and Frontend tests generate separate reports

### Test Execution Flow

#### Backend Test (`BackEnd-Test.py`)
1. Create test user
2. Create test task for the user
3. Verify task is properly linked to user
4. Clean up test data (delete task, then user)
5. Verify cleanup was successful
6. Generate PDF report

#### Frontend Test (`FrontEnd-Test.py`)
1. Open frontend application
2. Create user through web interface
3. Create task through web interface
4. Verify task appears in task list
5. Clean up test data via API calls
6. Verify cleanup was successful
7. Generate PDF report

### Report Structure

PDF reports include:
- Report number (sequential)
- Date and time of execution
- Test results for each step
- Pass/fail status for each operation
- Cleanup verification results

## 📊 Sample Test Output

```
✅ User created: {'id': 1, 'name': 'Camilo'}
✅ Task created: {'id': 1, 'title': 'Prepare presentation', 'user_id': 1}
✅ Test completed: task was successfully registered and linked to the user.
🧹 Cleaning up test data: User 1, Task 1
✅ Task 1 deleted successfully
✅ User 1 deleted successfully
🔍 Verifying data cleanup...
✅ User cleanup verified
✅ Task cleanup verified
📄 PDF report generated: reports/test_report_001.pdf
🎉 All tests passed successfully!
```

## 🔍 Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find and kill process using the port
   lsof -ti:5000 | xargs kill -9
   lsof -ti:5001 | xargs kill -9
   lsof -ti:5002 | xargs kill -9
   ```

2. **GeckoDriver issues:**
   - webdriver-manager should automatically manage GeckoDriver
   - If issues persist, install GeckoDriver manually or ensure Firefox is properly installed

3. **Database issues:**
   - Delete `*.db` files in service directories to reset databases
   - Restart services after database reset

### Service Status Check

```bash
# Check if services are running
curl http://localhost:5001/users
curl http://localhost:5002/tasks
curl http://localhost:5000
```

## 🛠️ Utility Scripts

### `start_services.py`
- Automatically starts all services
- Monitors service health
- Provides easy shutdown with Ctrl+C
- Shows service URLs and test instructions

### `run_all_tests.py`
- Runs both backend and frontend tests sequentially
- Provides comprehensive test summary
- Shows pass/fail status for each test
- Returns appropriate exit codes



