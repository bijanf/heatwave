"""
This script processes climate data to analyze and visualize differences in Heatwave Duration Index (HWDI) 
between two distinct climate datasets over a specified reference period. The analysis involves several key steps:
1. Utilizing Climate Data Operators (CDO) to calculate the daily mean temperatures during the reference period 
for both datasets, which aids in identifying heatwave days based on a defined temperature threshold.
2. Calculating the Heatwave Duration Index (HWDI) for both datasets. HWDI measures the total duration of heatwaves over a year,
providing insights into the intensity and frequency of heatwaves under different climatic conditions. It is calculated by identifying 
consecutive days where the temperature exceeds a certain threshold above the reference period's mean temperature.
3. Comparing the HWDI between the two datasets to understand variations in heatwave characteristics, which could be indicative of 
changes due to factors like climate change or different climate models.
4. Visualizing the difference in HWDI on a geographic map using matplotlib and cartopy. This step involves plotting the geographical
distribution of HWDI differences, highlighting areas with significant changes in heatwave durations.
Dependencies include CDO for climate data manipulation, xarray for handling multi-dimensional arrays, matplotlib for visualization,
and cartopy for geospatial data processing. This script is particularly useful for climate researchers and analysts looking to understand 
the impacts of climatic conditions on heatwave patterns.
"""
from cdo import Cdo
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

nday = 20 # Number of consecutive days to consider for a heatwave
T=7  # Temperature threshold above which a day is considered part of a heatwave
cdo = Cdo()

# Define input files
input_file1 = '/p/tmp/fallah/work_counter/gswp3-w5e5_counterclim_tasmax_CA_daily_1901_onwards.nc' #counterfactual cliamte data 
input_file2 = '/p/tmp/fallah/work_counter/gswp3-w5e5_obsclim_tasmax_CA_daily_1901_onwards.nc' #factual climate data 

# Set reference period
reference_period = "1900/1929"  # Adjusted to your new reference period

# Calculate daily minimum and maximum temperatures for the reference period for both files
min_temp_file1 = "min_temp_file1.nc"

min_temp_file2 = "min_temp_file2.nc"


cdo.ydaymean(input=f"-selyear,{reference_period} {input_file1}", output=min_temp_file1)
#cdo.ydaymax(input=f"-selyear,1900/2019", output=max_temp_file1)
cdo.ydaymean(input=f"-selyear,{reference_period} {input_file2}", output=min_temp_file2)
#cdo.ydaymax(input=f"-selyear,1900/2019", output=max_temp_file2)


# Calculate the Heatwave Duration Index (HWDI) for both datasets
# HWDI is calculated as follows:
# 1. Identify all periods of at least 'nday' consecutive days where the daily maximum temperature
#    exceeds a temperature threshold 'T' above the reference period mean.
# 2. For each identified period, count the number of days that meet the criteria.
# 3. The HWDI is the sum of all such periods' lengths over the year, providing a measure of
#    the total duration of heatwaves within that year.
hwdi_file1 = "hwdi_file1.nc"
hwdi_file2 = "hwdi_file2.nc"


# Assuming 'nday' and 'T' values are correctly chosen for your analysis,
# use CDO to calculate HWDI, comparing each dataset against its own reference period mean temperature.
cdo.eca_hwdi(f"{nday},{T} {input_file1} {min_temp_file1}", output=hwdi_file1)
cdo.eca_hwdi(f"{nday},{T} {input_file2} {min_temp_file2}", output=hwdi_file2)

# Load HWDI datasets
hwdi_ds1 = xr.open_dataset(hwdi_file1)
hwdi_ds2 = xr.open_dataset(hwdi_file2)

# Assuming the variable storing HWDI in your NetCDF files is named 'hwdi'; adjust as necessary
# Calculate difference
hwdi_diff = -hwdi_ds1['heat_wave_duration_index_wrt_mean_of_reference_period'] +  hwdi_ds2['heat_wave_duration_index_wrt_mean_of_reference_period']


# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Add country borders and coastlines
ax.add_feature(cfeature.BORDERS, linestyle='-', linewidth=1, edgecolor='k')
ax.add_feature(cfeature.COASTLINE, linewidth=1.0, edgecolor='black')

# Plot HWDI difference
hwdi_diff.plot(ax=ax, transform=ccrs.PlateCarree(),
               cmap='coolwarm', vmin=-200, vmax=200,  # Example color map and limits
               cbar_kwargs={'shrink': .7, 'label': 'HWDI Difference\n obsclim minus counterclim'})

# Title and labels
ax.set_title('', fontsize=14)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)

# Save the figure without white space around it
plt.savefig('HWDI_Difference_Map_'+str(nday)+'_'+str(T)+'.png', bbox_inches='tight', pad_inches=0)
plt.close(fig)  # Close the figure window after saving to free up memory
