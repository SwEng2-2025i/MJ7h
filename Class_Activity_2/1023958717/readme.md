# Project Integration & Testing

This repository contains three components:

1. **User Service** (`main_users_service.py`) – Manages user creation, retrieval, and deletion.
2. **Task Service** (`main_task_service.py`) – Manages task creation, retrieval, and deletion.
3. **Frontend** (`main_front.py`) – Provides a simple web interface to interact with both services.

Additionally, automated integration tests for both backend and frontend ensure clean data handling and PDF report generation.

---

## Sections with Changes

### 1. User Service (`main_users_service.py`)

- **Added** `DELETE /users/<int:user_id>` endpoint to remove users.
- **Validation**: Returns `404 Not Found` if the user does not exist, otherwise deletes and returns `200 OK`.

### 2. Task Service (`main_task_service.py`)

- **Added** `DELETE /tasks/<int:task_id>` endpoint to remove tasks.
- **Validation**: Returns `404 Not Found` if the task does not exist, otherwise deletes and returns `200 OK`.

### 3. Frontend (`main_front.py`)

- **UI Update**: Added an **"Delete"** button next to each task in the tasks list.
- **JavaScript**: Implemented `deleteTask(taskId)` function that calls `DELETE /tasks/{taskId}` and refreshes the list after deletion.
- **Optional CSS**: Styled the delete button with a red background and hover effect.

### 4. Backend Integration Test (`BackEnd-Test.py`)

- **Data Cleanup**: After creating a user and task, calls `DELETE` on both resources and asserts they no longer exist.
- **PDF Reports**: Uses `reportlab` to generate sequenced PDF reports (`test_reports/report_1.pdf`, `report_2.pdf`, etc.) summarizing test outcomes.

### 5. Frontend Integration Test (`FrontEnd-Test.py`)

- **Data Cleanup**: After performing end-to-end UI operations (create user → create task → verify list), deletes the created entities via API and verifies removal in the UI.
- **PDF Reports**: Uses `reportlab` to generate sequenced PDF reports (`frontend_reports/report_1.pdf`, `report_2.pdf`, etc.) summarizing test outcomes.

---



## Notes

- Make sure both services are running before executing tests.
- Each test run appends a new PDF, preserving all previous reports.
- Ensure `reportlab` and `selenium` (plus WebDriver) are installed for PDF and UI tests.

---

*End of README*

