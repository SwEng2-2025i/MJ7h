# Class Activity 2 
David Fernando Adames Rondon, 1000252828

## Implemented Features

1.  **Data Cleanup:** All tests now automatically delete any data they create (users, tasks) and verify that the deletion was successful. This ensures a clean state after each test run.

2.  **Automatic PDF Reports:** Both backend and frontend tests now generate a PDF report summarizing their execution. These reports are saved with a unique, sequential number in the `reports/` directory and are not overwritten.

## Code Modifications Summary

### Services (`Users_Service/` & `Task_Service/`)
*   Added `DELETE` endpoints to both services (`/users/<id>` and `/tasks/<id>`) to enable data cleanup.
*   Added a `GET /tasks/<id>` endpoint to the Task Service for more direct verification.

### Testing (`Test/`)
*   **`BackEnd-Test.py` & `FrontEnd-Test.py`**:
    *   Updated to call the new `DELETE` endpoints for cleanup after test execution.
    *   Added verification steps to confirm data deletion.
    *   Integrated the new PDF reporting module to save test logs.

### Reporting (`reporting/`)
*   **`pdf_generator.py` (New File)**: A module created to handle the generation of sequentially numbered PDF reports from test logs.
*   **`__init__.py` (New File)**: Makes the `reporting` directory a Python package.

### Project Files
*   **`requirements.txt`**: Added `selenium` and `fpdf2` libraries.
*   **`README.md` (This File)**: Updated to document the changes. 