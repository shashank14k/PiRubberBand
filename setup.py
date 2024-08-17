import os
import sys
import subprocess
import urllib.request
import tarfile
import configparser
import shutil

def ensure_setuptools():
    try:
        import setuptools
        print("setuptools is already installed.")
    except ImportError:
        print("setuptools not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'setuptools'], check=True)
            import setuptools
            print("setuptools installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install setuptools. Please install it manually.")
            sys.exit(1)

ensure_setuptools()
from setuptools import setup
rubberband_version = "3.3.0"
fname = f"rubberband-{rubberband_version}.tar.bz2"
rubberband_src_code_link = f"https://breakfastquay.com/files/releases/{fname}"
cwd = os.path.dirname(__file__)

def download_and_extract_rubberband(dest_folder):
    os.makedirs(dest_folder, exist_ok=True)
    # Download the file
    file_name = os.path.join(dest_folder, rubberband_src_code_link.split('/')[-1])
    print(f"Downloading {file_name}...")
    urllib.request.urlretrieve(rubberband_src_code_link, file_name)
    print("Download complete.")

    # Extract the file
    print(f"Extracting {file_name} to {dest_folder}...")
    with tarfile.open(file_name, 'r:bz2') as tar:
        tar.extractall(path=dest_folder)
    print("Extraction complete.")

def install_rubberband():
    install_dir = os.path.join(cwd)
    rubberband_dir = os.path.join(cwd, f"rubberband-{rubberband_version}")
    build_dir = os.path.join(cwd, "rubberband")
    download_and_extract_rubberband(install_dir)
    os.makedirs(build_dir, exist_ok=True)

    if sys.platform.startswith('linux'):
        build_command = f"meson setup {rubberband_dir} {build_dir} -Ddefault_library=shared && ninja -C {build_dir}"
    else:
        raise NotImplemented("{} not supported".format(sys.platform))

    subprocess.run(build_command, check=True, shell=True)
    os.chdir(install_dir)


    config = configparser.ConfigParser()
    config['Rubberband'] = {
        'so_file': os.path.join(build_dir, "librubberband.so")
    }

    # Write the configuration to the file
    with open(os.path.join(cwd, "pirubberband", "config.conf"), 'w') as configfile:
        config.write(configfile)
    shutil.rmtree(rubberband_dir)
    os.remove(os.path.join(cwd, fname))


install_rubberband()

# Define your package setup
setup(
    name='pirubberband',
    version='0.0.1',
    description='Python wrapper for rubberband library',
    author='Shashank',
    author_email='shashank14k@gmail.com',
    packages=['pirubberband'],
    install_requires=[
        "numpy",
        "soundfile"
    ],
)
