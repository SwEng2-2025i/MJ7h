# Integration Test Report - Class Activity 2

This project implements a basic microservice architecture using Flask, with automated integration testing and PDF reporting. It consists of:

- A **User Service** (`Users_Service/main.py`) running on port `5001`
- A **Task Service** (`Task_Service/main.py`) running on port `5002`
- A **Front-End** Flask app (`Front-End/main.py`) running on port `5000`
- An **automated integration test** that verifies communication between services and generates a PDF report
- A `requirements.txt` file to manage dependencies

---

## ✅ Summary of Test Results

- A user was created and a task was linked to that user successfully.
- The task appeared in the task list (fetched via the API).
- Both resources were deleted after the test.
- A PDF report was generated and saved with a unique number.

---

## 🛠️ Sections of Code Added

### 1. **Test Automation** (`Test/BackEnd-Test.py`)
Functions added:
- `create_user()`, `create_task()`, `get_tasks()`, `delete_user()`, `delete_task()`
- `integration_test()` orchestrates the entire test and logs the outcome.
- Results are collected and passed to a report generator.

### 2. **Report Generation** (`Test/reports/generate_report.py`)
- The function `generate_pdf_report(content)` creates a uniquely numbered PDF file containing the test log.
- PDF files are saved in the `reports/` folder without overwriting previous reports.

### 3. **Backend Endpoints Added**
- **User Service (`service_a.py`):**
  - `DELETE /users/<int:user_id>`
- **Task Service (`service_b.py`):**
  - `DELETE /tasks/<int:task_id>`

---

## 🚀 How to Run the Project

### 1. Clone the repository

``` bash
git clone https://github.com/SwEng2-2025i/MJ7h.git
cd Class_Activity_2/1011201389/
```

### 2. Create and activate a virtual environment (optional but recommended)
``` bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
``` bash
pip install -r requirements.txt
```

### 4. Run the services (in separate terminal tabs/windows)
#### 🟢 User Service (port 5001)
``` bash
    python .\Users_Service\main.py
```

#### 🟢 Task Service (port 5002)
``` bash
    python .\Task_Service\main.py 
```

#### 🟢 Front-End (port 5000)
``` bash
    python Front-End/main.py
```

### 5. Run the integration tests for backend and frontend
#### Backend
``` bash
python .\Test\BackEnd-Test.py  
```
#### Frontend
``` bash
python .\Test\FrontEnd-Test.py
```
