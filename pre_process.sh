#!/bin/bash
#=============================================
#code to prepare the obs_hist,sim_hist,sim_fut
# and cut the domain for the Target
#=============================================
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



set -e
#var="pr tas"
#var="ps hurs"
#var="tasmax"
var="tasmin"
realizations="counterclim obsclim"
#realizations="obsclim"
#model="20CRv3"
#years="2011_2015"
#model="20CRv3-ERA5"
#years="2011_2020"
#model="20CRv3-W5E5"
#years="2011_2019"
#model="GSWP3-W5E5"
#years="2011_2019"
#model="20CRv3 20CRv3-ERA5 20CRv3-W5E5 GSWP3-W5E5"
model="GSWP3-W5E5"


years="1901_1910 1911_1920 1921_1930 1931_1940 1941_1950 1951_1960 1961_1970 1971_1980 1981_1990 1991_2000 2001_2010 2011_2019"


dir="/p/projects/isimip/isimip/ISIMIP3a/InputData/climate/atmosphere/"
post_dir="global/daily/historical/"
cdo_cmd_1=" -sellonlatbox,44,91,33,56.5 "
cdo_cmd_2=" -mergetime "
#cdo_cmd_3=" -timpctl,98 "
dir_work="/p/tmp/fallah/work_counter/"


# P R E P R O C E S S I N G #
preprocess="True"

if [ $preprocess == "True" ]
then

for vars in $var
do

for year in ${years}
do

mkdir -p ${dir_work}
for real in ${realizations}
do

for mod in ${model}
do
    mods=$(echo "${mod,,}")
    echo $mod $year $vars
    #20crv3-w5e5_obsclim_rlds_global_daily_1991_2000.nc
    cdo ${cdo_cmd_1} ${dir}/${real}/${post_dir}/${mod}/${mods}_${real}_${vars}_global_daily_${year}.nc ${dir_work}/${mods}_${real}_${vars}_global_daily_${year}_CA.nc

done #model

done #realization

done # years

done # var

fi # preprocess

# M E R G I N G #

for vars in $var
do
    for real in ${realizations}
    do
        for mod in ${model}
        do
            mods=$(echo "${mod,,}")
            cdo -O -mergetime ${dir_work}/${mods}_${real}_${vars}_global_daily_*_CA.nc ${dir_work}/${mods}_${real}_${vars}_CA_daily_1901_onwards.nc
        done #models
    done # realizations
done #vars
