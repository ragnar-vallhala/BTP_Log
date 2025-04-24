
import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description="Parse command-line arguments for gem5 simulation")


parser.add_argument(
    "--arch", 
    type=str, 
    help="ISA architecture"
)

parser.add_argument(
    "--cache", 
    type=int, 
    help="Cache availablity"
)

parser.add_argument(
    "--L1ISize", 
    type=int, 
    help="L1 instruction cache size"
)

parser.add_argument(
    "--L1DSize", 
    type=int, 
    help="L1 data cache size"
)

parser.add_argument(
    "--L1Assoc", 
    type=int, 
    help="L1 cache associativity"
)


parser.add_argument(
    "--L2Size", 
    type=int, 
    help="L2 instruction cache size"
)

parser.add_argument(
    "--L2Assoc", 
    type=int, 
    help="L2 cache associativity"
)

parser.add_argument(
    "--dim", 
    type=int, 
    help="matrix dimension"
)


parser.add_argument(
    "--max", 
    type=int, 
    help="maximum value"
)

compilers={
    "x86": "gcc",
    "ARM": "aarch64-linux-gnu-gcc",
    "RISCV": "riscv64-linux-gnu-gcc"
}
args = parser.parse_args()



def process():
    from gem5.components.boards.simple_board import SimpleBoard
    from gem5.components.memory.single_channel import SingleChannelDDR3_1600
    from gem5.components.processors.simple_processor import SimpleProcessor
    from gem5.components.processors.cpu_types import CPUTypes
    from gem5.isas import ISA
    from gem5.resources.resource import BinaryResource
    from gem5.simulate.simulator import Simulator
    from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import PrivateL1PrivateL2CacheHierarchy
    from gem5.components.cachehierarchies.classic.no_cache import NoCache


    command = [f"{compilers[args.arch]}", "-static", f"-DDIM={args.dim}", f"-DMAX={args.max}","-o", f"mul-{args.arch}", "mul.c"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"{command} \nSTDOUT:", result.stdout, "\nSTDERR:", result.stderr)

    #####################################################################################################################################
    memory = SingleChannelDDR3_1600("4GiB")

    isa=None
    if args.arch == "x86":
        isa=ISA.X86
    elif args.arch=="ARM":
        isa=ISA.ARM
    elif args.arch=="RISCV":
        isa=ISA.RISCV

    processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=isa)

    ####################################################################################################################################

    cache_hierarchy = NoCache()
    if args.cache==0:
        cache_hierarchy=NoCache()
    elif args.cache==1:
        cache_hierarchy=PrivateL1PrivateL2CacheHierarchy(l1d_size=str(args.L1DSize)+"kB", l1i_size=str(args.L1ISize)+"kB", l2_size=str(args.L2Size)+"kB")


    ###################################################################################################################################
    board = SimpleBoard(
        clk_freq="1GHz",
        processor=processor,
        memory=memory,
        cache_hierarchy=cache_hierarchy,
    )
    ####################################################################################################################################
    # Set the workload.
    binary = BinaryResource(f"/home/ragnar/Documents/BTP/gem5/programs/benchmarking/matrix/mul-{args.arch}")  # Use the Binary class to load the local binary
    board.set_se_binary_workload(binary)

    simulator = Simulator(board=board)
    simulator.run()

    #####################################################################################################################################

def copy(cache_file):
    command = ["mv","m5out/stats.txt", f"stats/{args.arch}_{cache_file}_{args.max}_{args.dim}.txt"]
    subprocess.run(command)
    
    
cache_file = "No_Cache"

if args.cache==1:
    cache_file = f"L1D{args.L1DSize}L1I{args.L1ISize}L2{args.L2Size}"
    
    
if not os.path.isfile(f"stats/{args.arch}_{cache_file}_{args.max}_{args.dim}.txt"):
    print(f"Simulating {cache_file}")
    process()
    copy(cache_file)
else:
    print(f"Already done {cache_file}")
