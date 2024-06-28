`validation_labels_alldata.csv` is a copy of alldata.csv with a new column `validation_label` which labels the observations that were dropped from the citizen data in our team's data cleaning process. The reason for dropping each observation is given by the validation label's value. The meanings of these values are listed in the key below:

## Key for `validation_label` Column

| Label | Meaning |
| :----: | :----- |
| 0      | Kept   |
| 1      | Dropped because a phenophase was incorrectly reported as being -2 |
| 2      | Dropped because a phenophase had missing data (Null Values) |
| 3      | Dropped because observation was flagged as anomalous |

## Counts for `validation_label` Column

| Label | Number of Observations |
| :----: | :----- |
| 0      | 318332 |
| 1      | 46200 |
| 2      | 210436 |
| 3      | 17625 |