from setuptools import setup, find_packages

def requirements_from_file(file_name):
    return open(file_name).read().splitlines()

setup(
    name="scratcher",
    version="0.9.0",
    install_requires=['pandas','numpy','uuid','requests','selenium','webdriver_manager','opencv-python','matplotlib', 'tslearn'],
    packages=find_packages(),
    entry_points={
    }
)
