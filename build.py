import os
import shutil
import sys
from datetime import datetime

def clean_build():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def create_executable():
    """Create executable using PyInstaller"""
    # Get Python installation directory
    python_dir = os.path.dirname(sys.executable)
    
    command = (
        'python -m PyInstaller '
        '--name="Swimming Tracker" '
        '--windowed '
        '--icon=assets/icon.ico '
        f'--paths="{python_dir}" '
        '--add-data="data;data" '
        '--hidden-import=PIL '
        '--hidden-import=PIL._tkinter_finder '
        '--hidden-import=customtkinter '
        '--collect-all customtkinter '
        '--collect-all matplotlib '
        '--noconsole '
        'src/main.py'
    )
    os.system(command)

def create_release():
    """Create release zip file"""
    version = "0.1.0-beta"
    date_str = datetime.now().strftime("%Y%m%d")
    release_name = f"swimming-tracker-v{version}-{date_str}"
    
    # Create release directory
    if os.path.exists(release_name):
        shutil.rmtree(release_name)
    os.makedirs(release_name)
    
    # Copy dist contents to release directory
    dist_path = os.path.join('dist', 'Swimming Tracker')
    if os.path.exists(dist_path):
        shutil.copytree(dist_path, os.path.join(release_name, 'Swimming Tracker'))
        
        # Create zip file
        shutil.make_archive(release_name, 'zip', release_name)
        shutil.rmtree(release_name)
    else:
        print(f"Error: Build directory not found at {dist_path}")

if __name__ == "__main__":
    clean_build()
    create_executable()
    create_release()