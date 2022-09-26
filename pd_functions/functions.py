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


# 11. City  from which most patient are visiting
def most_patients_city(patient_df):
    count_df = patient_df.groupby('patient_city').count(
    ).sort_values(by='patient_id', ascending=False)
    count_df = count_df[['patient_id']]
    return count_df.rename(columns={'patient_id': 'count'}).reset_index()


# 12  Patient and doc name belonging to same city
def same_city(patient_df, doctor_df):
    merge_df = patient_df.merge(doctor_df, on='doctor_id')
    same_city_df = merge_df.query("patient_city==doctor_city")
    return same_city_df[['patient_name', 'doctor_name', 'patient_city', 'doctor_city']]


# 13 Calculate the bill amount each doc has collected for the hospital and name the highest.
def highest_bill_doctor(patient_df, doctor_df, bill_df):
    merge_df = patient_df.merge(doctor_df, on='doctor_id')
    merge_df = merge_df.merge(bill_df, on='patient_id')
    highest_bill_df = merge_df.groupby('doctor_name')[
        'bill_amount'].sum().sort_values(ascending=False)
    return highest_bill_df.to_frame().reset_index().rename(columns={'bill_amount': 'total_bill_collected'})


# 14. specialization this hospital is famous for ( popularity is measured by no. of patient visiting those doctors with specialization)
def most_popular_specialization(patient_df, doctor_df):
    merge_df = patient_df.merge(doctor_df, on='doctor_id')
    count_df = merge_df.groupby('doctor_specialization').count(
    ).sort_values(by='patient_id', ascending=False)
    count_df = count_df[['patient_id']]
    return count_df.rename(columns={'patient_id': 'count'}).reset_index()


# 15. Display Room no  and patient  who stayed in hospital for longer duration.
def longest_stay(patient_df, bill_df):
    patient_bill_df = patient_df.merge(bill_df, on='patient_id')
    patient_bill_df['duration_of_stay'] = patient_bill_df['discharge_date'] - \
        patient_bill_df['admit_date']
    # patient_bill_df['duration_of_stay']=patient_bill_df['duration_of_stay'].dt.days #convert to int
    patient_bill_df = patient_bill_df.sort_values(
        by='duration_of_stay', ascending=False)
    return patient_bill_df[['room_id', 'patient_name', 'duration_of_stay']]


# 16. Capitalize all  Doc and patient name and update to database
def capitalize_name(patient_df):
    patient_df = patient_df['patient_name'].str.title()
    return patient_df.to_frame().rename(columns={'patient_name': 'patient_name_capitalized'})
