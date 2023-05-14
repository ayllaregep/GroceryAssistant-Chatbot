import subprocess
import sys
import venv
import os

venv_dir = 'venv'

# Create a virtual environment
print("Creating a virtual environment...")
venv.create(venv_dir, with_pip=True)
print("Virtual environment created successfully.")

# Activate the virtual environment and install dependencies
def install(package):
    subprocess.check_call([os.path.join(venv_dir, 'Scripts', 'python.exe'), "-m", "pip", "install", package])

dependencies = ["flask", "googlemaps", "requests", "Flask-Session"]

for dependency in dependencies:
    print(f"Installing {dependency}...")
    try:
        install(dependency)
        print(f"{dependency} installed successfully.")
    except Exception as e:
        print(f"Error installing {dependency}: {e}")

print("Your venv is ready for use type this in your console: venv\\Scripts\\activate")