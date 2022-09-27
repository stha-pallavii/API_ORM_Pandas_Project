from flask import Flask, jsonify, request
from sqlalchemy import create_engine, MetaData, insert, inspect
from sqlalchemy import Table, Column, Integer, String, Float, Boolean, Date
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import MySQLdb
import pandas as pd
import json
from datetime import datetime
from pd_functions import functions as f


# engine for connecting to database and performing operations
# engine = create_engine('[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]')
engine = create_engine(
    'mysql+mysqldb://panda007:1234@localhost:3306/hospital')

app = Flask(__name__)

Base = declarative_base()  # create a base class for our class definitions

# create a session object to connect to the DB
session = sessionmaker(bind=engine)()

############################################# MODELS #########################################################


class Doctor(Base):
    __tablename__ = 'doctor'
    doctor_id = Column(Integer, primary_key=True, autoincrement=False)
    doctor_name = Column(String(50), nullable=False)
    doctor_specialization = Column(String(30), nullable=False)
    doctor_city = Column(String(20), nullable=False)
    doctor_phone = Column(String(15), nullable=False, unique=True)

    patient = relationship("Patient", back_populates="doctor")

    def __repr__(self):
        return f"Doctor(doctor_id={self.doctor_id}, doctor_name={self.doctor_name}, doctor_specialization={self.doctor_specialization}, doctor_city={self.doctor_city}, doctor_phone={self.doctor_phone})"


class Room(Base):
    __tablename__ = 'room'
    room_id = Column(Integer, primary_key=True, autoincrement=False)
    room_price_per_day = Column(Integer, nullable=False)

    patient = relationship("Patient", back_populates="room")

    def __repr__(self):
        return f"Room(room_id={self.room_id}, room_price_per_day={self.room_price_per_day})"


class Patient(Base):
    __tablename__ = 'patient'
    patient_id = Column(Integer, primary_key=True, autoincrement=False)
    patient_name = Column(String(50), nullable=False)
    patient_gender = Column(String(1), nullable=False)
    patient_dob = Column(Integer, nullable=False)
    patient_city = Column(String(20), nullable=False)
    patient_phone = Column(String(15), nullable=False, unique=True)
    room_id = Column(Integer, ForeignKey('room.room_id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctor.doctor_id'), nullable=False)

    doctor = relationship("Doctor", back_populates="patient")
    room = relationship("Room", back_populates="patient")

    def __repr__(self):
        return f"Patient(patient_id={self.patient_id}, patient_name={self.patient_name },patient_gender={self.patient_gender}, patient_dob={self.patient_dob}, patient_city={self.patient_city}, patient_phone={self.patient_phone}, room_id={self.room_id}, doctor_id={self.doctor_id})"


class Bill(Base):
    __tablename__ = 'bill'
    bill_id = Column(Integer, primary_key=True, autoincrement=False)
    admit_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=False)
    bill_amount = Column(Integer, nullable=False)
    patient_id = Column(Integer, ForeignKey(
        'patient.patient_id'), nullable=False)

    # patient = relationship("Patient", back_populates="bill")

    def __repr__(self):
        return f"Bill(bill_id={self.bill_id}, bill_date={self.bill_date}, bill_amount={self.bill_amount}, patient_id={self.patient_id})"


# function to create all of the above tables in the metadata
def create_tables():
    Base.metadata.create_all(engine)

# function to drop all of the above tables in the metadata


def drop_tables():
    Base.metadata.drop_all(engine)


# delete all data from tables
def delete_data():
    session.query(Bill).delete()
    session.query(Patient).delete()
    session.query(Doctor).delete()
    session.query(Room).delete()
    session.commit()


# emply all rows from all tables delete in roder to avoid foreign key constraint error

# function to insert(csv) data into the tables

def insert_data():
    patient_df = pd.read_csv('patient.csv')
    doctor_df = pd.read_csv('doctor.csv')
    room_df = pd.read_csv('room.csv')
    bill_df = pd.read_csv('bill.csv')

    # add in order to avoid foreign key constraint error doctor>>room>>patient>>bill
    room_df.to_sql('room', con=engine, if_exists='append', index=False)
    doctor_df.to_sql('doctor', con=engine, if_exists='append', index=False)
    patient_df.to_sql('patient', con=engine, if_exists='append', index=False)
    bill_df.to_sql('bill', con=engine, if_exists='append', index=False)

    session.commit()


# ############################# API    ############################################
# 1. A new room was recently added to the hospital
@app.route('/que1', methods=['POST'])
def vip_room_added():
    data = request.form  # get data from request body
    room_id = data['room_id']
    room_price_per_day = data['room_price_per_day']

    df = pd.DataFrame(data, index=[0])  # index=[0] to make it one row

    # raise error if room_id  and room_price_per_day are  integer or not
    if not room_id.isdigit() or not room_price_per_day.isdigit():
        return jsonify({'error': 'room_id and room_price_per_day must be integer'}), 400

    try:
        df.to_sql('room', con=engine, if_exists='append', index=False)
        return jsonify({'success': 'room added successfully', 'room_id': room_id, 'room_price_per_day': room_price_per_day}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400

# 2. A new doctor joined adds his details


@app.route('/que2', methods=['POST'])
def doc_adds_details():
    data = request.form
    doctor_id = data['doctor_id']
    doctor_name = data['doctor_name']
    doctor_specialization = data['doctor_specialization']
    doctor_city = data['doctor_city']
    doctor_phone = data['doctor_phone']

    df = pd.DataFrame(data, index=[0])

    if not doctor_id.isdigit() or not doctor_phone.isdigit():
        return jsonify({'error': 'doctor_id and doctor_phone must be integer'}), 400

    try:
        df.to_sql('doctor', con=engine, if_exists='append', index=False)
        return jsonify({'success': 'doctor added successfully', 'doctor_id': doctor_id, 'doctor_name': doctor_name, 'doctor_specialization': doctor_specialization, 'doctor_city': doctor_city, 'doctor_phone': doctor_phone}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 3. Existing doc moved to new city , make change to database
@app.route('/que3', methods=['PUT'])
def doc_change_details():
    data = request.form
    doctor_id = data['doctor_id']
    doctor_city = data['doctor_city']

    print('data is', data)

    if not doctor_id.isdigit():
        return jsonify({'error': 'doctor_id must be integer'}), 400

    try:
        doctor = session.query(Doctor).filter_by(doctor_id=doctor_id).first()
        if doctor is None:
            return jsonify({'error': 'doctor_id not found'}), 400
        doctor.doctor_city = doctor_city
        session.commit()
        return jsonify({'success': 'doctor city changed successfully', 'doctor_id': doctor_id, 'doctor_city(NEW)': doctor_city}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


if __name__ == '__main__':

    # be careful with below functions . comment them out when not in use

    create_tables()
    # insert_data() # please comment out this function after first use

    # drop_tables() # drop all tables
    # delete_data() # delete all data from tables but keep the tables and its structure

    app.run(debug=True)
