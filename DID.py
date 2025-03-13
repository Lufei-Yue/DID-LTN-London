pip install pystats19
import pystats19
import pandas as pd
import geopandas as gpd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt

# Extract stats19 data
from pystats19.read import list_files

# List selected files
list_files(year=2023)

# Pull data
from pystats19.source import pull_file
pull_file('dft-road-casualty-statistics-collision-1979-latest-published-year.csv', data_dir="./data")
df = pd.read_csv('./data/dft-road-casualty-statistics-collision-1979-latest-published-year.csv')

# Filter data
filtered = df[(df['accident_year'] >= 2008) & (df['accident_year'] <= 2023)]
filtered.to_csv('filtered.csv')
filter = pd.read_csv('filtered.csv')
# Convert to point data
from shapely.geometry import Point

# Create GeoDataFrame for accidents
filtered['geometry'] = filtered.apply(lambda row: Point(row['location_easting_osgr'], row['location_northing_osgr']), axis=1)
gdf_filtered = gpd.GeoDataFrame(filtered, geometry='geometry')

# Set the coordinate reference system (CRS) to OSGB 1936 / British National Grid (EPSG:27700)
gdf_filtered.crs = {'init': 'epsg:27700'}

# LTN data
LTN_new = gpd.read_file('LTN_areas.geojson')
LTN_before = gpd.read_file('LTN.shp')

# Filter eligible LTNs
def analyze_ltn_data(csv_file):
 
    df = pd.read_csv('LTN_new.csv')

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    df['Date_Remov'] = pd.to_datetime(df['Date_Remov'], format='%d/%m/%Y', errors='coerce')

    start_date = pd.to_datetime('2020-01-01')
    end_date = pd.to_datetime('2022-01-31') 

    established_within_range = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Filter for LTNs that have not been removed 
    not_removed = established_within_range[ (established_within_range['Removed'] == 0) & (established_within_range['Date_Remov'].isnull())]

    return not_removed

csv_file = "LTN_new.csv"
filtered_ltns = analyze_ltn_data('LTN_new.csv')

# Buffer LTNs
gdf_LTN = gpd.GeoDataFrame(filtered_ltns, geometry='geometry')
gdf_LTN['geometry'] = gdf_LTN['geometry'].buffer(10)

# Set the coordinate reference system (CRS) to British National Grid (EPSG:27700)
gdf_LTN.crs = {'init': 'epsg:27700'}

# London data
# London out LTNs before 2020
London_original = gpd.read_file('London_Ward.shp')
London_2020 = gpd.overlay(London_original, LTN_before, how="difference")
London_2020.to_file("London_2020.shp")

# London out LTNs (eligible & before 2020)
London = gpd.overlay(London_2020, LTN_new, how="difference") 
London.to_file("London.shp")

# Merge data by 'district'
London = result.dissolve(by='DISTRICT')

# Load region data as GeoDataFrame
gdf_London = gpd.GeoDataFrame(London, geometry='geometry')

# Set the coordinate reference system (CRS) to British National Grid (EPSG:27700)
gdf_London.crs = {'init': 'epsg:27700'}

# Spatial join
spatial_London = gpd.sjoin(gdf_filtered, gdf_London, how='left', predicate='within')
spatial_LTN = gpd.sjoin(gdf_filtered, gdf_LTN, how='left', predicate='within')

# Save data
spatial_London.to_csv('spatial_London_all.csv', index=False)
spatial_LTN.to_csv('spatial_LTN_all.csv', index=False)

# Calculate accident counts
accident_counts_London = spatial_London.groupby(['DISTRICT', 'collision_year']).size().reset_index(name='count')
accident_counts_LTN = spatial_LTN.groupby(['LGA', 'collision_year']).size().reset_index(name='count')

# Save data
accident_counts_London.to_csv('accident_counts_London.csv', index=False)
accident_counts_LTN.to_csv('accident_counts_LTN.csv', index=False)

# Set time
# London data
start_year = 2008
end_year = 2023
years = list(range(start_year, end_year + 1))

accident_counts1 = (
    accident_counts_London[accident_counts_London['accident_year'].isin(years)]
    .pivot(index='DISTRICT', columns='accident_year', values='count')
    .reset_index()
)

# LTN data
start_year = 2008
end_year = 2023
years = list(range(start_year, end_year + 1))

accident_counts2 = (
    accident_counts_LTN[accident_counts_LTN['accident_year'].isin(years)]
    .pivot(index='LGA', columns='accident_year', values='count')
    .reset_index()
)

# Set column names
accident_counts1.columns = ['DISTRICT', 'count_2008_London', 'count_2009_London', 'count_2010_London', 'count_2011_London', 'count_2012_London', 'count_2013_London', 'count_2014_London', 'count_2015_London', 'count_2016_London', 'count_2017_London', 'count_2018_London', 'count_2019_London', 'count_2020_London', 'count_2021_London', 'count_2022_London', 'count_2023_London']
accident_counts2.columns = ['LGA', 'count_2008_LTN', 'count_2009_LTN', 'count_2010_LTN', 'count_2011_LTN', 'count_2012_LTN', 'count_2013_LTN', 'count_2014_LTN', 'count_2015_LTN', 'count_2016_LTN', 'count_2017_LTN', 'count_2018_LTN', 'count_2019_LTN', 'count_2020_LTN', 'count_2021_LTN', 'count_2022_LTN', 'count_2023_LTN']

# Save data
accident_counts1.to_csv('accident_counts1.csv', index=False)
accident_counts2.to_csv('accident_counts2.csv', index=False)

# Merge data
accident_counts = pd.merge(accident_counts1, accident_counts2, left_on='DISTRICT', right_on='LGA', how='outer')
accident_counts.to_csv('accident_counts_all.csv', index=False)

# Plot accident counts change
all = pd.read_csv('accident_counts_all.csv')

df = pd.DataFrame(all)

years = list(range(2015, 2025))
ltn_columns = [f"count_{year}_LTN" for year in years]
london_columns = [f"count_{year}_London" for year in years]

ltn_data = df[ltn_columns].sum()
london_data = df[london_columns].sum()


fig, ax1 = plt.subplots(figsize=(12, 6))

color = '#D95319'
ax1.plot(years, ltn_data, linestyle='-', linewidth=2, marker='o', markersize=5, color=color, label='inside LTNs')
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Accident Count inside LTNs', fontsize=12)
ax1.tick_params(axis='y')

ax2 = ax1.twinx() 
color = '#0072BD'
ax2.plot(years, london_data, linestyle='-', linewidth=2, marker='s', markersize=5, color=color, label='outside LTNs')
ax2.set_ylabel('Accident Count outside LTNs', fontsize=12)
ax2.tick_params(axis='y')

ax1.set_xticks(years)
# add legend
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95), bbox_transform=fig.transFigure, fontsize=10)

fig.tight_layout() 
plt.title('Accident Counts inside and outside LTNs')
plt.show()

# Difference-in-differences analysis
# Traditionlal DID model
# Set time scale
start_year = 2015
end_year = 2024
years = list(range(start_year, end_year + 1))

# Remove data for 2020
years_no_2021 = [year for year in years if year != 2021]
ltn_cols = [f'count_{year}_LTN' for year in years_no_2021]
london_cols = [f'count_{year}_London' for year in years_no_2021]
df = df[['LGA'] + ltn_cols + london_cols]
df_long = pd.melt(df, id_vars=['LGA'], value_vars=ltn_cols + london_cols,
                   var_name='year_LTN', value_name='count')

df_long['year'] = df_long['year_LTN'].str.extract(r'(\d{4})').astype(int)
df_long['treatment'] = df_long['year_LTN'].str.contains('_LTN').astype(int)
df_long['post'] = (df_long['year'] >= 2021).astype(int)
df_long['interaction'] = df_long['treatment'] * df_long['post']

model_poisson = glm(
    'count ~ treatment + post + interaction',
    data=df_long, family=sm.families.Poisson()
).fit()

print(model_poisson.summary())

# Calculate R2
null_model = glm('count ~ 1', data=df_long, family=sm.families.Poisson()).fit()
# McFadden's Pseudo R²
pseudo_r2 = 1 - (model_poisson.llf / null_model.llf)
print(f"McFadden's Pseudo R²: {pseudo_r2:.4f}")

# Improved DID model
# Load data
all = pd.read_csv('accident_counts.csv')
df = pd.DataFrame(all)

# Set time scale
start_year = 2015
end_year = 2024
years = list(range(start_year, end_year + 1))

# Remove data for 2020 and 2021
years_no_2021 = [year for year in years if year != 2021 and year != 2020]

ltn_cols = [f'count_{year}_LTN' for year in years_no_2021]
london_cols = [f'count_{year}_London' for year in years_no_2021]
available_cols = ltn_cols + london_cols

df = df[['LGA'] + available_cols]
df_long = pd.melt(df, id_vars=['LGA'], value_vars=available_cols,
                   var_name='year_LTN', value_name='count')

df_long['year'] = df_long['year_LTN'].str.extract(r'(\d{4})').astype(int)
df_long['treatment'] = df_long['year_LTN'].str.contains('_LTN').astype(int)
df_long['post'] = (df_long['year'] >= 2021).astype(int)
df_long['timebefore'] = np.where(df_long['year'] <= end_year, df_long['year'] - start_year, 0)
df_long['timeafter'] = np.where(df_long['year'] >= 2021, df_long['year'] - 2020, 0)
df_long['interaction_post'] = df_long['treatment'] * df_long['post']
df_long['interaction_timeafter'] = df_long['treatment'] * df_long['timeafter']
df_long['interaction_timebefore'] = df_long['treatment'] * df_long['timebefore']

model_poisson = glm(
    'count ~ treatment + post + interaction_post + timebefore + timeafter + interaction_timebefore + interaction_timeafter',
    data=df_long, family=sm.families.Poisson()
).fit()

print(model_poisson.summary())
