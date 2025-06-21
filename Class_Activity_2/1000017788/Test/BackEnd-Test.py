import requests
from test_report_generator import TestReportGenerator

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

class BackEndTestRunner:
    def __init__(self):
        self.created_users = []
        self.created_tasks = []
        self.test_results = []
        self.cleanup_results = []
        self.report_generator = TestReportGenerator()
    
    def create_user(self, name):
        try:
            response = requests.post(USERS_URL, json={"name": name})
            response.raise_for_status()
            user_data = response.json()
            self.created_users.append(user_data)
            print("✅ User created:", user_data)
            self.test_results.append({
                'passed': True,
                'description': f'User "{name}" created successfully',
                'details': f'User ID: {user_data["id"]}'
            })
            return user_data["id"]
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': f'Failed to create user "{name}"',
                'details': str(e)
            })
            raise

    def create_task(self, user_id, description):
        try:
            response = requests.post(TASKS_URL, json={
                "title": description,
                "user_id": user_id
            })
            response.raise_for_status()
            task_data = response.json()
            self.created_tasks.append(task_data)
            print("✅ Task created:", task_data)
            self.test_results.append({
                'passed': True,
                'description': f'Task "{description}" created successfully',
                'details': f'Task ID: {task_data["id"]}, User ID: {user_id}'
            })
            return task_data["id"]
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': f'Failed to create task "{description}"',
                'details': str(e)
            })
            raise

    def get_tasks(self):
        try:
            response = requests.get(TASKS_URL)
            response.raise_for_status()
            tasks = response.json()
            return tasks
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to retrieve tasks',
                'details': str(e)
            })
            raise

    def delete_user(self, user_id):
        try:
            response = requests.delete(f"{USERS_URL}/{user_id}")
            if response.status_code == 200:
                self.cleanup_results.append({
                    'success': True,
                    'description': f'User {user_id} deleted successfully'
                })
                return True
            else:
                self.cleanup_results.append({
                    'success': False,
                    'description': f'Failed to delete user {user_id}',
                    'details': f'Status code: {response.status_code}'
                })
                return False
        except Exception as e:
            self.cleanup_results.append({
                'success': False,
                'description': f'Error deleting user {user_id}',
                'details': str(e)
            })
            return False

    def delete_task(self, task_id):
        try:
            response = requests.delete(f"{TASKS_URL}/{task_id}")
            if response.status_code == 200:
                self.cleanup_results.append({
                    'success': True,
                    'description': f'Task {task_id} deleted successfully'
                })
                return True
            else:
                self.cleanup_results.append({
                    'success': False,
                    'description': f'Failed to delete task {task_id}',
                    'details': f'Status code: {response.status_code}'
                })
                return False
        except Exception as e:
            self.cleanup_results.append({
                'success': False,
                'description': f'Error deleting task {task_id}',
                'details': str(e)
            })
            return False

    def verify_data_deleted(self):
        """Verify that all test data has been properly deleted"""
        try:
            # Check if users still exist
            for user in self.created_users:
                response = requests.get(f"{USERS_URL}/{user['id']}")
                if response.status_code == 200:
                    self.test_results.append({
                        'passed': False,
                        'description': f'User {user["id"]} still exists after deletion',
                        'details': 'Data cleanup verification failed'
                    })
                    return False
            
            # Check if tasks still exist
            all_tasks = self.get_tasks()
            for task in self.created_tasks:
                if any(t['id'] == task['id'] for t in all_tasks):
                    self.test_results.append({
                        'passed': False,
                        'description': f'Task {task["id"]} still exists after deletion',
                        'details': 'Data cleanup verification failed'
                    })
                    return False
            
            self.test_results.append({
                'passed': True,
                'description': 'All test data successfully deleted and verified',
                'details': 'Data cleanup verification passed'
            })
            return True
            
        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Failed to verify data deletion',
                'details': str(e)
            })
            return False

    def cleanup_test_data(self):
        """Clean up all data created during the test"""
        print("\n🧹 Starting data cleanup...")
        
        # Delete tasks first (due to foreign key relationships)
        for task in self.created_tasks:
            self.delete_task(task['id'])
        
        # Delete users
        for user in self.created_users:
            self.delete_user(user['id'])
        
        # Verify deletion
        self.verify_data_deleted()

    def run_integration_test(self):
        """Main test execution"""
        try:
            print("🚀 Starting Backend Integration Test...")
            
            # Step 1: Create user
            user_id = self.create_user("Camilo")

            # Step 2: Create task for that user
            task_id = self.create_task(user_id, "Prepare presentation")

            # Step 3: Verify that the task is registered and associated with the user
            tasks = self.get_tasks()
            user_tasks = [t for t in tasks if t["user_id"] == user_id]

            if any(t["id"] == task_id for t in user_tasks):
                self.test_results.append({
                    'passed': True,
                    'description': 'Task correctly registered and linked to user',
                    'details': f'Task ID {task_id} found associated with User ID {user_id}'
                })
                print("✅ Test completed: task was successfully registered and linked to the user.")
            else:
                self.test_results.append({
                    'passed': False,
                    'description': 'Task was not correctly registered or linked to user',
                    'details': f'Task ID {task_id} not found or not associated with User ID {user_id}'
                })
                print("❌ The task was not correctly registered")

        except Exception as e:
            self.test_results.append({
                'passed': False,
                'description': 'Test execution failed with exception',
                'details': str(e)
            })
            print(f"❌ Test failed with error: {e}")
        
        finally:
            # Always clean up data
            self.cleanup_test_data()
            
            # Generate PDF report
            created_data = {
                'users': self.created_users,
                'tasks': self.created_tasks
            }
            
            report_path = self.report_generator.generate_report(
                test_name="Backend Integration Test",
                test_results=self.test_results,
                created_data=created_data,
                cleanup_results=self.cleanup_results
            )
            
            print(f"📊 Test completed. Report saved to: {report_path}")


def integration_test():
    test_runner = BackEndTestRunner()
    test_runner.run_integration_test()


if __name__ == "__main__":
    integration_test()