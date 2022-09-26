from sqlalchemy import create_engine, MetaData, insert, inspect
from sqlalchemy import Table, Column, Integer, String, Float, Boolean, Date
from sqlalchemy import ForeignKey, UniqueConstraint
import MySQLdb

def create_schema(engine):
    # create metadata object and connect it to the engine
    metadata = MetaData(bind=engine)
    MetaData.reflect(metadata)

    doctor = Table('doctor', metadata,
                    Column('doctor_id', Integer, primary_key=True, autoincrement=True),
                    Column('doctor_name', String(50), nullable=False),
                    Column('doctor_specialization', String(30), nullable=False),
                    Column('doctor_city', String(20), nullable=False),
                    Column('doctor_phone', String(15), nullable=False),
                    UniqueConstraint('doctor_phone', name='UniqueKey_doctor')
                    )

    room = Table('room', metadata,
                     Column('room_id', Integer, primary_key=True, autoincrement=True),
                     Column('room_price_per_day', Integer, nullable=False),
                     )

    patient = Table('patient', metadata,
                       Column('patient_id', Integer, primary_key=True, autoincrement=True),
                       Column('patient_name', String(50), nullable=False),
                       Column('patient_gender', String(1), nullable=False),
                       Column('patient_dob', Integer, nullable=False),          #only year is included in dob
                       Column('patient_city', String(20), nullable = False),
                       Column('patient_phone', String(15), nullable=False),
                       Column('room_id', Integer, ForeignKey('room.room_id', onupdate = 'CASCADE', ondelete = 'CASCADE'), nullable=False),
                       Column('doctor_id', Integer, ForeignKey('doctor.doctor_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
                       UniqueConstraint('patient_phone', name='UniqueKey_patient')
                    )

    bill = Table('bill', metadata,
                         Column('bill_id', Integer, primary_key=True, autoincrement=True),
                         Column('patient_id', Integer, ForeignKey('patient.patient_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False),
                         Column('admit_date', Date, nullable=False),
                         Column('discharge_date', Date, nullable=False),
                         Column('bill_amount', Float, nullable=False)
                         )

#create all of the above tables in the metadata
    metadata.create_all(engine)


def insert_data(engine):
    # make connection to the engine using connect() method
    connection = engine.connect()

    # create a MetaData object: metadata
    metadata = MetaData(bind=engine)

    #reflect the MetaData
    MetaData.reflect(metadata)

    #Reflect tables from the engine using SQLalchemy Table object
    doctor = Table('doctor', metadata, autoload=True, autoload_with=engine)
    room = Table('room', metadata, autoload=True, autoload_with=engine)
    patient = Table('patient', metadata,autoload=True, autoload_with=engine)
    bill = Table('bill', metadata, autoload=True, autoload_with=engine)


    # Building list of dictionaries for each table representing column:value pairs for each record to be inserted
    # these lists will be passed to the connection.execute() method alongside insert() statement
    doctor_list = [
        {'doctor_id': 1, 'doctor_name': 'Asmita Gautam', 'doctor_specialization': 'general medicine',
         'doctor_city': 'Kathmandu', 'doctor_phone': '9845055667'},
        {'doctor_id': 2, 'doctor_name': 'Rimi Pradhan', 'doctor_specialization': 'cardiology',
         'doctor_city': 'Lalitpur', 'doctor_phone': '9861223456'},
        {'doctor_id': 3, 'doctor_name': 'Basanta Panta', 'doctor_specialization': 'neurosurgery',
         'doctor_city': 'Lalitpur', 'doctor_phone': '9851011220'},
        {'doctor_id': 4, 'doctor_name': 'Milan Poudel', 'doctor_specialization': 'endocrinology',
         'doctor_city': 'Lalitpur', 'doctor_phone': '9805800111'},
        {'doctor_id': 5, 'doctor_name': 'Ashok Baskota', 'doctor_specialization': 'orthopedics',
         'doctor_city': 'Kathmandu', 'doctor_phone': '9801880655'}
    ]

    room_list = [
        {'room_id': 101, 'room_price_per_day': 1000},
        {'room_id': 102, 'room_price_per_day': 1500},
        {'room_id': 103, 'room_price_per_day': 3000},
        {'room_id': 104, 'room_price_per_day': 4000},
        {'room_id': 105, 'room_price_per_day': 2000},
        {'room_id': 201, 'room_price_per_day': 1500},
        {'room_id': 202, 'room_price_per_day': 1000}
    ]

    patient_list = [
        {'patient_id': 1001, 'patient_name': 'Baburam Shrestha', 'patient_gender': 'M', 'patient_dob': 1990,
         'patient_city': 'Lalitpur', 'patient_phone': '9845123456', 'room_id': 101, 'doctor_id':1},
        {'patient_id': 1002, 'patient_name': 'Akshey Sigdel', 'patient_gender': 'M', 'patient_dob': 1995,
         'patient_city': 'Kathmandu', 'patient_phone': '9855098765', 'room_id': 102, 'doctor_id': 2},
        {'patient_id': 1003, 'patient_name': 'Shijal Pouel', 'patient_gender': 'F', 'patient_dob': 1987,
         'patient_city': 'Kathmandu', 'patient_phone': '9812098745', 'room_id': 103, 'doctor_id': 2},
        {'patient_id': 1004, 'patient_name': 'Memosha Joshi', 'patient_gender': 'F', 'patient_dob': 1980,
         'patient_city': 'Kathmandu', 'patient_phone': '9861324244', 'room_id': 104, 'doctor_id': 1},
        {'patient_id': 1005, 'patient_name': 'Pujan Dahal', 'patient_gender': 'M', 'patient_dob': 1976,
         'patient_city': 'Kathmandu', 'patient_phone': '9846088987', 'room_id': 105, 'doctor_id': 3},
    ]

    bill_list = [
        {'bill_id':10001, 'patient_id':1001, 'admit_date':'2022-05-10', 'discharge_date':'2022-05-15',
         'bill_amount': 5000},
        {'bill_id': 10002, 'patient_id': 1002, 'admit_date': '2022-05-27', 'discharge_date': '2022-06-05',
         'bill_amount': 12000},
        {'bill_id': 10003, 'patient_id': 1003, 'admit_date': '2022-06-01', 'discharge_date': '2022-06-06',
         'bill_amount': 15000},
        {'bill_id': 10004, 'patient_id': 1004, 'admit_date': '2022-06-05', 'discharge_date': '2022-06-15',
         'bill_amount': 40000},
        {'bill_id': 10005, 'patient_id': 1005, 'admit_date': '2022-06-10', 'discharge_date': '2022-06-21',
         'bill_amount': 22000}
    ]

#creating dictionary for all tables
    dict_tables = {
        doctor: doctor_list,
        room: room_list,
        patient: patient_list,
        bill: bill_list
    }

# execute all insert operations in a loop
    for (table, table_list) in dict_tables.items():
        connection.execute(insert(table), table_list)

#create loop
if __name__ == '__main__':
    # engine for connecting to database and performing operations
    # engine = create_engine('[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]')
    engine = create_engine('mysql://root:pallu.SQL.123@localhost:3306/hospital')

    # inspector to inspect database elements
    inspector = inspect(engine)

    # create database schema
    create_schema(engine)

    # insert data into the database
    insert_data(engine)