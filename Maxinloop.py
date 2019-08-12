import psutil
import os
import subprocess

for n in range[2]:
	subprocess.Popen([r"3dsmax.exe"])
	for pid in (process.pid for process in psutil.process_iter() if process.name()=="3dsmax.exe"):
		os.kill(pid)


