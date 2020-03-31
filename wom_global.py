import requests
from bs4 import BeautifulSoup
from datetime import datetime
from wom_utils import cleanDataField

def demographic():
    url='https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/'
    #open with GET method 
    resp=requests.get(url) 

    if resp.status_code==200:
        demographics={}
        soup=BeautifulSoup(resp.text,'html.parser')
        tables=soup.find_all('table')
        header=''
        for table in tables:
            rows=table.find_all('tr')
            for row in rows:
                divs=row.find_all('div')
                if len(divs) == 1:
                    header = divs[0].text.strip().lower()
                    demographics[header]={}
                else:
                    segment = divs[0].text.strip().replace(' years old','')
                    data={}
                    if len(segment) == 0:
                        segment = row.td.text.strip().replace(' years old','')
                        data[segment]={'death rate confirmed cases':divs[0].text.strip() if len(divs[0].text.strip()) > 0 else '0.0%','death rate all cases':divs[1].text.strip() if '%' in divs[1].text.strip() else '0.0%'}
                    else:
                        data[segment]={'death rate confirmed cases':divs[1].text.strip() if len(divs[1].text.strip()) > 0 else '0.0%','death rate all cases':divs[2].text.strip()}
                    
                    
                    demographics[header].update(data)

        return demographics

    else:
        print(resp.text)


def countries():
    url='https://www.worldometers.info/coronavirus/'
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 

        #print(resp.text)

        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
  
        # l is the list which contains all the text i.e news  
        l=soup.find(id='main_table_countries_today') 
        header = l.find('thead').find_all('th')
        body = l.find('tbody').find_all('tr')
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
        countries_total={}
        
        for row in body:
            data = row.find_all('td')
            countries_total[data[0].text.lower()] = {
                'Total Cases': cleanDataField(data[1]),
                'New Cases': cleanDataField(data[2]),
                'Total Deaths': cleanDataField(data[3]),
                'New Deaths': cleanDataField(data[4]),
                'Total Recovered': cleanDataField(data[5]),
                'Active Cases': cleanDataField(data[6]),
                'Critical Cases': cleanDataField(data[7]),
                'Total Cases 1M Pop': cleanDataField(data[8]),
                'Total Deaths 1M Pop': cleanDataField(data[9]),
                'First Case Reported': datetime.strptime(data[10].text.strip() + ' 2020', '%b %d %Y').date().strftime('%Y-%m-%d')
            }

        
        return countries_total
    else: 
        print("Error") 