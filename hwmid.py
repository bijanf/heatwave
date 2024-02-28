from cdo import Cdo
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

nday = 20
T=7
cdo = Cdo()

# Define input files
input_file1 = '/p/tmp/fallah/work_counter/gswp3-w5e5_counterclim_tasmax_CA_daily_1901_onwards.nc'
input_file2 = '/p/tmp/fallah/work_counter/gswp3-w5e5_obsclim_tasmax_CA_daily_1901_onwards.nc'

# Set reference period
reference_period = "1900/1929"  # Adjusted to your new reference period

# Calculate daily minimum and maximum temperatures for the reference period for both files
min_temp_file1 = "min_temp_file1.nc"

min_temp_file2 = "min_temp_file2.nc"


cdo.ydaymean(input=f"-selyear,{reference_period} {input_file1}", output=min_temp_file1)
#cdo.ydaymax(input=f"-selyear,1900/2019", output=max_temp_file1)
cdo.ydaymean(input=f"-selyear,{reference_period} {input_file2}", output=min_temp_file2)
#cdo.ydaymax(input=f"-selyear,1900/2019", output=max_temp_file2)


# Calculate HWDI for both datasets
hwdi_file1 = "hwdi_file1.nc"
hwdi_file2 = "hwdi_file2.nc"

# Assuming nday and T values are correctly chosen for your analysis
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
