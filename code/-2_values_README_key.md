-2_values.ipynb creates a CSV file, adding new columns to alldata.csv (raw citizen data). The new columns indicate whether a phenophase should be reported as -2 (e.g. The open fruit phenophase **does not** appear in mangos, but citizens report values other than -2 in the open fruit column) or is mistakenly reported as -2 (e.g. The mature leaves phenophase **does** appear in mangos, but citizens report values of -2 in the mature leaves column) for each phenophase. This process is done for all ~177 species within the citizen data. Present and absent phenpohases are determined according to SW tree phenology handbook.

The possible values in the new columns are 0, 1, & 2.

| Label  | Meaning |
| :----: | :----- |
| 0      | Valid |
| 1      | Mistakenly reported as -2 (false positive) |
| 2      | Mistakenly reported as not -2 (false negative) |