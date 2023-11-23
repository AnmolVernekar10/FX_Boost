#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# In[2]:


mydata = pd.read_csv("E:/Anmol_Projects/FX_Project/data/NTData3.csv")


# In[3]:


mydata['Date'] = pd.to_datetime(mydata['Date'])  


# In[4]:


mydata


# ### Interpolation
# 

# In[5]:


df = mydata.copy()

#setting data as index
df.set_index('Date', inplace=True)


# In[6]:


df.interpolate(method='linear', inplace=True)


# In[7]:


df.head(20)


# In[8]:


# fill NaN values in each column with the next non-NaN value along the column
df = df.apply(lambda x: x.bfill(), axis=0)
df.head(20)


# ### Functions

# In[9]:


def values(cur, startdate, enddate):
    
    start = pd.to_datetime(startdate)
    end = pd.to_datetime(enddate)
    mask = (mydata['Date'] > start) & (mydata['Date'] <= end)
    y = np.array(mydata[cur].loc[mask])
    x = np.array(mydata['Date'].loc[mask])
    x = np.datetime_as_string(x)
    x = np.array([temp[:10] for temp in x])
    
    df1 = pd.DataFrame(x,columns = ['Date'])
    df2 = pd.DataFrame(y,columns = ['Values'])
    df = pd.concat([df1,df2],axis = 1)
    
    json_data = df.to_json(orient='index')
    
    # create a json file with the data
    with open("values.json", "w") as json_file:
        json_file.write(json_data)
    
    return json_data


# In[10]:
    
def diffcurr(cur1, cur2, startdate, enddate):
    start = pd.to_datetime(startdate)
    end = pd.to_datetime(enddate)
    mask = (mydata['Date'] > start) & (mydata['Date'] <= end)

    x = mydata['Date'].loc[mask]
    x = x.dt.strftime('%Y-%m-%d')

    y1 = mydata[cur1].loc[mask]
    y2 = mydata[cur2].loc[mask]
    y = np.array(y2 / y1)

    result_dict = dict(zip(x, y))

    return result_dict

# In[11]:


def plot_fx_rates(currency, start_date, end_date):
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    currency_df = df[[currency]].loc[start_date:end_date]
    
    plt.figure(figsize=(8,6))
    plt.plot(currency_df.index, currency_df[currency], marker='o')
    plt.title(f'{currency} Exchange Rates ({start_date} to {end_date})')
    plt.xlabel('Date')
    plt.ylabel('FX Rate')
    plt.grid(True)
    plt.show()


# In[12]:


def get_json(currency, start_date, end_date):

    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # start_date = start_date.strftime('%Y-%m-%d')
    
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    # end_date = end_date.strftime('%Y-%m-%d')
    
    currency_df = df[currency].loc[start_date:end_date]
    
    currency_df.index = currency_df.index.strftime('%Y-%m-%d')
    
    json_data = currency_df.to_json(orient='index')
    
    # # create a json file with the data
    # with open("fx_rates.json", "w") as json_file:
    #     json_file.write(json_data)
    
    return json_data


# In[13]:


def get_min_rate(currency, start_date, end_date):
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    currency_df = df[[currency]].loc[start_date:end_date]
    
    lowest = currency_df[currency].min()
    
    return lowest


# In[14]:


def get_max_rate(currency, start_date, end_date):
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')
    
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    currency_df = df[[currency]].loc[start_date:end_date]
    
    highest = currency_df[currency].max()
    
    return highest


# In[15]:


# curr = input("Enter currency: ")
# start = input("Enter start date: ")
# end = input("Enter end date: ")


# In[16]:


# plot_fx_rates(curr, start, end)


# # In[17]:


# highest = get_max_rate(curr, start, end)
# highest


# # In[18]:


# lowest = get_min_rate(curr, start, end)
# lowest


# # In[19]:


# get_json(curr, start, end)


# # In[20]:


# values(curr, start, end)


# # In[21]:


# currency2 = input("Enter currency2: ")
# diffcurr(currency2, curr, start, end)

