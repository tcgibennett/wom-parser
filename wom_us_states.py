import requests
from bs4 import BeautifulSoup
from datetime import datetime
from wom_utils import cleanDataField
import json

def getUSByState():
    url='https://www.worldometers.info/coronavirus/country/us/'
    #open with GET method 
    resp=requests.get(url) 

    if resp.status_code==200:
        soup=BeautifulSoup(resp.text,'html.parser') 
        l=soup.find(id='usa_table_countries_today')
        tbodies = l.find_all('tbody')
        states={}

        for tbody in tbodies:
            rows = tbody.find_all('tr')
            for row in rows:
                data = row.find_all('td')
                if 'Total' not in data[0].text:
                    states[data[0].text.strip()] = {
                        'Total Cases': cleanDataField(data[1]),
                        'New Cases': cleanDataField(data[2]),
                        'Total Deaths': cleanDataField(data[3]),
                        'New Deaths': cleanDataField(data[4]),
                        'Active Cases': cleanDataField(data[5]),
                        'Date': datetime.now().date().strftime('%Y-%m-%d')
                    }

        
        return states

def getCountyByState(state):
    url='https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/'
    headers={'User-Agent':'Chrome/41.0.2228.0'}
    resp=requests.get(url=url,headers=headers) 
    if resp.status_code==200:
        soup=BeautifulSoup(resp.text,'html.parser') 
        l=soup.findAll('script')
        for i in l:
            if 'window' in i.text:
                series = i.text.split('window.')
                for s in series:
                    windows = s.split(' = ')
                    if 'STATEWIDE_TIMESERIES' in windows[0]:
                        print(windows[1])
                        array = json.loads(windows[1].strip().replace(';',''))
                        print(len(array))
