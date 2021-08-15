import subprocess
import random
import time
import os
import csv
import glob
import getpass
from pathlib import Path
import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

cpu_model = None
while not cpu_model:
    cpu_model = input('Qual é o seu processador? ').replace(' ', '_')
Path(f'./results/processors/{cpu_model}').mkdir(parents=True, exist_ok=True)

def generateArray(size, seed=None):
    random.seed(seed)
    if os.path.isfile(f"data/array-{size}.txt"): return
    with open(f"data/array-{size}.txt", "w") as f:
        for i in np.arange(size, 0, -1, dtype=np.int64): f.write(str(i) + ' ')

def compile(source_file):
    print(*["g++", "./lib/System.cpp", "./lib/App.hpp", f'algorithms/{source_file}', "-o", f'./bin/{source_file[:-4]}', "-lpapi", "-O0", "-I./lib/", "-I.", "-lm"])
    start_time = time.time()
    process = subprocess.Popen(["g++", "./lib/System.cpp", f'algorithms/{source_file}', "-o", f'./bin/{source_file[:-4]}', "-lpapi", "-O0", "-I./lib/", "-I.", "-lm"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    end_time = (time.time() - start_time)
    print(f"Compile time: {end_time}s")
    if stderr:
        print("Error:\n" + stderr.decode("utf-8"))
        return False
    else:
        print("Compiled with success")
        return True

def run(source_file, args, array_size, log=False):
    start_time = time.time()
    process = subprocess.Popen(["./bin/"+source_file[:-4], *args.split()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    end_time = (time.time() - start_time)
    if log: print(f"{array_size} run time: {end_time}s")
    if stderr:
        if log:
            print("Error:\n" + stderr.decode("utf-8"))
        return False
    else:
        if log: 
            print("Runned with success")
            print('stdout:\n' + stdout.decode("utf-8"))
        return True

def generateResultFile(filename, headers):
    data_filename = f'results/processors/{cpu_model}/result_{filename[:-4]}.txt'
    if os.path.exists(data_filename):
        os.remove(data_filename)
    with open(data_filename, 'w') as data_file:
        data_file.write(headers)

def clean_data_files():
    files = glob.glob('data/*')
    print("Cleaning data/ ~")
    for f in files:
        os.remove(f)

def enableKernelEvents():
    with open("/proc/sys/kernel/perf_event_paranoid", "r") as f:
        r = f.readline().strip()
        print('/proc/sys/kernel/perf_event_paranoid -> ' + r)
        if r != '0':
            print('Type your password to unlock some kernel events. REQUIRED')
            command = "sudo -S sh -c 'echo 0 >/proc/sys/kernel/perf_event_paranoid'"
            password = getpass.getpass()
            aa = os.system('echo %s | %s' % (password, command))
            password = None
            enableKernelEvents()
        else:
            print("Success")

def getProcessorList():
    dirlist = []
    for filename in os.listdir("./results/processors/"):
        if os.path.isdir(os.path.join("./results/processors/",filename)):
            dirlist.append(filename)
    if '.ipynb_checkpoints' in dirlist:
        dirlist.remove('.ipynb_checkpoints')
    return dirlist

enableKernelEvents()

for filename in ['merge_sort.cpp', 'quick_sort.cpp']:
    if compile(filename):
        generateResultFile(filename, 'array_size;time_spent(s);PAPI_L1_TCM;PAPI_L2_TCM;PAPI_L3_TCM;DATA_BYTES;NUM_INSTRUCTIONS;PAPI_TOT_INS\n')

        for array_size in np.arange(2048, 128000+1, 128):
            generateArray(size=array_size)
            run(filename, f'./data/array-{array_size}.txt {array_size} {cpu_model}', array_size, log=False);