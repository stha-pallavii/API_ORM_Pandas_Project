import pandas as pd
from pd_functions import functions as f
from pandas.io.json import to_json
from flask import Flask, jsonify, request
from exceptions import ValueNotFound, ValueDuplicate
#from sqlalchemy import create_engine, MetaData
#from sqlalchemy import Table, insert
#from sqlalchemy import select, func
#from sqlalchemy.orm import sessionmaker

app=Flask(__name__)

@app.route('/que7',methods=['GET'])
def male_female_patients():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=f.group_by_gender(patient_df)
    ##pandasquery=pandas_query.to_json(orient='index(???)')
    print(pandas_query)
    columns=[]
    records=[]
    for i in range(pandas_query.shape[1]):
        columns.append[pandas_query.columns[i]]
    print(columns)
    for j in range(pandas_query.shape[0]):
        value=pandas_query.iloc[j]
        records.append(value)
    print(records)
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': records
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
    
        
@app.route('/que8',methods=['GET'])
def patient_after_1985():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=pd.to_json(f.after_1985(patient_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
    
@app.route('/que9',methods=['GET'])
def unique_patients():
    patient_df = pd.read_csv('patient.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=pd.to_json(f.most_unique_patients(patient_df,doctor_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
    
@app.route('/que10',methods=['GET'])
def highestbill():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    pandas_query=pd.to_json(f.highest_bill(patient_df,bill_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }

@app.route('/que11',methods=['GET'])
def patients_city():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=pd.to_json(f.most_patients_city(patient_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
        
@app.route('/que12',methods=['GET'])
def city_same():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=pd.to_json(f.same_city(patient_df,doctor_df,bill_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }

        
@app.route('/que13',methods=['GET'])
def highest_billdoc():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=pd.to_json(f.highest_bill_doctor(patient_df,doctor_df,bill_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
    
        
@app.route('/que14',methods=['GET'])
def specialization():
    patient_df = pd.read_csv('patient.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=pd.to_json(f.most_popular_specialization(patient_df,doctor_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }
 
        
@app.route('/que15',methods=['GET'])
def longest_stay():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    pandas_query=pd.to_json(f.longest_stay(patient_df,bill_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        } 
   
        
@app.route('/que16',methods=['GET'])
def capitalize():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=pd.to_json(f.capitalize_name(patient_df))
    try:
        return jsonify
        {
            'status':200,
            'message': 'successful retrieval',
            'data': pandas_query
        }
    except:
        return jsonify
        {
            'status': 400,
            'message': 'Something is not right! Check',
            'data': {}
        }    
        
if __name__ == '__main__':
    app.run(debug=True)