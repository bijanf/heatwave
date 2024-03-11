#!/bin/bash

year_start=1979
year_end=2016

for year in $(seq $year_start $year_end); do
    sbatch pre_process_chelsa.sh $year
done
