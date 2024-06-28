#!/usr/bin/env python
# coding: utf-8

# Python script version of data_cleaning.ipynb


# Imports


# This is an uncommon library so we run a pip install of it just in case
get_ipython().system('pip install geopandas shapely')

# Common imports
import pandas as pd # Pandas for storing and manipulating CSV files as DataFrames (tables)
import geopandas as gpd # Geopandas for converting coordinates to states
from shapely.geometry import Point # Same as Geopandas
import numpy as np # Numpy for storing and manipulating arrays (lists)
import math # Math for finding NaN values
import os # OS for writing and reading directories (folders)
import time # Time for checking how long things take
from sklearn.ensemble import IsolationForest # Isolation Forests for anomaly detection


# Previewing Original Citizen Data


df = pd.read_csv("../data/original_citizen_data/alldata.csv") # Load raw citizen data in


# # Handling Incorrect -2 Values


# Replacing incorrect -2 values with either NA or -2
all_species = list(df['Species_name'].value_counts().index) # All species names in order of frequency
phenophases = list(df.columns[9:]) # Phenophase column names

def create_species_dict(*absent_phenophases):
    """
    Creates a dictionary informing if each phenophase is seen in a species or not (0 for seen, 1 for not seen)

    Args:
        absent_phenophase (List(string)): List of phenophases not seen in a species
        use_q (bool):  False means use MDP value iteration, true means use Q-learning
    Returns:
        species_dict (Dict(string,int)): A Dictionary mapping phenophases to binaries indicating presence in a species
    """
    species_dict = dict(zip(phenophases, np.zeros(len(phenophases), int)))
    for phenophase in absent_phenophases:
        species_dict[phenophase] = 1
    return species_dict

handbook_dicts = {} # Dict mapping species to species dicts. 
# Below are manually input absent phenophases for each species in the citizen dataset. Labels derived from SeasonWatch Tree Phenology Guide
handbook_dicts[all_species[0]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[1]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[2]] = create_species_dict('Flowers_open', 'Fruits_open')
handbook_dicts[all_species[3]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[4]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[5]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[6]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[7]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[8]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[9]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[10]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[11]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[12]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[13]] = create_species_dict('Flowers_bud', 'Flowers_open', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[14]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[15]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[16]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[17]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[18]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[19]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[20]] = create_species_dict('Flowers_bud', 'Flowers_open', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[21]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[22]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[23]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[24]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[25]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[26]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[27]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[28]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[29]] = create_species_dict('Flowers_bud', 'Flowers_open', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[30]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[31]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[32]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[33]] = create_species_dict('Flowers_bud', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[34]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[35]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[36]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[37]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[38]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[39]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[40]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[41]] = create_species_dict('Flowers_open', 'Fruits_open')
handbook_dicts[all_species[42]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[43]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[44]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[45]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[46]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[47]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[48]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[49]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[50]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[51]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[52]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[53]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[54]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[55]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[56]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[57]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[58]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[59]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[60]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[61]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[62]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[63]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[64]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[65]] = create_species_dict('Flowers_open', 'Fruits_open') # Silkworm Mulberry
handbook_dicts[all_species[66]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[67]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[68]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[69]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[70]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[71]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[72]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[73]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[74]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[75]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[76]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[77]] = create_species_dict('Flowers_open', 'Fruits_open') # Box-myrtle
handbook_dicts[all_species[78]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[79]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[80]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Airi Mango
handbook_dicts[all_species[81]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[82]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[83]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[84]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[85]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[86]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[87]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[88]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[89]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[90]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[91]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[92]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[93]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[94]] = create_species_dict('Flowers_open') # Wild Almond
handbook_dicts[all_species[95]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[96]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[97]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[98]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[99]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[100]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[101]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[102]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[103]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[104]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Alphonso Mango
handbook_dicts[all_species[105]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[106]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[107]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[108]] = create_species_dict('Flowers_open')
handbook_dicts[all_species[109]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[110]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[111]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[112]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[113]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[114]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[115]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Aabehayat Mango
handbook_dicts[all_species[116]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[117]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[118]] = create_species_dict('Flowers_bud', 'Flowers_open', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[119]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[120]] = create_species_dict('Flowers_open')
handbook_dicts[all_species[121]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[122]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[123]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[124]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[125]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[126]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[127]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[128]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[129]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Manjeera Mango
handbook_dicts[all_species[130]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[131]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[132]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[133]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[134]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[135]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[136]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[137]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[138]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[139]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[140]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[141]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[142]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[143]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[144]] = create_species_dict('Flowers_male', 'Flowers_Female') # Blue Pine
handbook_dicts[all_species[145]] = create_species_dict('Flowers_open')
handbook_dicts[all_species[146]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[147]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[148]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[149]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[150]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[151]] = create_species_dict('Flowers_open', 'Fruits_open') # Indian Charcoal Tree
handbook_dicts[all_species[152]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[153]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[154]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[155]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[156]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[157]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[158]] = create_species_dict('Flowers_open')
handbook_dicts[all_species[159]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[160]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Mallika Mango
handbook_dicts[all_species[161]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[162]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[163]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[164]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[165]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[166]] = create_species_dict('Flowers_open','Fruits_open') # Mohru Oak
handbook_dicts[all_species[167]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[168]] = create_species_dict('Flowers_bud', 'Flowers_open', 'Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[169]] = create_species_dict('Flowers_male', 'Flowers_Female')
handbook_dicts[all_species[170]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[171]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[172]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Chosa Mango
handbook_dicts[all_species[173]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open')
handbook_dicts[all_species[174]] = create_species_dict('Flowers_male', 'Flowers_Female', 'Fruits_open') # Olour Mango
handbook_dicts[all_species[175]] = create_species_dict('Flowers_open','Fruits_open')
handbook_dicts[all_species[176]] = create_species_dict('Flowers_bud', 'Flowers_male', 'Flowers_Female', 'Fruits_open')

# Replace Incorrect -2 Values
for species in all_species:
    species_df = df[df['Species_name'] == species]
    species_dict = handbook_dicts[species]
    for phenophase in phenophases:
        if species_dict[phenophase] == 0: # Phenophase seen in species
            false_positive_idx = species_df.index[species_df[phenophase] == -2] # Indices of reports that incorrectly assign -2 values (false positive) to phenophases SEEN in the species
            df.loc[false_positive_idx, phenophase] = np.full(len(false_positive_idx),np.nan) # Turn all false positives into NaN values (these observations will later be dropped)
        if species_dict[phenophase] == 1: # Phenophase NOT seen in species
            false_negative_idx = species_df.index[species_df[phenophase] != -2] # Indices of reports that incorrectly assign values other than -2 (false negative) to phenophases NOT SEEN in the species
            df.loc[false_negative_idx, phenophase] = np.full(len(false_negative_idx),-2.0) # Turn all false negatives into -2 values


# Combining Mango Varieties


# Combining all mango varieties under the Species_name of Mango (all varieties)- Mangifera indica
df['Species_name'] = df['Species_name'].replace(to_replace=r'\w* Mango- Mangifera indica', value='Mango (all varieties)- Mangifera indica', regex=True)


# Filling in Missing States


states_shapefile = gpd.read_file("../data/india_map/gadm41_IND_3.shp") # Load map of India with states as a coordinate grid with labels

# Function for filling state_name attribute based on coordinates for observations with NA state_name
def find_indian_state(latitude, longitude, gdf):
    """
    Finds the state name associated with a set of coordinates

    Args:
        latitude, longitude (int, int): Latitude and longitude coordinates
        gdf (GeoDataFrame): Coordinate grid of India with states labeled
    Returns:
        state['NAME_1'] (string): If coordinates map to somewhere within India, return state name
        None (None): Else, return None because the coordinates are unreliable
    """
    
    point = Point(longitude, latitude)
    
    for _, state in gdf.iterrows():
        if state['geometry'].contains(point):
            return state['NAME_1']
    return None

# Fill any missing state names in dataset
print("Started Filling Missing States")
import time 
start_time = time.time() # Measuring Time
counter = 0 # Number of observations checked so far
observations_missing_state_name = df[df["State_name"].isna()].drop(['State_name'], axis=1).dropna(how='any') # Taking a subset of citizen observations with all columns recorded (not NaN/Null/None) except State_name
for idx, row in observations_missing_state_name.iterrows(): # Iterate over observations missing a state name
    if (counter % 1000) == 0: # Report time every 1000 observations
        print(f"{counter}: {time.time()-start_time} seconds elapsed; {counter/len(observations_missing_state_name)*100}% Done")
    df.at[idx, "State_name"] = find_indian_state(row["Lat"], row["Long"], states_shapefile) # Add state name based on coordinates (if coordinates are reliable)
    counter += 1
# In case any states are labeled as a name inconsistent with our dataset
df['State_name'] = df['State_name'].replace('Andaman and Nicobar', 'Andaman and Nicobar Islands') # Two names for Andaman and Nicobar Islands
df['State_name'] = df['State_name'].replace('NCT of Delhi', 'Delhi') # Two names for Delhi
print(f"Finished Filling Missing States in {time.time()-start_time} seconds")


# Dropping NAs


# Drop observations with Null/NaN/None values and sort by species name
df = df.drop(df.columns[0], axis=1) # Drop the index column called "Unnamed: 0"
df = df.dropna(how='any') # Drop any observation with at least one NaN/Null/None value reported
df = df.sort_values(by='Species_name') # Order data by species for organization


# Reformatting & Adding Date Columns


# Reformats df to Year, Week formatting to match the reference data
df["Date_of_observation"] = pd.to_datetime(df["Date_of_observation"], format='mixed') # Change Date_of_observation column to datetime format/datatype

df["Year"] = df["Date_of_observation"].dt.isocalendar().year # Extract the year of each observation from the date column

"""
!!! Use the following instead if 52 weeks are wanted !!!
df["Year"] = df["Date_of_observation"].dt.isocalendar().week
Warning: 52nd week will only be 1 or 2 days depending on if it's a leap year or not
"""

# Weeks are 48 weeks instead of 52 because this follows the format of the reference data
df["Week"] = df["Date_of_observation"].dt.dayofyear // (366/48+0.0000000000001) # Week durations vary between 7 or 8 days (~50% of weeks are 7 days long. ~50% of weeks are 8 days long)
df["Week"] = df["Week"].astype(int) # Convert Week column from decimal to integer

"""
dt.dayofyear gives an index starting at 1, thus use 366 in equation for leap years
Add 0.0000000000001 bias to 48 (number of weeeks) so week is in range [0,47] instead of [0,48]
"""


# Anomaly Detection


def outlier_detection(df, num_trees=500): 
    """
    Helper function for anomaly_detection_overall. Gives indices of anomalous observations.

    Args:
        df (DataFrame): Observations spanning at least an entire year. Observations are preferably of the same species within the same state.
        num_trees (int): Number of trees making up an isolation forest. Higher number of trees reduces variance but slows down training.
    Returns:
        invalid_indices (List(int)): Index values in citizen data associated with observations deemed outliers by an isolation forest (invalid).
    """
    
    df = df.drop(["Date_of_observation", "Observation_ID", "User_id", "User_Tree_id", "State_name", "Species_name", "Year"], axis=1) # Drop columns not used in training
    
    model = IsolationForest(n_estimators = num_trees, contamination = 0.08, verbose = 1, random_state = 42) # Generate isolation forest
    # Note: Higher contamination score means more false positive outliers; Lower contamination score means more false negative outliers
    
    invalid_indices = []
    
    for week in df["Week"].sort_values().unique(): # Iterate over each week
        week_df = df[df["Week"] == week] # Use only observations from the current week
        week_df = week_df.drop("Week", axis=1) # Drop week column because it is not used in training
        
        model.fit(week_df) # Train isolation forest on particular week
        preds = model.predict(week_df) # Predict if each observation is an outlier
        week_df["Predictions"] = preds # Add prediction to observation data
        
        invalid_indices += list(week_df[week_df["Predictions"] == -1].index) # Record indices of outliers from the given week
    return invalid_indices 

def anomaly_detection_overall(df, min_observations_for_outlier_detection):
    """
    Performs anomaly detection on entire dataset

    Args:
        df (DataFrame): All citizen data
        min_observations_for_outlier_detection (int): Minimum number of observations in a subset of the data for anomaly detection to be performed
    Returns:
        invalid_indices (List(int)): Index values in citizen data associated with observations deemed outliers by isolation forests (invalid).
    """
    print("Started Anomaly Detection")
    start_time = time.time() # Time
    invalid_indices = []
    states = df["State_name"].unique() # All states in dataset
    for state in states: # Iterate over all states
        print(f"**********{state}**********")
        state_start_time = time.time() # Time
        state_df = df[df["State_name"] == state] # Only observations from the given state
        years = state_df["Year"].sort_values().unique() # All years data was recorded in the given state
        for year in years: # Iterate over each year
            print(f"**********{year}**********")
            year_start_time = time.time() # Time
            state_year_df = state_df[state_df["Year"] == year] # Only observations in the given year from the given state
            species_list = state_year_df["Species_name"].unique() # All species in the given year from the given state
            for species in species_list: # Iterate over each species
                species_state_year_df = state_year_df[state_year_df["Species_name"] == species] # Only observations of the given species in the given year from the given state
                if len(species_state_year_df) > min_observations_for_outlier_detection: # Verifying there are enough observations for anomaly detection
                    species_start_time = time.time() # Time
                    outliers = outlier_detection(species_state_year_df) # Run outlier detection on observations
                    invalid_indices += outliers # Record indices of outliers
                    print(f"{len(outliers)}/{len(species_state_year_df)} observations invalid in {species} in {year} in {state}") # Outlier count
                    print(f"Finished {species} in {state} during {year} in {time.time()-species_start_time} seconds") # Time
            print(f"Finished {state} during {year} in {time.time()-year_start_time} seconds") # Time
        print(f"Finished {state} in {time.time()-state_start_time} seconds") # Time
    print(f"{len(invalid_indices)}/{len(df)} observations invalid overall") # Total outlier count
    print(f"Finished Anomaly Detection completely in {time.time()-start_time} seconds") # Time
    return invalid_indices

# Run anomaly detection on all citizen data and drop any anomalies
invalid_indices = anomaly_detection_overall(df, 15*52) # Choose 15*52 as the min num of observations because it means there's an average of 15 observations per week
df = df.drop(invalid_indices) # Drop observations deemed outliers


# Species ID <-> Name Dicts


# Load species lookup dicts for id <-> name from species_codes.csv
species_codes = pd.read_csv("../data/species codes.csv", encoding='unicode_escape')

species_id_to_name = {}
species_name_to_id = {}

# Creating species id <-> name dictionaries
# Refomatting species names from "species codes.csv" to match those of the citizen data
# Load the reformatted data to dictionaries for converting species_name to species_id and vice versa
for i, row in species_codes.iterrows():
    species_id_to_name[row["species_id"]] = "{}-{}".format(row["species_primary_common_name"], row["species_scientific_name"])
    species_name_to_id["{}-{}".format(row["species_primary_common_name"], row["species_scientific_name"]).lower().replace(" ", "")] = row["species_id"]


# Encoding and Decoding Species ID & Species Names in Citizen Data


# Reformat species names in citizen data
print("Started Reformatting Species Names")
for i, row in df.iterrows():
    name = row["Species_name"].lower().replace(" ", "") # Reformat species names

    # Change formatting of species names within citizen observations to be standardized & consistent with reference data
    if name == "arjuntree-terminaliaarjuna": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1083]
        continue
    if name == "axlewoodtree-anogeissuslatifolia": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1009]
        continue
    if name == "chiku-sapodilla-manilkarazapota\xa0": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1188]
        continue
    if name == "dyer'soleander-wrightiatinctoria": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1181]
        continue
    if name == "ficusmollis-softfig":
        df.loc[i, "Species_name"] = species_id_to_name[1197]
        continue
    if name == "frangipani-templetree-plumeriarubra": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1176]
        continue
    if name == "garuga-kharpat-garugapinnata": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1038]
        continue
    if name == "ghostrree-sterculiaurens": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1078]
        continue
    if name == "indianfrankincense-boswelliaserrata": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1195]
        continue
    if name == "indiancoraltree-erythrinaindica": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1034]
        continue
    if name == "kadamba-neolamarckiacadamba": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1058]
        continue
    if name == "lanneacoromandelica-indianashtree": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1194]
        continue
    if name == "mexicanoleander-yellowoleander-cascabelathevetia": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1177]
        continue
    if name == "nightfloweringjasmine-harsingar-nyctanthesarbor-tristis": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1059]
        continue
    if name == "prosopiscineraria-khejri": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1201]
        continue
    if name == "raintree-samaneasaman": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1162]
        continue
    if name == "redsilk-cotton-bombaxceiba": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1015]
        continue
    if name == "whitesilk-cotton-ceibapentandra": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1021]
        continue
    if name == "yellow-silkcottontree-cochlospermumreligiosum": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1023]
        continue
    if name == "karkat-dogteak-dilleniapentagyna": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1032]
        continue
    if name == "chosamango-mangiferaindica": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1108]
        continue
    if name == "falsewhiteteak-mallotusnudiflorus": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1088]
        continue
    if name == "floss-silktree-ceibaspeciosa": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1022]
        continue
    if name == "largesebesten-bairola-cordiawallichii": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1026]
        continue
    if name == "roxburghskydia-pulia-kydiacalycina": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1044]
        continue
    if name == "wildrose-rosawebbiana": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1206]
        continue
    if name == "albiziaodoratissima-blacksiris": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1199]
        continue
    if name == "anogeissuspendula-kardhai": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1198]
        continue
    if name == "brokenbonestree-oroxylumindicum": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = "Broken Bones Tree-Oroxylum Indicum"
        continue
    if name == "pyinmatree-andamancrapemyrtle-lagerstroemiahypoleuca": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1216]
        continue
    if name == "crataevareligiosa-garlic-peartree": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1196]
        continue
    if name == "guh-de-three-leafcapertree-cratevaadansonii": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1217]
        continue
    if name == "aabehayatmango-mangiferaindica": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1091]
        continue
    if name == "bedu-punjabfig-ficuspalmata": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1235]
        continue
    if name == "chinar-platanusorientalis": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = "Chinar-Platanus Orientalis"
        continue
    if name == "prunusnepalensis-sohiong": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1192]
        continue
    if name == "tecomellaundulata-roheda": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = species_id_to_name[1200]
        continue
    if name == "tigersmilkspruce-falconeriainsignis": # If statements to catch any misspellings or missing entries in species codes.csv
        df.loc[i, "Species_name"] = "Tiger's Milk Spruce-Falconeria Insignis"
        continue
    if species_name_to_id[name]: # General case with no misspellings
        df.loc[i, "Species_name"] = species_id_to_name[species_name_to_id[name]] # species dictionaries to undo the .lower().replace(" ","") formatting

# Adding a Species_id column to the citizen data for comparing to the reference database
df.insert(loc = 4, column = 'Species_id', value = [species_name_to_id.get(species.lower().replace(" ",""), np.nan) for species in df["Species_name"]])
print("Finished Reformatting Species Names")


# Save Updated Citizen Data in One File


# Save updated_alldata.csv to disk
df.to_csv('../data/cleaned_alldata.csv', index=False)


# Make Directories for Citizen and Reference Data


# Create directories for storing citizen and reference data.
os.makedirs("../data/citizen_states_cleaned", exist_ok=True)
os.makedirs("../data/reference_states_cleaned", exist_ok=True)


# State DFs to all data/citizen folder\


# Saving separate CSV files for citizen observations based on state
for state_name in df["State_name"].unique(): # Iterate over all states
    state_df = df[df["State_name"] == state_name] # Only use observations from given state
    state_df = state_df.drop(["State_name"], axis = 1) # Drop State_name column because it is the same value throughout each CSV file
    state_name = state_name.replace(" ","_").lower() # Reformat state names to lowercase with _ instead of spaces
    state_df.to_csv(f"../data/citizen_states_cleaned/{state_name}.csv", index=False) # Save citizen observations in the given state to disk


# Reference Data Cleaning


# Dicts and Functions

# Dictionary mapping reference data acronyms to citizen data phenophase names
acronym_to_phenophase_dict = {'FL': 'Leaves_fresh', 'ML': 'Leaves_mature', 'DL': 'Leaves_old', 
                              'BD': 'Flowers_bud', 'OF': 'Flowers_open', 'MF': 'Flowers_male', 
                              'FF': 'Flowers_Female', 'UFR': 'Fruits_unripe', 'RFR': 'Fruits_ripe', 
                              'OFR': 'Fruits_open'} 

# Dictionary mapping reference data phenophase values (strings) to citizen data phenophase values (int or None)
str_to_val_dict = {'NA': None, '': None, '0': 0, '1': 1, '2': 2} 

def split_reformat_code(code):
    """
    Converts phenophase acronyms to phenophase names (e.g. 'FL' -> 'Leaves_fresh')

    Args:
        code (string): Phenophase acronym and value stored as one string
    Returns:
        code_attr_tup (tuple(string, int or None)): Phenophase acronym and value stored in tuple
    """
    code_attr_tup = code.split('_') # Split code into acronym and value
    code_attr_tup[0] = acronym_to_phenophase_dict[code_attr_tup[0]] # Phenophase acronym -> Phenophase name
    code_attr_tup[1] = str_to_val_dict[code_attr_tup[1]] # Phenophase value (string) -> Phenophase value (int or None)
    code_attr_tup = tuple(code_attr_tup) # Convert from list to tuple
    return code_attr_tup

def clean_df(df):
    """
    Cleans Reference Data:
        Adds new columns: everything in df that is not a month, plus the 10 categorical codes, plus a 'week' column

    Args:
        df (DataFrame): Reference data for a certain state
    Returns:
        new_df (DataFrame): Cleaned reference data for a certain state
    """
    
    df = df.drop_duplicates() # Drop reference data for species with duplicate yearly observations
    
    week_codes = list(df.columns[3:-2]) # Names of week columns
    base_cols = list(df.columns[:3]) + [df.columns[-1]] # Names of non-week columns excluding created_at (excluding this column acts as dropping it)
    
    new_cols = base_cols + ['week'] + list(acronym_to_phenophase_dict.values()) # Names of columns used in cleaned reference data
    
    new_df = pd.DataFrame(columns=new_cols) # Initialize new DataFrame with the finalized columns

    num_idxs = len(df) # Total number of indices of input reference data
    
    for idx, row in df.iterrows(): # Iterate over rows in input reference data
                  
        if idx % 10 == 0: # Every 10 iterations...
            print("{} % done".format(100 * idx / num_idxs)) # Progress update
        
        # Add records (rows) to the new DataFrame for each week (48 rows per species) with phenophases as columns
        for week_idx, week_code in enumerate(week_codes): # Iterate over the 48 week columns
            new_record = {} # Initialize new record to put into the new DataFrame
            for old_colname in base_cols: # Iterate over non-week columns excluding created_at
                new_record[old_colname] = row[old_colname] # Carry the values from the non-week columns over to the new DataFrame
            new_record['week'] = week_idx # Add the associated week to the new record
            phenophase_vals_for_week = row[week_code] # String of phenophase values for the associated week
            # e.g. "FL_NA,ML_NA,DL_NA,BD_NA,OF_NA,MF_NA,FF_NA,UFR_NA,RFR_NA,OFR_NA"

            # Add new record if phenophase values are all Null
            if math.isnan(phenophase_vals_for_week): # If phenophase values is Null/NaN/None...
                for phenophase in acronym_to_phenophase_dict.values(): # Iterate over phenophase names
                    new_record[phenophase] = None # Add None as the phenophase values to the new record
                new_df.loc[len(new_df)] = new_record # Add the new record to the new DataFrame
            
            # Add new record in typical case
            else:
                phenophase_val_list = list(map(split_reformat_code, phenophase_vals_for_week.split(","))) # Phenophase names and their associated values
                for (phenophase, value) in phenophase_val_list: # Iterate over phenophase names and values
                    new_record[phenophase] = value # Add phenophase values to the new record

                new_df.loc[len(new_df)] = new_record # Add the new record to the new DataFrame
    
    # Remove unnamed columns if they exist
    for col in new_df.columns: # Iterate over all columns in the new DataFrame
        if 'Unnamed' in col or col == 'id': # If given column is unnamed or the id column...
            new_df = new_df.drop(col, axis=1) # Drop given column
    
    # Adding species_name column
    new_df['species_name'] = new_df['species_id'].map(species_id_to_name) # Map species id to the associated species name

    return new_df


# Saving Cleaned Reference Data Files


# Clean all pvt tables & save them to disk in reference folder
print("Started Cleaning Reference Data")
for tablename in os.listdir('../data/original_reference_data/pvttables_raw/'): # Iterate through pvt tables
    if tablename == '.DS_Store': # Ignore this file 
        continue
    print("cleaning {}".format(tablename))
    ref_df = pd.read_csv('../data/original_reference_data/pvttables_raw/{}'.format(tablename), sep=';') # Load the given pvt table
    tablename = tablename.replace("pvt_","") # Reformat table name
    if tablename == 'maharastra.csv': # Fix misspelling
        tablename = 'maharashtra.csv'
    new_df = clean_df(ref_df) # Clean reference data
    new_df.to_csv('../data/reference_states_cleaned/{}'.format(tablename), index=False) # Save cleaned reference data to disk in reference folder
print("Finished Citizen and Reference Data Cleaning")
