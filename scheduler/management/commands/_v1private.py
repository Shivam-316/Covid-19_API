import pandas as pd
import numpy as np
import json
import requests as req
import io
from datetime import datetime, date, timedelta
from api.models import StatewiseData
from django.urls import reverse
from covid_api.settings import DEFAULT_DOMAIN
 
 
date_today = date.today().isoformat()
date_31_days_before = (date.today()-timedelta(days=31)).isoformat()
 
def get_cases_data():
  cases_data_req = req.get('https://api.covid19india.org/csv/latest/states.csv')
  cases_data = pd.read_csv(io.StringIO(cases_data_req.text))
  cases_data.Date = pd.to_datetime(cases_data.Date)
  cases_data = cases_data[(cases_data['Date'] >= date_31_days_before) &(cases_data['Date'] < date_today)]
  cases_data.reset_index(drop=True, inplace=True)
  return cases_data
 
def get_vaccination_data():
  vacc_data_req = req.get("http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv")
  vacc_data = pd.read_csv(io.StringIO(vacc_data_req.text))
  vacc_data.rename(columns={'Updated On' : 'Date'}, inplace=True)
  vacc_data.Date = pd.to_datetime(vacc_data.Date, format='%d/%m/%Y')
  vacc_data = vacc_data[(vacc_data['Date'] >= date_31_days_before) & (vacc_data['Date'] < date_today)]
  vacc_data.reset_index(drop=True, inplace=True)
  return vacc_data
 
def get_state_codes():
  codes_data_req = req.get('https://api.covid19india.org/csv/latest/state_wise.csv')
  codes_data = pd.read_csv(io.StringIO(codes_data_req.text))
  codes_data = codes_data.drop(index=[0])
  codes_data = codes_data[['State','State_code']]
  codes_data.columns = ['State','key']
  india_code = pd.DataFrame([['India','IND']], columns=codes_data.columns)
  codes_data = codes_data.append(india_code, ignore_index=True)
  return codes_data
 
def merge_and_relative_bind(cases_data, vacc_data, codes_data):
  final_data = cases_data.merge(vacc_data, how='outer')
  final_data = codes_data.merge(final_data, on='State')
  final_data = final_data.fillna(0)
  corrected_final_data = pd.DataFrame(columns=final_data.columns)
  for key in final_data.key.unique():
    state_data = final_data[final_data.key == key]
    state_data_ahead = state_data.copy()
    state_data_ahead = state_data_ahead.drop([state_data_ahead.index[-1]], axis=0)
    state_data_ahead.drop(['key','State','Date'], axis=1, inplace=True)
    mask_df = pd.DataFrame(np.zeros_like(state_data_ahead.iloc[0], shape=(1,state_data_ahead.shape[1])), columns=state_data_ahead.columns)
    state_data_mask = pd.concat([mask_df, state_data_ahead], ignore_index=True)
    state_data.reset_index(drop=True, inplace=True)
    correct_state_data = state_data.subtract(state_data_mask)
    correct_state_data = correct_state_data.drop([0])
    correct_state_data.Date, correct_state_data.key, correct_state_data.State = state_data.Date.dt.strftime('%Y-%m-%d'), state_data.key, state_data.State
    corrected_final_data = corrected_final_data.append(correct_state_data, ignore_index=True)
  corrected_final_data = corrected_final_data[
      ['key', 'Date', 'State', 'Confirmed', 'Recovered', 'Deceased',
      'First Dose Administered', 'Second Dose Administered',
      'Male (Doses Administered)', 'Female (Doses Administered)',
      'Transgender (Doses Administered)', 'Covaxin (Doses Administered)',
      'CoviShield (Doses Administered)','Sputnik V (Doses Administered)',
      '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)',
      '60+ Years (Doses Administered)','Total Doses Administered',
    ]
  ]
  corrected_final_data.columns = ['key', 'date', 'state', 'confirmed', 'recovered', 'deceased', 'first_dose', 'second_dose', 'male_vcc', 'female_vcc','transgender_vcc','total_covaxin','total_covishield','total_sputnik','age18_45','age45_60','age60','total_vcc']
  
  return corrected_final_data

def post_to_database(row):
    try:
        res = req.post(
            url= DEFAULT_DOMAIN + reverse('addRecords'),
            data = row.to_json(),
            headers = {'content-type': 'application/json'},
            auth = ('peter','peter316')
        )
        print(row)
    except Exception as e:
        print(e, "POST Error")

def init_data():
    try:
        cases = get_cases_data()
        vaccination = get_vaccination_data()
        state_codes = get_state_codes()

        data = merge_and_relative_bind(cases, vaccination, state_codes)
    except Exception as e:
        print(e, "Data Error")
    else:
        StatewiseData.objects.all().delete()
        data.iloc[:50].apply(post_to_database,axis=1)

