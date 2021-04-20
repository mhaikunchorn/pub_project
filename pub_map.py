import folium
from folium import plugins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.display import display, HTML
import csv
import csv
pubs_data = []
with open('london_pubs.csv', 'r') as numPub:
    pubs = csv.DictReader(numPub)
    for row in pubs:
        pubs_data.append(row)
# Print sales data in nice rows:
# pprint(sales_data)
def get_la_from_row(pubs_data_row):
    return pubs_data_row['Local Authority']
def get_pubs_from_row(pubs_data_row):
    return int(pubs_data_row['Number of Pubs'])
def get_lat_from_row(pub_data_row):
    return int(pub_data_row(['Latitude']))
def get_lng_from_row(pub_data_row):
    return int(pub_data_row(['Longitude']))
# def get_name_from_row(pubs_data_row):
    # return pubs_data_row['Name of Pubs']
#find latitude and logitude of first value
print(pubs_data[0])
#create map
map_pubs = folium.Map([51.606027,-0.172783], zoom_start=5.5, control_scale=True)
#address latitude and longitude
# address_lat = row['Latitude']
# address_lng = row['Longitude']
# address_lat = len(pubs_data, key=get_lat_from_row)
# address_lng = len(pubs_data, key=get_lng_from_row)
# address_lating = [address_lat,address_lng]
# folium.Marker(address_lating, popup=row.loc['name'], tooltip='click').add_to(map_pubs)
#plot pub locations
for row in pubs_data.__iter__():
    folium.Marker(location=[row['latitude'], row['longitude']],
                  popup=row['name'] + ' ' + row['local_authority'],
                  tooltip='click').add_to(map_pubs)
display(map_pubs)
map_pubs.save('london_pubs.html')