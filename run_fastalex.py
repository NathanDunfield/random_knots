#! /bin/env sage-python
#
#SBATCH --partition m
#SBATCH --tasks=1
#SBATCH --mem-per-cpu=4096
#SBATCH --nice=10000
#SBATCH --time=7-00:00
#SBATCH --output=slurm_out/%j
#SBATCH --error=slurm_error/%j

import taskdb2, knot_db
KD = knot_db.KnotDatabase()

def fastalex(task):
    KD.compute_alexander_dror(int(task['name']))
    task['done'] = True

T = taskdb2.TaskDatabase('fastalex')
T.run_function(fastalex, num_tasks=1)
