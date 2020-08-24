#%%
import pandas as pd
#%%
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
#%%
confirmed = pd.read_csv("time_series_covid19_confirmed_global.csv")
deaths = pd.read_csv("time_series_covid19_deaths_global.csv", index_col=None)
recovered = pd.read_csv("time_series_covid19_recovered_global.csv", index_col=None)
US_confirmed = pd.read_csv("time_series_covid19_confirmed_US.csv", index_col=None)
US_deaths = pd.read_csv("time_series_covid19_deaths_US.csv", index_col=None)
confirmed.head(5)
#%%
US_deaths = US_deaths.drop(['UID','iso2','iso3','code3','FIPS','Admin2','Combined_Key'], axis=1)
US_confirmed = US_confirmed.drop(['UID','iso2','iso3','code3','FIPS','Admin2','Combined_Key'], axis=1)
#%%
US_confirmed.head(5)
#%%
def merge(A, B):
    M = pd.merge(A, B, left_on=
    ['Province/State', 'Country/Region', 'Lat', 'Long'],
                 right_on=
                 ['Province/State', 'Country/Region', 'Lat', 'Long'])
    return M
mergeDf = merge(confirmed, recovered)
mergeDf = merge(mergeDf, deaths)
# mergeDf = pd.merge(mergeDf0, deaths, left_on = ['Province/State','Country/Region','Lat','Long'], right_on = ['Province/State','Country/Region','Lat','Long'])
# mergeDf
US_confirmed = US_confirmed.rename(columns={"Province_State": 'Province/State',
                                            "Country_Region": "Country/Region",
                                            "Long_": "Long"})
US_deaths = US_deaths.rename(columns={"Province_State": 'Province/State',
                                      "Country_Region": "Country/Region",
                                      "Long_": "Long"})
#%%
mergeUS = merge(US_confirmed, US_deaths)
mergeUS.head(5)
#%%
days = len(confirmed.columns) - 4
def createUSDf(date, data):
    d = {'Province/State':[],'Country/Region':[],'Last Update':[],
         'Confirmed':[],'Deaths':[],'Recovered':[],'Latitude':[],'Longitude':[]}
    df=pd.DataFrame(data=d)
    df['Country/Region']=(data['Country/Region'].values)
    df['Province/State']=(data['Province/State'].values)
    df['Latitude']=(data['Lat'].values)
    df['Longitude']=(data['Long'].values)
    D=[]
    for i in range(0,len(data)):
        D.append(US_confirmed.columns[date])
    df['Last Update']=D
    df['Confirmed']=(data[data.columns[date]].values)
    df['Deaths']=(data[data.columns[date + days]].values)
    return df
#%%
d = {'Province/State':[],'Country/Region':[],'Last Update':[],
    'Confirmed':[],'Deaths':[],'Recovered':[],'Latitude':[],'Longitude':[]}
df_US=pd.DataFrame(data=d)
for i in range(4,len(US_confirmed.columns)):
    df_US = df_US.append(createUSDf(i, mergeUS))
df_US.head(5)
#%%
df_US_Mar = df_US[df_US['Last Update']>='3/1/20']
df_US_Mar.head(5)

#%%
days = len(confirmed.columns) - 4
def createDf(date, data):
    d = {'Province/State':[],'Country/Region':[],'Last Update':[],
         'Confirmed':[],'Deaths':[],'Recovered':[],'Latitude':[],'Longitude':[]}
    df=pd.DataFrame(data=d)
    df['Country/Region']=(data['Country/Region'].values)
    df['Province/State']=(data['Province/State'].values)
    df['Latitude']=(data['Lat'].values)
    df['Longitude']=(data['Long'].values)
    D=[]
    for i in range(0,len(data)):
        D.append(confirmed.columns[date])
    df['Last Update']=D
    df['Confirmed']=(data[data.columns[date]].values)
    df['Recovered']=(data[data.columns[date + days]].values)
    df['Deaths']=(data[data.columns[date + days + days]].values)
    return df
#%%
d = {'Province/State':[],'Country/Region':[],'Last Update':[],
    'Confirmed':[],'Deaths':[],'Recovered':[],'Latitude':[],'Longitude':[]}
df=pd.DataFrame(data=d)
for i in range(4,len(confirmed.columns)):
    df = df.append(createDf(i, mergeDf))
df.head(5)
#%%
with pd.ExcelWriter('data.xlsx') as writer:
    df_US_Mar.to_excel(writer,sheet_name='US')
    df.to_excel(writer,sheet_name='global')