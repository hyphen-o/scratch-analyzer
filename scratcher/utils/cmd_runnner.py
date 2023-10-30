import subprocess


class CmdRunner:
    def __init__(self, cmd):
        self.cmd = cmd

    def run_command(self):
        try:
            result = subprocess.run(
                self.cmd, shell=True, capture_output=True, text=True
            )
            return {
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except Exception as e:
            return {"stdout": "", "stderr": str(e), "returncode": -1}
