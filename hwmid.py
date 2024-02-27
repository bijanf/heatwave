import xarray as xr
import numpy as np
import pandas as pd

def print_green(message):
    print(f"\033[92m{message}\033[0m")

# Assuming you've already loaded your dataset
ds = xr.open_dataset('/p/tmp/fallah/work_counter/gswp3-w5e5_obsclim_tasmax_CA_daily_1901_onwards.nc')
#ds = xr.open_dataset('/p/tmp/fallah/work_counter/gswp3-w5e5_counterclim_tasmax_CA_daily_1901_onwards.nc')

tasmax = ds['tasmax']
print_green("Dataset loaded successfully.")

# Define the reference period
reference_start = '1961-01-01'
reference_end = '1990-12-31'
reference_period = tasmax.sel(time=slice(reference_start, reference_end))
print_green("Reference period defined.")

# Calculate the 90th percentile thresholds for each day of the year
percentiles = reference_period.groupby('time.dayofyear').reduce(np.nanpercentile, q=90, dim='time')
print_green("90th percentile thresholds calculated.")

# Function to find exceedances over the 90th percentile (heatwave days)
def find_exceedances(tasmax, percentiles):
    exceedances = tasmax.groupby('time.dayofyear') - percentiles
    return exceedances.where(exceedances > 0)

# Calculate exceedances
exceedances = find_exceedances(tasmax, percentiles)
print_green("Exceedances calculated.")

# Convert to a binary format: 1 for exceedance, 0 otherwise
heatwave_days = exceedances.notnull().astype(int)
print_green("Heatwave days identified.")

# Identify heatwave events: at least 3 consecutive days of exceedances
def identify_heatwave_events(heatwave_days):
    consecutive_days = heatwave_days.rolling(time=3, center=True).sum()
    heatwave_events = consecutive_days >= 3
    return heatwave_events

# Identify heatwave events
heatwave_events = identify_heatwave_events(heatwave_days)
print_green("Heatwave events identified.")

# Calculate the magnitude of each heatwave event (sum of exceedances during the event)
heatwave_magnitude = (exceedances * heatwave_events).groupby('time.year').sum()
print_green("Heatwave magnitudes calculated.")

# Calculate the maximum heatwave magnitude for each year (HWMId)
hwm_id = heatwave_magnitude.max(dim='year')
print_green("HWMId calculated for each year.")

# Save the result as a NetCDF file
output_path = '/p/tmp/fallah/work_counter/hwm_id_obsclim.nc'
#output_path = '/p/tmp/fallah/work_counter/hwm_id_counterclim.nc'

hwm_id.to_netcdf(output_path)
print_green(f"HWMId saved as a NetCDF file at {output_path}")
