import subprocess
from tqdm import tqdm 

archs = ["x86", "ARM", "RISCV"]
caches = ["0", "1"]
l1DCache = ["32", "64", "128"]
l1ICache = ["32", "64", "128"]
l2Cache = ["128", "256", "512", "1024"]
dim = []
max_val = int(1e6)

i = 5
while i < int(100):
    dim.append(str(i))
    i *= 2
print("Matrix sizes:", dim)

def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

# Calculate total tasks for tqdm
total_tasks = 0
for arch in archs:
    for cache in caches:
        if cache == "0":
            total_tasks += len(dim)
        else:
            total_tasks += len(l1DCache) * len(l1ICache) * len(l2Cache) * len(dim)

# Progress bar
with tqdm(total=total_tasks, desc="Running Simulations") as pbar:
    for arch in archs:
        for cache in caches:
            if cache == "0":
                for d in dim:
                    command = [
                        "../../../build/ALL/gem5.opt",
                        "Modular.py",
                        "--arch", arch,
                        "--cache", cache,
                        "--dim", d,
                        "--max", str(max_val),
                    ]
                    run(command)
                    pbar.update(1)
            else:
                for l1d in l1DCache:
                    for l1i in l1ICache:
                        for l2 in l2Cache:
                            for d in dim:
                                command = [
                                    "../../../build/ALL/gem5.opt",
                                    "Modular.py",
                                    "--arch", arch,
                                    "--cache", cache,
                                    "--L1ISize", l1i,
                                    "--L1DSize", l1d,
                                    "--L2Size", l2,
                                    "--dim", d,
                                    "--max", str(max_val),
                                ]
                                run(command)
                                pbar.update(1)
