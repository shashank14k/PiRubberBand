from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import subprocess
import shutil
import urllib.request
import tarfile
import sys

rubberband_version = "3.3.0"
src_fname = f"rubberband-{rubberband_version}.tar.bz2"
src_code_link = f"https://breakfastquay.com/files/releases/{src_fname}"

def ensure_build_tools():
    """Ensure meson and ninja are installed."""
    for tool in ['meson', 'ninja']:
        try:
            subprocess.run([tool, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{tool} is installed.")
        except FileNotFoundError:
            print(f"{tool} not found. Please install it manually.")
            sys.exit(1)

def download_and_extract_rubberband(dest_folder):
    """Download and extract the Rubberband source code."""
    os.makedirs(dest_folder, exist_ok=True)
    file_name = os.path.join(dest_folder, src_fname)
    if not os.path.exists(file_name):
        print(f"Downloading {file_name}...")
        urllib.request.urlretrieve(src_code_link, file_name)
        print("Download complete.")
    else:
        print(f"Source file {file_name} already exists. Skipping download.")
    print(f"Extracting {file_name} to {dest_folder}...")
    with tarfile.open(file_name, 'r:bz2') as tar:
        tar.extractall(path=dest_folder)
    print("Extraction complete.")

def build_rubberband(package_dir):
    """Build Rubberband from source."""
    rubberband_dir = os.path.join(package_dir, f"rubberband-{rubberband_version}")
    build_dir = os.path.join(package_dir, "rubberband_build")

    download_and_extract_rubberband(package_dir)
    os.makedirs(build_dir, exist_ok=True)
    ensure_build_tools()

    if sys.platform.startswith('linux'):
        build_command = f"meson setup {build_dir} {rubberband_dir} -Ddefault_library=shared && ninja -C {build_dir}"
        subprocess.run(build_command, check=True, shell=True)

    elif sys.platform.startswith('win'):
        build_command = f"meson setup {build_dir} {rubberband_dir} -Ddefault_library=shared && ninja -C {build_dir}"
        subprocess.run(build_command, check=True, shell=True)

    else:
        raise NotImplementedError(f"{sys.platform} platform not supported")
    print("Cleaning up...")
    # Uncomment these lines if you want to remove build files after installation
    shutil.rmtree(rubberband_dir)
    os.remove(os.path.join(package_dir, src_fname))

class CustomBuildPy(build_py):
    """Custom build command to override the default build_py."""
    def run(self):
        # Call the original build process
        package_dir = os.path.join(self.build_lib, 'pirubberband')
        build_rubberband(package_dir)
        build_py.run(self)

setup(
    name='pirubberband',
    version='0.0.1',
    description='Python wrapper for Rubberband library',
    author='Shashank',
    author_email='shashank14k@gmail.com',
    packages=find_packages(),  # Automatically discover all packages and sub-packages
    install_requires=[],  # Specify dependencies here
    include_package_data=True,
    cmdclass={
        'build_py': CustomBuildPy,
    },
)