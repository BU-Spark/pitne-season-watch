# PIT-NE SeasonWatch Project Overview

_Further details on project background, process, and results in SeasonWatch_project_report_

SeasonWatch, a citizen science organization based in India, provided our PIT-NE team with a citizen database containing daily tree phenology data collected from citizen scientists in India and a reference database containing weekly tree phenology data collected from credible sources (e.g. textbooks).

## Applications

Our team processed and analyzed these databases to provide valuable information to support the SeasonWatch in their climate research efforts:

### Data Processing

- Cleaned and reformatted citizen and reference databases (Made database formatting consistent, handled data with incorrectly reported features, etc.)
- Developed a data validation system for citizen database (Used isolation forests for anomaly detection)

### Data Analysis

- Created visualizations of the citizen and reference data over time (Bar and line charts highlighting discrepancies between the citizen and reference observations over time)
- Developed a process for selecting representative citizen observations over a year to use as up-to-date baselines for any species.
- Designed a scoring function to identify flowering and fruiting stage transitions throughout a given year.

## Repository Structure

### code (Contains Python notebooks used in the final product)
  - -2_values (Flags citizen observations with incorrect reports regarding the presence or absence of a phenophase in the reported species)
  - data_cleaning (Cleans citizen and reference databases, and validates citizen database)
  - mean_transition_times_generation (Creates visualizations and a dataset of probability distributions of phenophase transition times based on a score function)
  - selecting_reference_data (Creates visualizations and a dataset of representative citizen observations selected as baselines)
  - validation_labels (Flags citizen observations dropped during the data cleaning process and gives reasons for dropping them)
  - visualizations (Creates visualizations of the citizen and reference data)
  - year_to_year_transition_times_data_generation (Creates the year_to_year_transition_time dataset)
### data (Contains CSV files of original data and data produced by the Python notebooks in code)
  - citizen_states_cleaned (Cleaned and reformatted citizen database sorted by states)
  - india_map (Geographic data used for finding the Inidan state given a set of coordinates)
  - original_citizen_data (Citizen database given by SeasonWatch)
  - original_reference_data (Reference database given by SeasonWatch)
  - reference_states_cleaned (Cleaned and reformatted reference database sorted by states)
  - alldata_labeling_-2_all_species (Citizen database given by SeasonWatch with incorrect reports regarding the presence or absence of a phenophase in the reported species flagged)
  - average_transition_times (Dataset of probability distributions of phenophase transition times based on a score function)
  - cleaned_alldata (Cleaned and reformatted citizen database as one dataset)
  - selected_reference_data (Dataset of representative citizen observations selected as baselines)
  - species codes (Dataset mapping tree species ids to names)
  - validation_labels_alldata (Citizen database given by SeasonWatch with citizen observations dropped during the data cleaning process flagged and reasons for dropping them given)
  - year_to_year_transition_time (Dataset of max and mean transition time and probability of phenophases)
### dev_code (Contains Python notebooks used in the development process)
  - jobfiles (Files of jobs submitted to shared cloud computing service)
  - scc-config (Config for submitting jobs to shared cloud computing service)
  - kmeans_pca_testing (Experimenting with and visualizing data validation methods)
  - mean transition times from repeat observations (Experimenting with only using regular citizen observations to find phenophase transition times)
  - mean_transition_times_dev (Experimenting with different methods for finding phenophase transition times)
  - plotting (Preliminary, experimental visualizations)
  - ref_cit_na_comparison (Comparing how much citizen data has associated reference data)
### plots (Contains PNG files depicting plots produced by the Python notebooks in code)

> _Citizen observations are usually depicted as percentages. This measure indicates the percentage of citizen reports observing a phenophase in the given week._
>
> _Plots report information weekly (48 weeks per year) over a year._

  - combination_percentage_charts (Compares citizen data and reference data over time; bar charts indicate number of citizen observations that week)
  - overlaid_percentage_plots (Compares related phenophases within citizen data over time; bar charts indicate number of citizen observations that week)
  - repeat_combination_percentage_charts (Compares regular observations and all observations within citizen data over time; bar charts indicate number of citizen observations that week)
  - repeat_observations (Compares differences between regular observations and reference data over time, and between all observations and reference data over time)
  - selected_ref_vs_cit (Compares citizen data and selected baselines over time)
  - transition_bar_plots (Depicts number of observations reporting a phenophase appearing over time)
  - two_values_weighted (Compares percentage presence of a phenophase and the magnitude of the presence of a phenophase within the citizen data over time)

## Usage Guide

### Step 1: Data Cleaning

Data should be cleaned, reformatted, and validated before it is applied to anything. Thus, the data cleaning notebook or script should be run before any visualization or analysis.

> _Edit file paths within the code to any new citizen data or reference data CSV files._

### Step 2: Plotting & Analysis

Any other notebook within the code folder can be run next to update the data and plots. Notebooks have functions for plotting and producing datasets. Modify parameters (states, species, year, etc.) to the functions as needed (i.e. If selected reference data on tamarind in Kerala in 2018 is wanted, set the function parameters to match that).

> _Edit plot and CSV file paths within the code as needed._
