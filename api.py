from codecs import ignore_errors
import pandas as pd
from pd_functions import functions as f
from pandas.io.json import to_json
from flask import Flask, jsonify, request
#from sqlalchemy import create_engine, MetaData
#from sqlalchemy import Table, insert
#from sqlalchemy import select, func
#from sqlalchemy.orm import sessionmaker

app=Flask(__name__)

@app.route('/que1',methods=['POST'])
def vip_room_added():
    room_df = pd.read_csv('room.csv')
    #data=request.get_json()
    data={'room_id':109,
          'room_price_per_day': 10000}
    room_df=room_df.append(data, ignore_index=True)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(room_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message

@app.route('/que2',methods=['POST'])
def doc_adds_details():
    doctor_df = pd.read_csv('doctor.csv')
    #data=request.get_json()
    data={'doctor_id':19,
          'doctor_name':'Helena Kc',
          'doctor_specialization': 'general medicine',
          'doctor_city': 'Kathmandu',
          'doctor_phone': 9856245223}
    doctor_df=doctor_df.append(data, ignore_index=True)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(doctor_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
@app.route('/que3/<int:id>',methods=['POST'])
def doc_change_details(id):
    doctor_df = pd.read_csv('doctor.csv')
    #data=request.get_json()
    new_city= 'Biratnagar'
    doctor_df.set_index('doctor_id', inplace=True)
    doctor_df.loc[id,['doctor_city']]=new_city
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(doctor_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message

@app.route('/que4',methods=['POST'])
def patient_adds_details():
    patient_df = pd.read_csv('patient.csv')
    #data=request.get_json()
    data={'patient_id':1091,
          'patient_name':'Harry Kc',
          'patient_gender': 'M',
          'patient_dob': 1999,
          'patient_city': 'Kathmandu',
          'patient_phone': 9856565223,
          'room_id':105,
          'doctor_id':19}
    patient_df=patient_df.append(data, ignore_index=True)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(patient_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message

@app.route('/que5',methods=['POST'])
def bill_adds_details():
    bill_df = pd.read_csv('bill.csv')
    #data=request.get_json()
    data={'bill_id':10090,
          'patient_id':1091,
          'admit_date': 2022-11-5,
          'discharge_date': 2022-11-9,
          'bill_amount': 3000}
    bill_df=bill_df.append(data, ignore_index=True)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(bill_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
@app.route('/que6/<int:id>',methods=['POST'])
def bill_drop_details(id):
    bill_df = pd.read_csv('bill.csv')
    #data=request.get_json()
    bill_df=bill_df.set_index('bill_id')
    bill_df=bill_df.drop(id)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(bill_df.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
@app.route('/que7',methods=['GET'])
def male_female_patients():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=f.group_by_gender(patient_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    ##pandasquery=pandas_query.to_json(orient='index(???)')
    #print(pandas_query)
    #columns=[]
    #records=[]
    #for i in range(pandas_query.shape[1]):
    #    columns.append[pandas_query.columns[i]]
    #print(columns)
    #for j in range(pandas_query.shape[0]):
    #    value=pandas_query.iloc[j]
    #    records.append(value)
    #print(records)
    #try:
    #    return jsonify
    #     {
    #     'status':200,
    #     'message': 'successful retrieval',
    #     'data': records
    #     }
    #except:
    #  return jsonify
    #    {
    #     'status': 400,
    #     'message': 'Something is not right! Check',
    #     'data': {}
    #    }
import json
@app.route('/que8',methods=['GET'])
def patient_after_1985():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=f.after_1985(patient_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e
    
@app.route('/que9',methods=['GET'])
def unique_patients():
    patient_df = pd.read_csv('patient.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=f.most_unique_patients(patient_df,doctor_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
@app.route('/que10',methods=['GET'])
def highestbill():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    pandas_query=f.highest_bill(patient_df,bill_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
@app.route('/que11',methods=['GET'])
def patients_city():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=f.most_patients_city(patient_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
        
@app.route('/que12',methods=['GET'])
def city_same():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=f.same_city(patient_df,doctor_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
        
@app.route('/que13',methods=['GET'])
def highest_billdoc():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=f.highest_bill_doctor(patient_df,doctor_df,bill_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
    
        
@app.route('/que14',methods=['GET'])
def specialization():
    patient_df = pd.read_csv('patient.csv')
    doctor_df = pd.read_csv('doctor.csv')
    pandas_query=f.most_popular_specialization(patient_df,doctor_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
 
        
@app.route('/que15',methods=['GET'])
def longest_stay():
    patient_df = pd.read_csv('patient.csv')
    bill_df = pd.read_csv('bill.csv',parse_dates=['admit_date','discharge_date'])
    pandas_query=f.longest_stay(patient_df,bill_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message
   
        
@app.route('/que16',methods=['GET'])
def capitalize():
    patient_df = pd.read_csv('patient.csv')
    pandas_query=f.capitalize_name(patient_df)
    try:
        return jsonify({
        'status': 200,
        'message':'Success',
        'data': json.loads(pandas_query.to_json(orient='records'))
    })
    except Exception as e:
        return e.message  
        
if __name__ == '__main__':
    app.run(debug=True)
    
    
