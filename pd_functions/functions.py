# 7. Find whether there are more  male/female patients .
# takes dataframe as argument  and return  a new dataframe with counts
def group_by_gender(df):
    count_df = df.groupby('patient_gender').count(
    ).sort_values(by='patient_id', ascending=False)
    count_df = count_df[['patient_id']]
    return count_df.rename(columns={'patient_id': 'count'}).reset_index()


# 8. List patient born after (1985)
def after_1985(df):
    df.query('patient_dob> 1985')
    return df[['patient_name', 'patient_dob']]


# 9. Name of doc treating most no of unique patients
# require 2 dataframes as positional arguments
def most_unique_patients(patient_df, doctor_df):
    merge_df = patient_df.merge(doctor_df, on='doctor_id')
    countdf = merge_df.groupby('doctor_name').count(
    ).sort_values(by='patient_id', ascending=False)
    countdf = countdf[['patient_id']]
    return countdf.rename(columns={'patient_id': 'count'}).reset_index()


# 10. Patient(details)  paying highest bill amount
# also accounts for multiple visits
def highest_bill(patient_df, bill_df):
    merge_df = patient_df.merge(bill_df, on='patient_id')
    # group by patient_name and sum the bill amount column and sort in descending order
    highest_bill_df = merge_df.groupby('patient_name')[
        'bill_amount'].sum().sort_values(ascending=False)
    # convert series to dataframe
    return highest_bill_df.to_frame().reset_index().rename(columns={'bill_amount': 'total_bill_amount'})
