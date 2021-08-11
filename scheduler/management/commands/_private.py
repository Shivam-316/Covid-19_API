import pandas as pd
import requests as req
import io
from datetime import datetime, date, timedelta
from api.models import StatewiseData
from django.urls import reverse
from covid_api.settings import DEFAULT_DOMAIN

def india_covid_cases():
    data_req = req.get('https://api.covid19india.org/csv/latest/states.csv')
    data = pd.read_csv(io.StringIO(data_req.text))
    df_data = pd.DataFrame.from_dict(data)
    current_date = date.today().isoformat()
    day_before = (date.today()-timedelta(days=30)).isoformat()
    date_index = df_data[df_data['Date']==day_before].index.values
    df_data = df_data[date_index[0]:]
    date_list = df_data['Date'].tolist()
    df_date = [datetime.strptime(x,'%Y-%m-%d') for x in date_list]
    df_data = df_data.drop(columns=['Date', 'Other', 'Tested'])
    df_data.insert(0, 'Date', df_date, True)
    df_data = df_data.loc[df_data["State"] == 'India']
    df_data.shape
    df_data.reset_index(drop=True, inplace=True)
    return df_data

def india_vaccination():
    data_req = req.get("http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv")
    data = pd.read_csv(io.StringIO(data_req.text))
    df_data = pd.DataFrame.from_dict(data)
    df_data['Updated On'] = pd.to_datetime(df_data['Updated On'],format='%d/%m/%Y')
    req_date = (date.today()-timedelta(days=30)).isoformat()
    date_index = df_data[df_data['Updated On']==req_date].index.values
    df_data = df_data[date_index[0]:]
    date_list = df_data['Updated On'].tolist()
    df_data = df_data.drop(columns=['Updated On'])
    df_data.insert(0, 'Date', date_list, True)
    df_data = df_data.loc[df_data["State"] == 'India']
    df_data = df_data[[
        'Date', 'State','First Dose Administered', 'Second Dose Administered',
        'Male (Doses Administered)', 'Female (Doses Administered)','Transgender (Doses Administered)',
        ' Covaxin (Doses Administered)', 'CoviShield (Doses Administered)', 'Sputnik V (Doses Administered)',
        '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)', '60+ Years (Doses Administered)',
        'Total Individuals Vaccinated'
    ]]
    df_data.reset_index(drop=True, inplace=True)
    return df_data

def india_data():
    df_cases = india_covid_cases()
    df_vaccination = india_vaccination()
    df_req = pd.merge(df_cases, df_vaccination , how ='outer')
    num_of_rows = df_req.count()[0]
    df_req.insert(loc=0, column='key', value = ['IND']*num_of_rows)
    #df_req = df_req.replace(to_replace = np.nan, value="Not Available")
    return df_req

def state_code():
    data_req = req.get('https://api.covid19india.org/csv/latest/state_wise.csv')
    data = pd.read_csv(io.StringIO(data_req.text))
    df_data = pd.DataFrame.from_dict(data)
    df_data = df_data.drop(index=[0])
    df_data = df_data[['State','State_code']]
    df_data.columns = ['State','key']
    return df_data

def state_covid_cases():
    data_req = req.get('https://api.covid19india.org/csv/latest/states.csv')
    data = pd.read_csv(io.StringIO(data_req.text))
    df_data = pd.DataFrame.from_dict(data)
    current_date = date.today().isoformat()
    day_before = (date.today()-timedelta(days=30)).isoformat()
    date_index = df_data[df_data['Date']==day_before].index.values
    df_data = df_data[date_index[0]:]
    date_list = df_data['Date'].tolist()
    df_date = [datetime.strptime(x,'%Y-%m-%d') for x in date_list]
    df_data = df_data.drop(columns=['Date', 'Other', 'Tested'])
    df_data.insert(0, 'Date', df_date, True)
    df_data = df_data.loc[df_data["State"] != 'India']
    df_data.shape
    df_data = df_data.sort_values(by = ['Date','State'])
    df_data = df_data.reset_index(drop = True)
    return df_data

def state_vaccination():
    r = req.get("http://api.covid19india.org/csv/latest/cowin_vaccine_data_statewise.csv")
    df = pd.read_csv(io.StringIO(r.text))
    df = pd.DataFrame.from_dict(df)
    df = df.rename(columns={'Updated On':'Date'})
    df['Date'] = pd.to_datetime(df['Date'],format='%d/%m/%Y')
    sorted = df.sort_values(by = ['Date','State'])
    sorted = sorted.reset_index(drop = True)
    indx = sorted.index[sorted['State'] == 'India'].tolist()
    sorted = sorted.drop(index = indx,axis = 0)
    sorted = sorted.reset_index(drop = True)
    before = (date.today()-timedelta(days = 30)).isoformat()
    idx = sorted.index[sorted['Date']==before].tolist()
    sorted = sorted.iloc[idx[0]:]
    sorted = sorted.reset_index(drop = True)
    sorted = sorted[[
        'Date', 'State','First Dose Administered', 'Second Dose Administered',
        'Male (Doses Administered)', 'Female (Doses Administered)','Transgender (Doses Administered)',
        ' Covaxin (Doses Administered)', 'CoviShield (Doses Administered)', 'Sputnik V (Doses Administered)',
        '18-44 Years (Doses Administered)','45-60 Years (Doses Administered)', '60+ Years (Doses Administered)',
        'Total Individuals Vaccinated'
    ]]
    return sorted

def state_data():
    df_cases = state_covid_cases()
    df_vaccination = state_vaccination()
    df_req = df_cases.merge(df_vaccination, how='outer')
    state_key = state_code()
    df_req = state_key.merge(df_req, on='State')
    return df_req

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
        full_df = pd.concat([india_data(),state_data()],axis=0)
        full_df['Date'] = full_df['Date'].dt.strftime('%Y-%m-%d')
        full_df.fillna(value=0,inplace=True)
        full_df.columns = ['key', 'date', 'state', 'confirmed', 'recovered', 'deceased', 'first_dose', 'second_dose', 'male_vcc', 'female_vcc','transgender_vcc','total_covaxin','total_covishield','total_sputnik','age18_45','age45_60','age60','total_vcc']

    except Exception as e:
        print(e, "Data Error")
    else:
        StatewiseData.objects.all().delete()
        full_df.iloc[:5].apply(post_to_database,axis=1)
