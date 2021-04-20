import folium
import re
import csv
pubs_data = []
with open('london_pubs.csv', 'r') as numPub:
    pubs = csv.DictReader(numPub)
    for row in pubs:
        pubs_data.append(row)
# create map
map_pubs = folium.Map(location=[51.51, -0.12], zoom_start=12)
# plot pub locations
for row in pubs_data:
    try:
        popup_text = "{}\n{}".format(re.sub(r'[^A-Za-z0-9 ]+', '', row['name']), row['local_authority'])
        folium.Marker(location=[float(row['latitude']), float(row['longitude'])], popup=popup_text).add_to(map_pubs)
    except ValueError:
        continue
# display(map_pubs)
map_pubs.save('london_pubs.html')