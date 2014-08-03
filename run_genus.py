#! /bin/env sage-python
#
#SBATCH --partition m
#SBATCH --tasks=1
#SBATCH --mem-per-cpu=4096
#SBATCH --nice=10000
#SBATCH --time=7-00:00
#SBATCH --output=slurm_out/%j
#SBATCH --error=slurm_out/%j

import taskdb
import knot_db
import knotgenus2
KD = knot_db.KnotDatabase()

def upper_bound(M, lower_bound=0):
    M.dehn_fill( (0,1) )
    return knotgenus2.genus_upper_bound(M)

def run_line(line):
    crossings, lower = map(int, line.split('\t'))
    KD.compute_entry(crossings, 'genus_upper_bound', upper_bound, lower_bound=lower)
    ans = KD.get_entry(crossings, 'genus_upper_bound')
    return line, lower == ans
    
#T = taskdb.TaskDatabase('genus')
#T.run_function(run_line, num_tasks=1)
