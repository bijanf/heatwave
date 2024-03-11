#!/bin/bash

#SBATCH --qos=short
#SBATCH --partition=standard
#SBATCH --account=gvca
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --job-name=preprocess
#SBATCH --output=slogs/out.%j
#SBATCH --error=slogs/err.%j

module load nco
module load cdo

set -e

# The year to process is passed as an argument to the script
year="$1"

var="tas"
input_dir="/p/projects/proclias/1km/data/chelsa_w5e5/nc/"
output_dir="/p/tmp/fallah/temp2/"

mkdir -p "$output_dir"

# Define the domain boundaries
lon_min=44.0
lon_max=91.0
lat_min=33.0
lat_max=56.5

# Process each month of the specified year
for month in $(seq -w 1 12); do
    filename="chelsa-w5e5v1.0_obsclim_tasmin_30arcsec_global_daily_${year}${month}.nc"
    input_filepath="${input_dir}/${filename}"
    if [ -f "$input_filepath" ]; then
        output_filepath="${output_dir}/subset_${filename}"
        ncks -d lon,$lon_min,$lon_max -d lat,$lat_min,$lat_max $input_filepath $output_filepath
        echo "Processed $input_filepath"
    else
        echo "File does not exist: $input_filepath"
    fi
done
