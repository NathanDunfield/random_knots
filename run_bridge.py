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
KD = knot_db.KnotDatabase()

def tetrahedra(manifold):
    return manifold.num_tetrahedra()

def volume(manifold):
    return manifold.volume()

def chern_simons(manifold):
    return manifold.chern_simons()

def bridge(knot):
    return knot.morse_index()

def run_line(line):
    KD.compute_entry(int(line), 'bridge_number', bridge, 'knot')
    #KD.compute_alexander_magma(int(line))
    return line, True
    
T = taskdb.TaskDatabase('exteriors')
T.run_function(run_line, num_tasks=1)
