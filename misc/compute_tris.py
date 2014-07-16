#! /bin/env sage-python
#
#SBATCH --partition e
#SBATCH --tasks=1
#SBATCH --mem-per-cpu=4096
#SBATCH --nice=10000
#SBATCH --time=7-00:00
#SBATCH --output=slurm_out/%j
#SBATCH --error=slurm_out/%j

import taskdb
import knot_sample

def run_line(line):
    knot_sample.exterior(eval(line))
    return line, True

T = taskdb.TaskDatabase('exteriors')
T.run_function(run_line, num_tasks=1)

