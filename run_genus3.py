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
import knotgenus3
KD = knot_db.KnotDatabase()

def create_taskdb(name):
    df = knot_db.dataframe()
    da = df[df.alexander_magma_genus_bound != df.genus_upper_bound]
    da['genus_lower_bound'] = da.alexander_magma_genus_bound.fillna(0).astype(int)
    da.to_csv('/tmp/' + name, sep='\t', columns=['crossings','genus_lower_bound'], header=False, index=False)

def upper_bound(M, lower_bound=0):
    return knotgenus3.genus_upper_bound(M)

def run_line(line):
    crossings, lower = map(int, line.split('\t'))
    KD.compute_entry(crossings, 'genus_upper_bound', upper_bound, lower_bound=lower)
    ans = KD.get_entry(crossings, 'genus_upper_bound')
    return line, True   #lower == ans
    
T = taskdb.TaskDatabase('genus3')
T.run_function(run_line, num_tasks=1)

#create_taskdb('genus3')
