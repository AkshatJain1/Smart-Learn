
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
import urllib


# ** Data Sources **
# 
# - [Median Household Income (2006 - 2010)](https://www.psc.isr.umich.edu/dis/census/Features/tract2zip/)
# - [Educational Attainment Over 18 years old](https://www.census.gov/data/tables/2019/demo/educational-attainment/cps-detailed-tables.html)
# - [School Enrollment over 3 years old](https://www.census.gov/data/tables/2018/demo/school-enrollment/2018-cps.html)
# - [**County Level Education and Income**](https://www.ers.usda.gov/data-products/county-level-data-sets/download-data/)
# - [**California SAT Scores 15-16**](https://data.world/education/california-sat-report-2015-2016)

# In[2]:


edu = pd.read_excel('Education.xls')
edu.head()


# In[3]:


inc = pd.read_excel('Income.xls')
inc.head()


# In[4]:


sat = pd.read_excel('SAT Report 2015-2016.xls')
sat.head()


# In[5]:


# Enter your API key here 
api_key = "d3a9620b51e510dc9f95e04679c958ab"
  
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
# Give city name 
city_name = input("Enter city name : ") 
  
# complete_url variable to store 
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
  
# get method of requests module 
# return response object 
response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
x = response.json() 
  
print(x)
# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
  
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp"] 
  
    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidiy = y["humidity"] 
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
  
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
  
    # print following values 
    print(" Temperature (in kelvin unit) = " +
                    str(current_temperature) + 
          "\n atmospheric pressure (in hPa unit) = " +
                    str(current_pressure) +
          "\n humidity (in percentage) = " +
                    str(current_humidiy) +
          "\n description = " +
                    str(weather_description))
else: 
    print(" City Not Found ") 

