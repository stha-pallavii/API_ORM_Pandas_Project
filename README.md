# API_ORM_Pandas_Project

This project includes topic related to API, ORM and Pandas.  

## Team Members 
1. [Akshey Sigdel](https://github.com/aksigdel)
2. [Amrit Prasad Phuyal](https://github.com/amrit-fuse)
3. [Pallavi Shrestha](https://github.com/stha-pallavii)

Above mentioned team members contributed and completed the project during thier traineeship at Fusemachines Nepal.

---
## Create and activate a virtual environment:
---

`>> python -m venv env_name`

`>> env_name\Scripts\activate`

Use `pip install -r requirements.txt` to install the required packages.

---
## `pd_fuctions` package and their methods
---


    doctor_df = pd.read_csv('doctors.csv')
    room_df = pd.read_csv('rooms.csv')
    patient_df = pd.read_csv('patients.csv')
    bill_df = pd.read_csv('bills.csv', parse_dates=['admit_date', 'discharge_date'])

| **Method name**                   | **Argument(s) needed**                                                                                                                              | **Description**                                                                                                                   |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| **`group_by_gender`**             | patient_df with atleast `patient_gender` and `patient_id` columns                                                                                   | Returns a df with `patient_gender` and `count` columns                                                                            |
| **`after_year`**                  | patient_df with atleast `patient_name` and `patient_dob` columns     and `year` supplied                                                            | Returns a df with `patient_name` and `patient_dob` columns born after 1985                                                        |
| **`most_unique_patients`**        | patient_df and doctor_df as positional argument with atleast `patient_id` , `doctor_id `  and `doctor_name` columns                                 | Returns a df with `doctor_name` and `count` columns with counts of unique patients only                                           |
| **`highest_bill`**                | patient_df and bill_df as positional argument with atleast `patient_id` , `pateient_name `  and `bill_amount` columns                               | Returns a df with columns `patient_name` and `total_bill_amount` from repetative visits                                           |
| **`most_patients_city`**          | patient_df with atleast `patient_city` and `patient_id` columns                                                                                     | Returns a df with columns `patient_city` and `count` for no. of patients from that particular city                                |
| **`same_city`**                   | patient_df and doctor_df as positional argument with atleast `patient_city`, `patient_name`, `doctor_id `, `doctor_city ` and `doctor_name` columns | Returns a df with columns `patient_city`, `patient_name`, `doctor_city ` and `doctor_name` where patients and doctor city matches |
| **`highest_bill_doctor`**         | patient_df, doctor_df and bill_df as positional argumnets with atleast `patient_id`,  `doctor_id `, and `bill_amount` columns                       | Returns a df with columns `doctor_name` and `total_bill_collected` from multiple patients                                         |
| **`most_popular_specialization`** | patient_df and doctor_df as positional argument with atleast `patient_id`, `doctor_id `and `doctor_specialization` columns                          | Returns a df with columns `doctor_specialization` and `count` no of patients visiting doctor with particular specialization       |
| **`longest_stay`**                | patient_df and bill_df as positional argument with atleast `patient_id`, `room_id `,`admit_date`,`discharge_date` and `patient_name` columns        | Returns a df with columns `room_id` as  room of thier longest stay , `patient_name` and `duration_of_stay`                        |
| **`capitalize_name`**             | patent_df with atleast `patient_name` column                                                                                                        | Returns a df with column `patient_name_capitalized`                                                                               |


