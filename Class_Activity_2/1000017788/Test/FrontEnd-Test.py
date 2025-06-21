import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_report_generator import TestReportGenerator

class FrontEndTestRunner:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
        self.cleanup_results = []
        self.report_generator = TestReportGenerator()
        self.driver = None
        self.wait = None
    
    def setup_browser(self):
        """Initialize browser"""
        options = Options()
        # options.add_argument('--headless')  # Uncomment for headless mode
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def abrir_frontend(self):
        """Opens the frontend application in the browser"""
        try:
            self.driver.get("http://localhost:5000")
            time.sleep(2)  # Give the page time to load
            self.test_results.append({
                'passed': True,
                'description': 'Frontend application opened successfully',
                'details': 'Connected to http://localhost:5000'
            })
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to open frontend application',
                'details': str(e)
            })
            raise

    def crear_usuario(self):
        """Creates a user through the frontend and returns the user ID"""
        try:
            username_input = self.driver.find_element(By.ID, "username")
            username_input.send_keys("Ana")
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
            time.sleep(2)

            user_result = self.driver.find_element(By.ID, "user-result").text
            print("Resultado usuario:", user_result)
            
            if "Usuario creado con ID" in user_result:
                user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
                
                # Store user data for cleanup
                user_data = {'id': int(user_id), 'name': 'Ana'}
                self.created_users.append(user_data)
                
                self.test_results.append({
                    'passed': True,
                    'description': 'User created successfully through frontend',
                    'details': f'User "Ana" created with ID: {user_id}'
                })
                return user_id
            else:
                raise Exception(f"User creation failed: {user_result}")
                
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to create user through frontend',
                'details': str(e)
            })
            raise

    def crear_tarea(self, user_id):
        """Creates a task through the frontend"""
        try:
            task_input = self.driver.find_element(By.ID, "task")
            task_input.send_keys("Terminar laboratorio")
            time.sleep(1)

            userid_input = self.driver.find_element(By.ID, "userid")
            userid_input.send_keys(user_id)
            userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
            time.sleep(1)

            crear_tarea_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
            )
            crear_tarea_btn.click()
            time.sleep(2)

            self.wait.until(
                EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
            )
            task_result = self.driver.find_element(By.ID, "task-result")
            print("Texto en task_result:", task_result.text)
            
            if "Tarea creada con ID" in task_result.text:
                task_id = ''.join(filter(str.isdigit, task_result.text))
                
                # Store task data for cleanup
                task_data = {'id': int(task_id), 'title': 'Terminar laboratorio', 'user_id': int(user_id)}
                self.created_tasks.append(task_data)
                
                self.test_results.append({
                    'passed': True,
                    'description': 'Task created successfully through frontend',
                    'details': f'Task "Terminar laboratorio" created with ID: {task_id}'
                })
                return task_id
            else:
                raise Exception(f"Task creation failed: {task_result.text}")
                
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to create task through frontend',
                'details': str(e)
            })
            raise

    def ver_tareas(self):
        """Verifies that the created task appears in the task list"""
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
            time.sleep(2)

            tasks = self.driver.find_element(By.ID, "tasks").text
            print("Tareas:", tasks)
            
            if "Terminar laboratorio" in tasks:
                self.test_results.append({
                    'passed': True,
                    'description': 'Task appears correctly in the task list',
                    'details': 'Task "Terminar laboratorio" found in the frontend task list'
                })
            else:
                self.test_results.append({
                    'passed': False,
                    'description': 'Task does not appear in the task list',
                    'details': f'Task list content: {tasks}'
                })
                
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to verify task in task list',
                'details': str(e)
            })
            raise

    def delete_user_via_api(self, user_id):
        """Delete user via API call"""
        try:
            response = requests.delete(f"http://localhost:5001/users/{user_id}")
            if response.status_code == 200:
                self.cleanup_results.append({
                    'success': True,
                    'description': f'User {user_id} deleted successfully via API'
                })
                return True
            else:
                self.cleanup_results.append({
                    'success': False,
                    'description': f'Failed to delete user {user_id} via API',
                    'details': f'Status code: {response.status_code}'
                })
                return False
        except Exception as e:
            self.cleanup_results.append({
                'success': False,
                'description': f'Error deleting user {user_id} via API',
                'details': str(e)
            })
            return False

    def delete_task_via_api(self, task_id):
        """Delete task via API call"""
        try:
            response = requests.delete(f"http://localhost:5002/tasks/{task_id}")
            if response.status_code == 200:
                self.cleanup_results.append({
                    'success': True,
                    'description': f'Task {task_id} deleted successfully via API'
                })
                return True
            else:
                self.cleanup_results.append({
                    'success': False,
                    'description': f'Failed to delete task {task_id} via API',
                    'details': f'Status code: {response.status_code}'
                })
                return False
        except Exception as e:
            self.cleanup_results.append({
                'success': False,
                'description': f'Error deleting task {task_id} via API',
                'details': str(e)
            })
            return False

    def verify_data_deleted(self):
        """Verify that all test data has been properly deleted"""
        try:
            # Check if users still exist via API
            for user in self.created_users:
                response = requests.get(f"http://localhost:5001/users/{user['id']}")
                if response.status_code == 200:
                    self.test_results.append({
                        'passed': False,
                        'description': f'User {user["id"]} still exists after deletion',
                        'details': 'Frontend test data cleanup verification failed'
                    })
                    return False
            
            # Check if tasks still exist via API
            response = requests.get("http://localhost:5002/tasks")
            if response.status_code == 200:
                all_tasks = response.json()
                for task in self.created_tasks:
                    if any(t['id'] == task['id'] for t in all_tasks):
                        self.test_results.append({
                            'passed': False,
                            'description': f'Task {task["id"]} still exists after deletion',
                            'details': 'Frontend test data cleanup verification failed'
                        })
                        return False
            
            self.test_results.append({
                'passed': True,
                'description': 'All frontend test data successfully deleted and verified',
                'details': 'Frontend data cleanup verification passed'
            })
            return True
            
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to verify frontend data deletion',
                'details': str(e)
            })
            return False

    def cleanup_test_data(self):
        """Clean up all data created during the frontend test"""
        print("\n🧹 Starting frontend data cleanup...")
        
        # Delete tasks first (due to foreign key relationships)
        for task in self.created_tasks:
            self.delete_task_via_api(task['id'])
        
        # Delete users
        for user in self.created_users:
            self.delete_user_via_api(user['id'])
        
        # Verify deletion
        self.verify_data_deleted()

    def run_frontend_test(self):
        """Main test execution"""
        try:
            print("🚀 Starting Frontend E2E Test...")
            
            self.setup_browser()
            self.abrir_frontend()
            user_id = self.crear_usuario()
            self.crear_tarea(user_id)
            self.ver_tareas()
            time.sleep(3)  # Final delay to observe results if not running headless
            
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Frontend test execution failed with exception',
                'details': str(e)
            })
            print(f"❌ Frontend test failed with error: {e}")
        
        finally:
            # Always close browser and clean up data
            if self.driver:
                self.driver.quit()
            
            self.cleanup_test_data()
            
            # Generate PDF report
            created_data = {
                'users': self.created_users,
                'tasks': self.created_tasks
            }
            
            report_path = self.report_generator.generate_report(
                test_name="Frontend E2E Test",
                test_results=self.test_results,
                created_data=created_data,
                cleanup_results=self.cleanup_results
            )
            
            print(f"📊 Frontend test completed. Report saved to: {report_path}")


def main():
    """Main test runner that initializes the browser and runs the full E2E flow"""
    test_runner = FrontEndTestRunner()
    test_runner.run_frontend_test()


if __name__ == "__main__":
    main()
