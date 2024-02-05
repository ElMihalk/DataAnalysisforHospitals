import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Stage 1/5: Upload the data
pd.set_option('display.max_columns', 8)

general = pd.read_csv(r'test\general.csv')
prenatal = pd.read_csv(r'test\prenatal.csv')
sports = pd.read_csv(r'test\sports.csv')

# print(general.head(20))
# print(prenatal.head(20))
# print(sports.head(20))

#Stage 2/5: Merge them!

#Unify column names
prenatal.columns = general.columns
sports.columns = general.columns

#Concatenate the DFs
merged_df = pd.concat([general, prenatal, sports], axis=0, ignore_index=True)

#Delete Unnamed: 0 column
del merged_df['Unnamed: 0']

#Examine sample from concatenated DF
# print(merged_df.sample(n=20, random_state=30))

#Stage 3/5: Improve your dataset

#Delete all the empty rows
merged_df.dropna(axis=0, how='all', inplace=True)

#Correct all the gender column values to f and m respectively
merged_df.replace(to_replace=['female', 'woman'], value='f', inplace=True)
merged_df.replace(to_replace=['male', 'man'], value='m', inplace=True)

#Replace the NaN values in the gender column of the prenatal hospital with f
prenatal_df = merged_df.loc[merged_df['hospital'] == 'prenatal'].fillna(value={'gender': 'f'})
merged_df.update(prenatal_df)

#Replace the NaN values in the bmi, diagnosis, blood_test, ecg, ultrasound, mri, xray, children, months columns with zeros
to_replace = {
    'bmi': 0,
    'diagnosis': '0',
    'blood_test': '0',
    'ecg': '0',
    'ultrasound': '0',
    'mri': '0',
    'xray': '0',
    'children': 0,
    'months': 0
}
merged_df.fillna(value=to_replace, inplace=True)
# Print shape of the resulting DataFrame like in example
# print(f'Data shape: {merged_df.shape}')

#Print random 20 rows of the resulting DataFrame. For the reproducible output set random_state=30
# print(merged_df.sample(n=20, random_state=30))

#Stage 4/5: The statistics

# Which hospital has the highest number of patients?
hospital_count_dict = merged_df['hospital'].value_counts().to_dict()
hospital_max_count = max(zip(hospital_count_dict.values(), hospital_count_dict.keys()))[1]


#What share of the patients in the general hospital suffers from stomach-related issues? Round the result to the third decimal place.
stomach_issues = merged_df['diagnosis'].loc[(merged_df['diagnosis'] == 'stomach') & (merged_df['hospital'] == 'general')].count()
total_patients = merged_df['diagnosis'].loc[merged_df['hospital'] == 'general'].count()
stomach_issue_fraction = round(stomach_issues/total_patients, 3)



#What share of the patients in the sports hospital suffers from dislocation-related issues? Round the result to the third decimal place.
sports_patients = merged_df['diagnosis'].loc[merged_df['hospital'] == 'sports'].count()
dislocation_issues = merged_df['diagnosis'].loc[(merged_df['hospital'] == 'sports') & (merged_df['diagnosis'] == 'dislocation')].count()
dislocation_issue_fraction = round(dislocation_issues/sports_patients, 3)

# What is the difference in the median ages of the patients in the general and sports hospitals?
general_median_age = merged_df['age'].loc[merged_df['hospital'] == 'general'].median()
sports_median_age = merged_df['age'].loc[merged_df['hospital'] == 'sports'].median()
median_age_diff = abs(sports_median_age-general_median_age)

#After data processing at the previous stages, the blood_test column has three values: t = a blood test was taken,
# f = a blood test wasn't taken, and 0 = there is no information.
# In which hospital the blood test was taken the most often (there is the biggest number of t in the blood_test column
# among all the hospitals)? How many blood tests were taken?
hospital_blood_test_dict = merged_df['hospital'].loc[merged_df['blood_test'] == 't'].value_counts().to_dict()
hospital_max_blood_test = max(zip(hospital_blood_test_dict.values(), hospital_blood_test_dict.keys()))[1]
count_max_blood_test = max(zip(hospital_blood_test_dict.values(), hospital_blood_test_dict.keys()))[0]

# print(f'The answer to the 1st question is {hospital_max_count}')
# print(f'The answer to the 2nd question is {stomach_issue_fraction}')
# print(f'The answer to the 3rd question is {dislocation_issue_fraction}')
# print(f'The answer to the 4th question is {median_age_diff}')
# print(f'The answer to the 5th question is {hospital_max_blood_test}, {count_max_blood_test} blood tests')

# Stage 5/5: Visualize it!

#What is the most common age of a patient among all hospitals?
# Plot a histogram and choose one of the following age ranges: 0-15, 15-35, 35-55, 55-70, or 70-80.
plt.hist(merged_df['age'], bins=[0, 15, 35, 55, 70, 80])
plt.show()
#15-35

# What is the most common diagnosis among patients in all hospitals? Create a pie chart.
# print(merged_df['diagnosis'].value_counts().keys())
plt.pie(merged_df['diagnosis'].value_counts(), labels=merged_df['diagnosis'].value_counts().keys())
most_common_diagnosis = merged_df['diagnosis'].value_counts().keys()[0]
plt.show()

# Build a violin plot of height distribution by hospitals.
# Try to answer the questions. What is the main reason for the gap in values?
# Why there are two peaks, which correspond to the relatively small and big values?
general_height = merged_df['height'].loc[merged_df['hospital'] == 'general']
prenatal_height = merged_df['height'].loc[merged_df['hospital'] == 'prenatal']
sports_height = merged_df['height'].loc[merged_df['hospital'] == 'sports']

fig, axes = plt.subplots()
plt.violinplot([general_height, prenatal_height, sports_height])
axes.set_xticks((1, 2, 3))
axes.set_xticklabels(('General', 'Prenatal', 'Sports'))
plt.show()

print('The answer to the 1st question: 15-35')
print(f'The answer to the 2nd question: {most_common_diagnosis}')
print('The answer to the 3rd question: It\'s because one of the hospitals uses imperial units.')