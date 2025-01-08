import subprocess

login_process = subprocess.run(["python", "SD/GUI/login.py"], check=False)

if login_process.returncode == 1:
    subprocess.run(["python", "SD/GUI/Gui.py"], check=True)

