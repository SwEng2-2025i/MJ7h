# Class Activity 2: Extending Integration Tests

This document outlines the changes made to the "Example 5 - Integration Test" project to fulfill the requirements of Class Activity 2.

## Features Implemented

1.  **Data Cleanup**: All data created during the backend and frontend tests (users and tasks) is now automatically deleted after the test execution completes. The tests include steps to verify that the data has been successfully removed from the system.
2.  **Automatic PDF Report Generation**: After each test run, a PDF report summarizing the results is generated. Each report is given a sequential number (e.g., `Backend_Integration_Test_report_1.pdf`, `Backend_Integration_Test_report_2.pdf`) to ensure that previous reports are not overwritten.

## Code Modifications

### 1. Services (`Users_Service` and `Task_Service`)

-   **`Users_Service/main.py`**: Added a `DELETE /users/<int:user_id>` endpoint to allow for the deletion of users.
-   **`Task_Service/main.py`**: Added a `DELETE /tasks/<int:task_id>` endpoint to allow for the deletion of tasks.

### 2. Tests (`Test` folder)

-   **`Test/report_generator.py`**: A new module was created using the `fpdf2` library to handle the generation of PDF reports. It automatically finds the next available report number to avoid overwriting files.

-   **`Test/BackEnd-Test.py`**:
    -   The test is wrapped in a `try...finally` block to ensure cleanup is always executed.
    -   The `finally` block calls new `delete_user` and `delete_task` functions.
    -   After deletion, new verification functions (`verify_user_deleted` and `verify_task_deleted`) are called to assert that the records no longer exist (expecting a 404 response).
    -   At the end of the test, it calls `generate_pdf_report` to save the results.

-   **`Test/FrontEnd-Test.py`**:
    -   Similar to the backend test, it uses a `try...finally` block.
    -   The `finally` block performs cleanup by making direct HTTP `DELETE` requests to the user and task services using the `requests` library.
    -   It verifies deletion by checking for a 404 status code on subsequent `GET` requests.
    -   It also calls `generate_pdf_report` to save the E2E test results.

### 3. Dependencies

-   **`requirements.txt`**: The `fpdf2` library was added as a dependency to support PDF generation.

## How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r "Example 5 - Integration Test/requirements.txt"
    ```
2.  **Start the Services**: Open three separate terminals and run:
    ```bash
    # Terminal 1: Frontend
    python "Example 5 - Integration Test/Front-End/main.py"

    # Terminal 2: Users Service
    python "Example 5 - Integration Test/Users_Service/main.py"

    # Terminal 3: Task Service
    python "Example 5 - Integration Test/Task_Service/main.py"
    ```
3.  **Run the Tests**: Open a new terminal for each test:
    ```bash
    # Run Backend Test
    python "Example 5 - Integration Test/Test/BackEnd-Test.py"

    # Run Frontend Test
    python "Example 5 - Integration Test/Test/FrontEnd-Test.py"
    ```

After running the tests, the generated PDF reports will be available in the `Example 5 - Integration Test/Test/` directory.
