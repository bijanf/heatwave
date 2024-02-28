#!/bin/bash
#=============================================
#code to prepare the obs_hist,sim_hist,sim_fut
# and cut the domain for the Target
#=============================================
#SBATCH --qos=short
#SBATCH --partition=standard
#####SBATCH --partition=largemem
#SBATCH --account=gvca
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --job-name=HWMId
#SBATCH --output=slogs/out.%j
#SBATCH --error=slogs/err.%j
###SBATCH --mem=16G

module load nco
module load cdo

set -e
python3 hwmid.py
