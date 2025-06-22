#!/usr/bin/env python3
"""
Service Startup Script
Starts all microservices for the integration testing project.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_service(service_name, service_path, port):
    """Start a service in the background"""
    print(f"🚀 Starting {service_name} on port {port}...")
    
    try:
        # Change to service directory and start the service
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=service_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for the service to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {service_name} started successfully (PID: {process.pid})")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start {service_name}")
            print(f"Error: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"💥 Error starting {service_name}: {e}")
        return None

def check_service_health(port):
    """Check if a service is responding"""
    try:
        import requests
        response = requests.get(f"http://localhost:{port}", timeout=5)
        return response.status_code < 500
    except:
        return False

def main():
    """Main startup function"""
    print("🔧 Starting Integration Testing Services")
    print("=" * 50)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Service configurations
    services = [
        ("Users Service", project_root / "Users_Service", 5001),
        ("Task Service", project_root / "Task_Service", 5002),
        ("Frontend", project_root / "Front-End", 5000)
    ]
    
    processes = []
    
    try:
        # Start all services
        for service_name, service_path, port in services:
            if not service_path.exists():
                print(f"❌ Service directory not found: {service_path}")
                continue
                
            process = start_service(service_name, service_path, port)
            if process:
                processes.append((service_name, process, port))
            else:
                print(f"💥 Failed to start {service_name}. Stopping all services.")
                return 1
        
        # Wait for services to be ready
        print("\n⏳ Waiting for services to be ready...")
        time.sleep(5)
        
        # Check service health
        print("\n🔍 Checking service health...")
        all_healthy = True
        
        for service_name, process, port in processes:
            if check_service_health(port):
                print(f"✅ {service_name} is healthy")
            else:
                print(f"⚠️ {service_name} may not be ready yet")
                all_healthy = False
        
        if all_healthy:
            print("\n🎉 All services started successfully!")
            print("\n📋 Service URLs:")
            print("   Frontend: http://localhost:5000")
            print("   Users API: http://localhost:5001")
            print("   Tasks API: http://localhost:5002")
            print("\n🧪 To run tests:")
            print("   cd Test")
            print("   python run_all_tests.py")
            print("\n⏹️ Press Ctrl+C to stop all services")
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping all services...")
                
        else:
            print("\n⚠️ Some services may not be ready. Check the logs above.")
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n💥 Error: {e}")
    finally:
        # Clean up processes
        print("\n🧹 Cleaning up processes...")
        for service_name, process, port in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"✅ {service_name} stopped")
            except:
                try:
                    process.kill()
                    print(f"🔪 {service_name} force killed")
                except:
                    print(f"⚠️ Could not stop {service_name}")
        
        print("👋 All services stopped")

if __name__ == "__main__":
    sys.exit(main()) 