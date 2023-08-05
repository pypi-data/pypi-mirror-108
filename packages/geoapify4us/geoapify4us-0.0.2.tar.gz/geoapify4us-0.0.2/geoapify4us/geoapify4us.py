#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
import urllib
import json

class GeoAPIfy4us:
  
  def __init__(self):
    self.url = 'https://api.geoapify.com/'

  def single_isoline(self, lat = 37.3, lon = 127.1, cal_type = 'distance', cal_mode = 'walk', search_range = 30, apiKey = 'YOUR_API_KEY', filename = 'single_isoline'):
    self.filename = filename
    self.apiKey = apiKey
    new_query_parts = []

    if cal_type =='distance':
      single_range = search_range * 1000
    elif cal_type =='time':
      single_range = search_range * 60
    else:
      print("That was no valid text. Please put the word, 'distance' or 'time'.")

    self.url = self.url + 'v1/isoline?'
    keys = ['lat', 'lon', 'type', 'mode', 'range', 'apiKey']
    values = [lat, lon, cal_type, cal_mode, single_range, apiKey]

    for i in keys:
      new_query_parts.append(i + '=' + str(values[keys.index(i)]))

    new_query = "&".join(new_query_parts)
    new_url = self.url + new_query
    request = urllib.request.Request(new_url)
    response = urllib.request.urlopen(request)
    
    if response.getcode() == 200:
      try:
        responseData = response.read()
        data = responseData.decode('utf-8')
        s = json.dumps(data, indent=4, sort_keys=True)
        fname = '{}.json'.format(self.filename)
        with open(fname, 'w') as outfile:
          outfile.write(s)
          print("{}.json file is created. Please check the file.".format(self.filename))
      except:
        print("There is an error in data handling. Please check the process...")
    else :
      print("URL response has an error. Please check the response...")


  def multi_isoline(self, lat = 37.3, lon = 127.1, cal_type = 'distance', cal_mode = 'walk', search_range = '5, 10, 15', apiKey = 'YOUR_API_KEY', filename = 'multi_isoline'):
    self.filename = filename
    self.apiKey = apiKey
    range_units, new_query_parts = [], []

    replaced = re.sub('[-=.#/?:$}{ ]', '',search_range)
    range_list = replaced.split(',')
    
    if cal_type =='distance':
      for each_range in range_list:
        range_units.append(int(each_range) * 1000)
    elif self.cal_type =='time':
      for each_range in range_list:
        range_units.append(int(each_range) * 60)
    else:
      print("That was no valid text. Please put 'distance' or 'time'.")

    self.url = self.url + 'v1/isoline?'
    keys = ['lat', 'lon', 'type', 'mode', 'range', 'apiKey']
    values = [lat, lon, cal_type, cal_mode, range_units, apiKey]

    for i in keys:
      if i == 'range':
        for j in range_units:
          new_query_parts.append(i + '=' + str(j))
      else:
        new_query_parts.append(i + '=' + str(values[keys.index(i)]))

    new_query = "&".join(new_query_parts)
    new_url = self.url + new_query
    request = urllib.request.Request(new_url)
    response = urllib.request.urlopen(request)
    
    if response.getcode() == 200:
      try:
        responseData = response.read()
        data = responseData.decode('utf-8')
        s = json.dumps(data, indent=4, sort_keys=True)
        fname = '{}.json'.format(self.filename)
        with open(fname, 'w') as outfile:
          outfile.write(s)
          print("{}.json file is created. Please check the file.".format(self.filename))
      except:
        print("There is an error in data handling. Please check the process...")
    else :
      print("URL response has an error. Please check the response...")

