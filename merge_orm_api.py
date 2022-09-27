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

# 4. New patient  visited add him/her


@app.route('/que4', methods=['POST'])
def patient_adds_details():
    data = request.form
    patient_id = data['patient_id']
    patient_name = data['patient_name']
    patient_gender = data['patient_gender']
    patient_dob = data['patient_dob']
    patient_city = data['patient_city']
    patient_phone = data['patient_phone']
    room_id = data['room_id']
    doctor_id = data['doctor_id']

    df = pd.DataFrame(data, index=[0])

    if not patient_id.isdigit() or not patient_phone.isdigit() or not room_id.isdigit() or not doctor_id.isdigit() or not patient_dob.isdigit():
        return jsonify({'error': 'patient_id, patient_phone, room_id, doctor_id and patient_dob must be integer'}), 400

    try:
        df.to_sql('patient', con=engine, if_exists='append', index=False)
        return jsonify({'success': 'patient added successfully', 'patient_id': patient_id, 'patient_name': patient_name, 'patient_gender': patient_gender, 'patient_dob': patient_dob, 'patient_city': patient_city, 'patient_phone': patient_phone, 'room_id': room_id, 'doctor_id': doctor_id}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 5. New bills created add it to database
@app.route('/que5', methods=['POST'])
def bill_adds_details():
    data = request.form
    bill_id = data['bill_id']
    patient_id = data['patient_id']
    admit_date = data['admit_date']
    discharge_date = data['discharge_date']

    try:
        admit_date = datetime.strptime(admit_date, '%Y-%m-%d')
        discharge_date = datetime.strptime(discharge_date, '%Y-%m-%d')
    except Exception as e:
        return jsonify({'message': e.args}), 400

    if not bill_id.isdigit() or not patient_id.isdigit():
        return jsonify({'error': 'bill_id and patient_id must be integer'}), 400

    # calculate bill amount using room price and number of days
    patient = session.query(Patient).filter_by(patient_id=patient_id).first()
    room_id = patient.room_id
    room = session.query(Room).filter_by(room_id=room_id).first()
    room_price_per_day = room.room_price_per_day
    Duration_of_stay = (discharge_date - admit_date).days
    bill_amount = room_price_per_day * Duration_of_stay

    data = {'bill_id': bill_id, 'patient_id': patient_id, 'admit_date': admit_date,
            'discharge_date': discharge_date, 'bill_amount': bill_amount}
    df = pd.DataFrame(data, index=[0])

    try:
        df.to_sql('bill', con=engine, if_exists='append', index=False)
        return jsonify({'success': 'bill added successfully', 'bill_id': bill_id, 'patient_id': patient_id, 'admit_date': admit_date, 'discharge_date': discharge_date, 'bill_amount': bill_amount, "Duration_of_stay": Duration_of_stay, "Room_price_per_day": room_price_per_day}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400

 # 6. Bill id 10090  contains inaccurate details and another bill id was already created with corrected details , so delete bill id 10090  from the database


@app.route('/que6', methods=['DELETE'])
def bill_drop_details():
    data = request.form
    bill_id = data['bill_id']

    if not bill_id.isdigit():
        return jsonify({'error': 'bill_id must be integer'}), 400

    try:
        bill = session.query(Bill).filter_by(bill_id=bill_id).first()
        if bill is None:
            return jsonify({'error': 'bill_id not found'}), 400
        session.delete(bill)
        session.commit()
        return jsonify({'success': 'bill deleted successfully', 'bill_id': bill_id}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400

##################################### use pd_functons package  ########################################


# 7. Find whether there are more male/female patients
@app.route('/que7', methods=['GET'])
def male_female_patients():
    conn = engine.connect()
    try:
        df = pd.read_sql(
            'SELECT patient_id, patient_gender FROM patient', conn)

        result = f.group_by_gender(df)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'result': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 8. List patient born after ( given year   )
@app.route('/que8', methods=['GET'])
def patient_after_year():

    data = request.form
    try:
        year = int(data['year'])
    except Exception as e:
        return jsonify({'message': e.args}), 400

    conn = engine.connect()
    try:
        df = pd.read_sql(
            'SELECT  patient_name, patient_dob FROM patient', conn)

        result = f.after_year(df, year)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'result': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 9 Name of doc treating most no of unique patient
@app.route('/que9', methods=['GET'])
def unique_patients():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, doctor_id FROM patient', conn)
        doctor_df = pd.read_sql(
            'SELECT doctor_id, doctor_name FROM doctor', conn)

        result = f.most_unique_patients(patient_df, doctor_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Doctors and their counts': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 10. Patient(name)  paying highest bill amount
@app.route('/que10', methods=['GET'])
def highestbill():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, patient_name FROM patient', conn)
        bill_df = pd.read_sql(
            'SELECT patient_id, bill_amount FROM bill', conn)

        result = f.highest_bill(patient_df, bill_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Patients and their bill amounts': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400

# 11.  City  from which most patient are visiting


@app.route('/que11', methods=['GET'])
def patients_city():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, patient_city FROM patient', conn)

        result = f.most_patients_city(patient_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Cities and their counts': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 12. Patient and doc name belonging to same city
@app.route('/que12', methods=['GET'])
def city_same():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, patient_name, patient_city,doctor_id FROM patient', conn)
        doctor_df = pd.read_sql(
            'SELECT doctor_id, doctor_name, doctor_city FROM doctor', conn)

        result = f.same_city(patient_df, doctor_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Patients and Doctors and their cities': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 13. Calculate the bill amount each doc has collected for the hospital and name the highest.
@app.route('/que13', methods=['GET'])
def highest_billdoc():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, doctor_id FROM patient', conn)
        doctor_df = pd.read_sql(
            'SELECT doctor_id, doctor_name FROM doctor', conn)
        bill_df = pd.read_sql(
            'SELECT patient_id, bill_amount FROM bill', conn)

        result = f.highest_bill_doctor(patient_df, doctor_df, bill_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Doctors and their bill amounts': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 14.Specialization this hospital is famous for ( popularity is measured by no. of patient visiting those doctors with specialization)
@app.route('/que14', methods=['GET'])
def specialization():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, doctor_id FROM patient', conn)
        doctor_df = pd.read_sql(
            'SELECT doctor_id, doctor_specialization FROM doctor', conn)

        result = f.most_popular_specialization(patient_df, doctor_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Specializations and their counts': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 15. Display Room no  and patient  who stayed in hospital for longer duration in one admission
@app.route('/que15', methods=['GET'])
def longest_stay():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, patient_name, room_id FROM patient', conn)
        admission_df = pd.read_sql(
            'SELECT patient_id, admit_date, discharge_date FROM bill', conn)

        result = f.longest_stay(patient_df, admission_df).head(5)
        result = result.to_json(orient='records')

        return jsonify({'success': 'request sucessful', 'Top 5 Patients and their durations': json.loads(result)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


# 16. Capitalize all  patient name and commit  to database
@app.route('/que16', methods=['PUT'])
def capitalize():
    conn = engine.connect()
    try:
        patient_df = pd.read_sql(
            'SELECT patient_id, patient_name FROM patient', conn)
        result = f.capitalize_name(patient_df)
        result_json = result.to_json(orient='records')
        patient = session.query(Patient).all()
        for i in range(len(patient)):
            patient[i].patient_name = result['patient_name_capitalized'][i]
        session.commit()

        return jsonify({'success': 'request sucessful', 'message': 'patient names capitalized', 'Capatilized names': json.loads(result_json)}), 200

    except Exception as e:
        return jsonify({'message': e.args}), 400


if __name__ == '__main__':

    # be careful with below functions . comment them out when not in use

    create_tables()
    # insert_data() # please comment out this function after first use

    # drop_tables() # drop all tables
    # delete_data() # delete all data from tables but keep the tables and its structure

    app.run(debug=True)
