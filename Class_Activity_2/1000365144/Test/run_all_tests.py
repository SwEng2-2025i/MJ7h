#!/usr/bin/env python3
"""
Test Runner for Integration Testing Project
Runs both backend and frontend tests and provides a summary.
"""

import subprocess
import sys
import os
from datetime import datetime

def run_test(test_name, test_file):
    """Run a specific test and return the result"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {test_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED")
            return True
        else:
            print(f"❌ {test_name} FAILED")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {test_name} ERROR: {e}")
        return False

def main():
    """Main test runner"""
    print("🧪 Integration Testing Suite")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Change to test directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Test results
    results = {}
    
    # Run backend tests
    results['Backend'] = run_test("Backend Integration Tests", "BackEnd-Test.py")
    
    # Run frontend tests
    results['Frontend'] = run_test("Frontend Integration Tests", "FrontEnd-Test.py")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 