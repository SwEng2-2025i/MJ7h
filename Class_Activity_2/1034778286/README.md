# Integration Testing Suite – SwEng2 Activity

This project extends the integration testing example covered in class by adding:

- Post-test data cleanup for users and tasks.
- Automatic generation of PDF reports.
- Summary chart of executed tests.
- Inclusion of intentionally failing tests for validation.
- Centralized registry and execution of multiple tests with statistics.

---

## Project Structure

1034778286/
├── run_all_tests.py # Runs all tests and generates general report  
├── reports/ # Automatically generated PDFs and charts  
├── Test/  
│ ├── BackEnd-Test.py # Integration test for backend (create/delete task)  
│ ├── FrontEnd-Test.py # Full E2E test using Selenium + Chrome (create/verify/delete)  
│ ├── InvalidUser-Test.py # Failing test (attempt to create task with invalid user)  
│ ├── registry.py # Central registry for all test files  
│ └── utils/  
│ └── report.py # Function to generate sequentially numbered PDF reports  
│  
├── Task_Service/  
│ └── main.py # Flask service for tasks (create, list, delete)  
│  
├── Users_Service/  
│ └── main.py # Flask service for users (create, list, delete)  

---

## How to Run

1. Make sure all dependencies are installed:
    ```
    pip install -r requirements.txt
    ```

2. Start services and frontend:
    ```
    python Users_Service/main.py
    python Task_Service/main.py
    python Front-End/main.py
    ```

3. Run the full test suite with:
    ```
    python run_all_tests.py
    ```

---

## Data Cleanup

Each test that creates data (user or task) deletes it after execution.  
HTTP responses are verified to ensure the data was successfully removed.

---

## Generated Reports

- Each test run automatically generates a PDF summary using `reportlab`.
- The file is saved under `reports/` with a sequential name like `frontend_report_1.pdf`, `suite_report_2.pdf`, etc.
- Previous reports are preserved and never overwritten.

---

## Results Chart

- The file `reports/tests_summary.png` shows how many tests passed and how many failed.
- It provides a quick visual summary of the suite's status.

---

## Added Tests

### Successful

- `FrontEnd-Test.py`: full browser-based test.
- `BackEnd-Test.py`: backend-only integration test.

### Failing

- `InvalidUser-Test.py`: tries to create a task with a non-existent user ID.
  This validates proper error handling in the system.

---

## Code Modifications

### New features:

- `DELETE` endpoints added to `/users/<id>` and `/tasks/<id>` in both services.
- `generate_pdf_report()` defined in `Test/utils/report.py`.
- Central test registry in `Test/registry.py`.
- Validation test that fails: `InvalidUser-Test.py`.
- New orchestrator `run_all_tests.py` to run all tests and generate the summary chart.

---
