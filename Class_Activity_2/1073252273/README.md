# Integration Test Project with Data Cleanup and PDF Reports

This project demonstrates integration testing with automatic data cleanup and PDF report generation.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start All Services
Open **3 separate terminals** and run each service:

**Terminal 1 - Users Service:**
```bash
python -m Users_Service.main
```

**Terminal 2 - Task Service:**
```bash
python -m Task_Service.main
```

**Terminal 3 - Frontend:**
```bash
python -m Front-End.main
```

### 3. Run Tests

**Individual Tests:**
```bash
# Backend integration test
python Test/BackEnd-Test.py

# Frontend E2E test  
python Test/FrontEnd-Test.py
```


## 🏗️ Architecture

- **Users_Service** (Port 5001): User management API
- **Task_Service** (Port 5002): Task management API  
- **Front-End** (Port 5000): Web interface
- **Test Suite**: Integration and E2E tests with cleanup

## ✨ New Features

### 🧹 Automatic Data Cleanup
- **Tracks all data** created during test execution
- **Automatically deletes** test data after completion
- **Verifies deletion** to ensure clean state
- Works for both Backend and Frontend tests

### 📄 PDF Report Generation
- **Sequential numbering** - Reports never overwrite previous ones
- **Detailed test results** with pass/fail status
- **Data tracking** - Shows what was created and cleaned up
- **Automatic generation** after each test run
- Reports saved to `Test_Reports/` directory

## 📊 Test Reports

Reports include:
- ✅ Test execution results
- 📋 Data created during tests (users, tasks)
- 🧹 Cleanup verification results
- 📅 Execution timestamp
- 🔢 Sequential report numbering

Example report: `Test_Reports/test_report_001.pdf`

## 🔧 API Endpoints

### Users Service (Port 5001)
- `POST /users` - Create user
- `GET /users/<id>` - Get user
- `GET /users` - List all users
- `DELETE /users/<id>` - Delete user *(NEW)*

### Task Service (Port 5002)
- `POST /tasks` - Create task
- `GET /tasks` - List all tasks
- `DELETE /tasks/<id>` - Delete task *(NEW)*

## 📁 Project Structure

```
├── Front-End/
│   ├── main.py              # Web interface
│   ├── static/
│   └── templates/
├── Users_Service/
│   └── main.py              # User API
├── Task_Service/
│   └── main.py              # Task API
├── Test/
│   ├── BackEnd-Test.py      # Backend integration test
│   ├── FrontEnd-Test.py     # Frontend E2E test
│   └── test_report_generator.py  # PDF report generator
├── Test_Reports/            # Generated PDF reports
└── requirements.txt
```

## 🛠️ Dependencies

- **flask** - Web framework
- **flask_sqlalchemy** - Database ORM
- **flask_cors** - CORS support
- **requests** - HTTP client for API calls
- **selenium** - Browser automation
- **reportlab** - PDF generation

## 💡 Best Practices Implemented

1. **Test Isolation**: Each test cleans up its own data
2. **Data Verification**: Confirms deletion was successful
3. **Comprehensive Reporting**: Detailed PDF reports with all test information
4. **Report Preservation**: Sequential numbering prevents overwriting
5. **Error Handling**: Robust error capture and reporting
6. **Modular Design**: Reusable components for testing and reporting

## 🚨 Important Notes

- Ensure all services are running before executing tests
- Tests will fail if services are not accessible
- Chrome browser required for frontend tests
- All test data is automatically cleaned up after execution
- PDF reports are preserved and never overwritten
