import subprocess
import os
import re


for filename in os.listdir("./coordinate_csv"):
    filename = re.sub(r"\D", "", filename)
    subprocess.run(["python3", "InputSnapTest_v3.py", filename])
