import pandas as pd

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
data = df.loc[:,['iso_code','date','new_cases','total_cases','new_deaths','total_deaths','new_tests','total_tests',
                  'people_vaccinated','people_fully_vaccinated']]

#!pip install xlsxwriter

iso_jpn = []
iso_usa = []
iso_kor = []
iso_gbr = []

for i in range(len(data)):
    iso_jpn.append(data['iso_code'][i] == 'JPN')
    iso_usa.append(data['iso_code'][i] == 'USA')
    iso_kor.append(data['iso_code'][i] == 'KOR')
    iso_gbr.append(data['iso_code'][i] == 'GBR')

data_jpn = data.iloc[iso_jpn,:]
data_kor = data.iloc[iso_kor,:]
data_usa = data.iloc[iso_usa,:]
data_gbr = data.iloc[iso_gbr,:]

data_jpn = data_jpn.drop(['iso_code'], axis = 1)
data_kor = data_kor.drop(['iso_code'], axis = 1)
data_gbr = data_gbr.drop(['iso_code'], axis = 1)
data_usa = data_usa.drop(['iso_code'], axis = 1)


# 国のデータに追記する値（7，9列）
jpn_vaccinated_1 = data_jpn['people_vaccinated'].diff()
jpn_vaccinated_2 = data_jpn['people_fully_vaccinated'].diff()

kor_vaccinated_1 = data_kor['people_vaccinated'].diff()
kor_vaccinated_2 = data_kor['people_fully_vaccinated'].diff()

gbr_vaccinated_1 = data_gbr['people_vaccinated'].diff()
gbr_vaccinated_2 = data_gbr['people_fully_vaccinated'].diff()

usa_vaccinated_1 = data_usa['people_vaccinated'].diff()
usa_vaccinated_2 = data_usa['people_fully_vaccinated'].diff()


# データ列名指定、順序指定
data_jpn.insert(7,'daily_people_vaccinated',jpn_vaccinated_1, True)
data_jpn.insert(9,'daily_people_fully_vaccinated',jpn_vaccinated_2, True)

data_kor.insert(7,'daily_people_vaccinated',kor_vaccinated_1, True)
data_kor.insert(9,'daily_people_fully_vaccinated',kor_vaccinated_2, True)

data_gbr.insert(7,'daily_people_vaccinated',gbr_vaccinated_1, True)
data_gbr.insert(9,'daily_people_fully_vaccinated',gbr_vaccinated_2, True)

data_usa.insert(7,'daily_people_vaccinated',usa_vaccinated_1, True)
data_usa.insert(9,'daily_people_fully_vaccinated',usa_vaccinated_2, True)

import datetime

for i in range(len(data_jpn)):
    data_jpn.iloc[i,0] = datetime.datetime.strptime(data_jpn.iloc[i,0], '%Y-%m-%d').strftime('%Y%m%d')
for i in range(len(data_kor)):
    data_kor.iloc[i,0] = datetime.datetime.strptime(data_kor.iloc[i,0], '%Y-%m-%d').strftime('%Y%m%d')
for i in range(len(data_gbr)):
    data_gbr.iloc[i,0] = datetime.datetime.strptime(data_gbr.iloc[i,0], '%Y-%m-%d').strftime('%Y%m%d')
for i in range(len(data_usa)):
    data_usa.iloc[i,0] = datetime.datetime.strptime(data_usa.iloc[i,0], '%Y-%m-%d').strftime('%Y%m%d')

data_jpn.columns = ['日付', '新規感染者数', '累積感染者数', '死亡者数', '累積死亡数', '検査実施人数', '累積検査実施人数',
                    '1回接種', '累積1回接種', '2回接種', '累積2回接種']
data_kor.columns = ['日付', '新規感染者数', '累積感染者数', '死亡者数', '累積死亡数', '検査実施人数', '累積検査実施人数',
                    '1回接種', '累積1回接種', '2回接種', '累積2回接種']
data_gbr.columns = ['日付', '新規感染者数', '累積感染者数', '死亡者数', '累積死亡数', '検査実施人数', '累積検査実施人数',
                    '1回接種', '累積1回接種', '2回接種', '累積2回接種']
data_usa.columns = ['日付', '新規感染者数', '累積感染者数', '死亡者数', '累積死亡数', '検査実施人数', '累積検査実施人数',
                    '1回接種', '累積1回接種', '2回接種', '累積2回接種']


from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

print('日本のコロナデータ')
data_jpn.loc[data_jpn.index[len(data_jpn)-10:len(data_jpn)],:]


#!pip install xmltodict

# 現在日付に合わせて'主要国のCovid-19感染者とワクチン接種統計'に保存
import datetime as dt
from datetime import datetime, timedelta

def get_week(y, m, d):
    target = get_date(y, m, d)
    firstday = target.replace(day = 1)
    if firstday.weekday() == 6:
        origin = firstday
    elif firstday.weekday() < 3:
        origin = firstday - timedelta(days=firstday.weekday() + 1)
    else:
        origin = firstday + timedelta(days = 6-firstday.weekday())
    return (target - origin).days // 7 + 1

def get_date(y, m, d):
    day = f'{y:04d}-{m:02d}-{d:02d}'
    return datetime.strptime(day, '%Y-%m-%d')


import xlsxwriter
import datetime as dt
n = dt.datetime.now()
writer = pd.ExcelWriter('主要国のCovid-19感染者とワクチン接種統計_{}年{}月{}週目.xlsx'.format(n.year, n.month, get_week(n.year, n.month, n.day)), 
                        engine = 'xlsxwriter')

data_jpn.to_excel(writer, index = False, sheet_name = '日本')
data_kor.to_excel(writer, index = False, sheet_name = '韓国')
data_gbr.to_excel(writer, index = False, sheet_name = 'イギリス')
data_usa.to_excel(writer, index = False, sheet_name = 'アメリカ')
writer.save()

import pandas as pd
import openpyxl
n = dt.datetime.now()

data_jpn = pd.read_excel('主要国のCovid-19感染者とワクチン接種統計_{}年{}月{}週目.xlsx'.
                         format(n.year, n.month, get_week(n.year, n.month, n.day)), sheet_name = '日本')

data_kor = pd.read_excel('主要国のCovid-19感染者とワクチン接種統計_{}年{}月{}週目.xlsx'.
                         format(n.year, n.month, get_week(n.year, n.month, n.day)), sheet_name = '韓国')

data_gbr = pd.read_excel('主要国のCovid-19感染者とワクチン接種統計_{}年{}月{}週目.xlsx'.
                         format(n.year, n.month, get_week(n.year, n.month, n.day)), sheet_name = 'イギリス')

data_usa = pd.read_excel('主要国のCovid-19感染者とワクチン接種統計_{}年{}月{}週目.xlsx'.
                         format(n.year, n.month, get_week(n.year, n.month, n.day)), sheet_name = 'アメリカ')


import datetime

for i in range(len(data_jpn)):
    data_jpn.iloc[i,0] = str(data_jpn.iloc[i,0])
    data_jpn.iloc[i,0] = datetime.datetime.strptime(data_jpn.iloc[i,0], '%Y%m%d').strftime('%Y-%m-%d')
    
for i in range(len(data_kor)):
    data_kor.iloc[i,0] = str(data_kor.iloc[i,0])
    data_kor.iloc[i,0] = datetime.datetime.strptime(data_kor.iloc[i,0], '%Y%m%d').strftime('%Y-%m-%d')
    
for i in range(len(data_gbr)):
    data_gbr.iloc[i,0] = str(data_gbr.iloc[i,0])
    data_gbr.iloc[i,0] = datetime.datetime.strptime(data_gbr.iloc[i,0], '%Y%m%d').strftime('%Y-%m-%d')

for i in range(len(data_usa)):
    data_usa.iloc[i,0] = str(data_usa.iloc[i,0])
    data_usa.iloc[i,0] = datetime.datetime.strptime(data_usa.iloc[i,0], '%Y%m%d').strftime('%Y-%m-%d')



# 現在日付から7日前の日付データ
dt_1 = datetime.date.today()
dt_2 = dt_1 - timedelta(days=7)
date = dt_2.strftime('%Y-%m-%d')


import folium

# 地図データ
m = folium.Map(location = [35.6528, 139.8394], zoom_start = 4,
               max_bounds = True, 
               min_zoom = 3, 
               min_lat = -90, max_lat = 90, 
               min_lon = -180, max_lon = 180)

# 韓国 円　生成
folium.CircleMarker(location = [37.3358,126.5840], radius = int(data_kor[data_kor['日付']==date]['新規感染者数'])/300,
                   color = 'white', fill_color = 'white',
                   tooltip = ('<h4><b>韓国</h4></b><br>'+
                              '<b> 日付:</b> {date}<br>'+
                              '<b> 新規感染者数:</b> {num}人<br>'+ 
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_kor[data_kor['日付']==date]['新規感染者数']),
                                      cum_num = int(data_kor[data_kor['日付']==date]['累積感染者数']))).add_to(m)

# 日本 円　生成
folium.CircleMarker(location = [35.6528, 139.8394], radius = int(data_jpn[data_jpn['日付']==date]['新規感染者数'])/300,
                   color = 'orange', fill_color = 'orange',
                   tooltip = ('<h4><b>日本</h4></b><br>'+
                              '<b> 日付:</b> {date}<br>'+
                              '<b> 新規感染者数:</b> {num}人<br>'+ 
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_jpn[data_jpn['日付']==date]['新規感染者数']),
                                      cum_num = int(data_jpn[data_jpn['日付']==date]['累積感染者数']))).add_to(m)


# イギリス 円　生成
folium.CircleMarker(location = [51.5072,-0.1275], radius = int(data_gbr[data_gbr['日付']==date]['新規感染者数'])/300,
                   color = 'red', fill_color = 'red',
                   tooltip = ('<h4><b>イギリス</h4></b><br>'+
                              '<b> 日付:</b> {date}<br>'+
                              '<b> 新規感染者数:</b> {num}人<br>'+ 
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_gbr[data_gbr['日付']==date]['新規感染者数']),
                                      cum_num = int(data_gbr[data_gbr['日付']==date]['累積感染者数']))).add_to(m)

# アメリカ 円　生成
folium.CircleMarker(location = [37.7618, -104.8810], radius = int(data_usa[data_usa['日付']==date]['新規感染者数'])/300,
                   color = 'blue', fill_color = 'blue',
                   tooltip = ('<h4><b>アメリカ</h4></b><br>'+
                              '<b> 日付:</b> {date}<br>'+
                              '<b> 新規感染者数:</b> {num}人<br>'+ 
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_usa[data_usa['日付']==date]['新規感染者数']),
                                      cum_num = int(data_usa[data_usa['日付']==date]['累積感染者数']))).add_to(m)

m.save('円として世界地図に感染者数可視化_{date}.html'.format(date = date))
m


import json

map = folium.Map(location = [51.5072,-0.1275], zoom_start = 4,
               max_bounds = True, 
               min_zoom = 3, min_lat = -90, 
               max_lat = 90, min_lon = -180, max_lon = 180)

geo_data = 'World_Countries__Generalized_.geojson'
jsonData = json.load(open(geo_data), encoding='utf-8')
folium.GeoJson(jsonData, name = 'json_data').add_to(map)

map.save('国境線.html')
map


import folium
import datetime
from datetime import datetime, timedelta
import time

# 現在日付から7日前の日付データ
dt_1 = datetime.today()
dt_2 = dt_1 - timedelta(days=7)
date = dt_2.strftime('%Y-%m-%d')

map_jpn = data_jpn[data_jpn['日付'] == date]
map_kor = data_kor[data_kor['日付'] == date]
map_gbr = data_gbr[data_gbr['日付'] == date]
map_usa = data_usa[data_usa['日付'] == date]

map_data = pd.concat([map_jpn,map_kor,map_gbr,map_usa], axis=0, ignore_index = True)

# geo_dataの isoコードに合わせて国のデータ生成
iso_info = pd.DataFrame(data = ['JP','KR','GB','US'], columns = ['iso_code'])
country_info = pd.DataFrame(data = ['日本', '韓国', 'イギリス','アメリア'], columns = ['国'])
map_data = pd.concat([iso_info,country_info,map_data], axis = 1)
map_data


import folium

geo_path = 'World_Countries__Generalized_.geojson'
geo_data = json.load(open(geo_path, encoding='UTF-8'))

m = folium.Map(location = [51.5072,-0.1275], zoom_start = 4,
               max_bounds = True, 
               min_zoom = 3, min_lat = -90, 
               max_lat = 90, min_lon = -180, max_lon = 180)

folium.Choropleth(geo_data = geo_data, 
             data = map_data,
             columns = ['iso_code','新規感染者数'], key_on = 'properties.ISO',
             highlight = True,
             fill_color = 'RdYlGn', fill_opacity = 0.7, line_opacity = 0.5,
             legend_name = '新規感染者数').add_to(m)

m.save('folium 世界地図感染者数可視化_{date}.html'.format(date = date))
m

geo_path = 'World_Countries__Generalized_.geojson'
geo_str = json.load(open(geo_path, encoding='UTF-8'))

# 現在日付から７日前の日付データ
dt_1 = datetime.today()
dt_2 = dt_1 - timedelta(days=7)
date = dt_2.strftime('%Y-%m-%d')

m = folium.Map(location = [51.5072,-0.1275], zoom_start = 4,
               max_bounds = True, 
               min_zoom = 3, min_lat = -90, 
               max_lat = 90, min_lon = -180, max_lon = 180)

choropleth = folium.Choropleth(geo_data = geo_str, 
             data = map_data,
             columns = ['iso_code','新規感染者数'], key_on = 'properties.ISO',
             highlight = True,
             fill_color = 'YlOrRd', fill_opacity = 0.5, line_opacity = 0.5,
             legend_name = 'Covid-19 感染者数').add_to(m)

# 日本
folium.Marker([35.6528, 139.8394], icon = folium.Icon(color = 'red'),
              tooltip = ('<h4><b>日本</h4></b><br>'
                              '<b> 日付: </b> {date}<br>'
                              '<b> 感染者数:</b> {num}人<br>' 
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_jpn[data_jpn['日付']==date]['新規感染者数']), 
                                      cum_num = int(data_jpn[data_jpn['日付']==date]['累積感染者数']))).add_to(m)


# 韓国
folium.Marker([37.3358,126.5840], icon = folium.Icon(color = 'red'),
              tooltip = ('<h4><b>韓国</h4></b><br>'
                              '<b> 日付:</b> {date}<br>'
                              '<b>感染者数:</b> {num}人<br>'
                              '<b>累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_kor[data_kor['日付']==date]['新規感染者数']), 
                                      cum_num = int(data_kor[data_kor['日付']==date]['累積感染者数']))).add_to(m)

# イギリス
folium.Marker([51.5072,-0.1275], icon = folium.Icon(color = 'red'),
              tooltip = ('<h4><b>イギリス</h4></b><br>'
                              '<b> 日付:</b> {date}<br>'
                              '<b> 感染者数:</b> {num}人<br>'
                              '<b> 累積感染者数:</b> {cum_num}人<br>'
                             ).format(date = date,
                                      num = int(data_gbr[data_gbr['日付']==date]['新規感染者数']), 
                                      cum_num = int(data_gbr[data_gbr['日付']==date]['累積感染者数']))).add_to(m)

# アメリカ
folium.Marker([37.7618, -104.8810], icon = folium.Icon(color = 'red'),
              tooltip = ('<h4><b>アメリカ</h4></b><br>'
                         '<b>日付: </b> {date}<br>'
                         '<b> 感染者数: </b> {num}人<br>'
                         '<b> 累積感染者数: </b> {cum_num}人<br>').format(date = date,
                                      num = int(data_usa[data_usa['日付']==date]['新規感染者数']), 
                                      cum_num = int(data_usa[data_usa['日付']==date]['累積感染者数']))).add_to(m)

m.save('choropleth Marker世界地図に感染者数可視化_{date}.html'.format(date = date))
m