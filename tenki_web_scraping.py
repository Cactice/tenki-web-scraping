

from bs4 import BeautifulSoup
import re
import requests
import math



ken = {} # ken means prefecture in Japanese

def init_tenki():
    weather_url = 'http://www.weather-eye.com/weatherchart/'
    r  = requests.get(weather_url)
    data = r.content
    soup = BeautifulSoup(data, 'html.parser')
    for each in soup.find_all('a'):
        ken_id = re.search('_(\d{5}).',each.get('href')).group(1)
        ken_name = each.get_text()
        ken[ken_name] = ken_id



init_tenki()



def transform_ken(ken):
    transformed_ken = re.sub('県|都|府','', ken)
    if transformed_ken == '京':
        transformed_ken = '京都'
    elif transformed_ken == '沖縄':
        transformed_ken = '沖縄島'
    elif transformed_ken == '北海道':
        transformed_ken = '旭川'
    return transformed_ken




def scrape_table(tr):
    day = 0
    day2 = 0
    month_obj = {}
    for index, each_tr in enumerate(tr):
        if index % 3 == 0:
            for b in each_tr.findAll('b'):
                month_obj[int(b.get_text())] = []
        if index % 3 == 1:
            for font in each_tr.findAll('font'):
                day += 0.5
                date = math.ceil(float(day))
                month_obj[date].append(font.get_text())
        if index % 3 == 2:
            for font in each_tr.findAll('font'):
                day2 += 0.5
                date = math.ceil(float(day2))
                month_obj[date].append(font.get_text())
    return month_obj



def scrape_tr(full_url):
    r  = requests.get(full_url)
    data = r.content
    soup = BeautifulSoup(data, 'html.parser')
    body = soup.find('body')
    table = body.findAll('table')[6]
    tr = table.findAll('tr')
    del tr[0]
    return scrape_table(tr)




def get_climate(target_ken_name,target_date,transform=True):
    if transform:
        target_ken_id = ken[transform_ken(target_ken_name)]
    else:
        target_ken_id = ken[target_ken_name]
    target_month = re.search('^\d{4}', target_date).group(0)
    target_day = int(re.search('\d{2}$', target_date).group(0))
    url_prefix = 'http://www.weather-eye.com/weatherchart/src/'
    url_suffix = '.htm'
    full_url = url_prefix + target_month + '_' + target_ken_id + url_suffix
    month_obj = scrape_tr(full_url)
    return month_obj[target_day]





