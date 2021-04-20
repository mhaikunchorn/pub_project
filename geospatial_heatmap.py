## Geospatial heat map
import folium
import csv
import geocoder
from folium import plugins
pubs_data = []
with open('london_pubs.csv', 'r') as numPub:
    pubs = csv.DictReader(numPub)
    for row in pubs:
        pubs_data.append(row)
#get location data for boroughs (latitude and logitude]
camden = geocoder.osm('Camden, London')
hackney = geocoder.osm('Hackney, London')
hammersmith = geocoder.osm('Hammersmith, London')
islington = geocoder.osm('Islington')
kensington_and_chelsea = geocoder.osm('Kensington and Chelsea, London')
lambeth = geocoder.osm('Lambeth, London')
lewisham = geocoder.osm('Lewisham, London')
southwark = geocoder.osm('Southwark, London')
tower_hamlets = geocoder.osm('Tower Hamlets, London')
wandsworth = geocoder.osm('Wandsworth, London')
westminster = geocoder.osm('Westminster,London')
barking = geocoder.osm('Barking, London')
barnet = geocoder.osm('Barnet, London')
bexley = geocoder.osm('Bexley, London')
croydon = geocoder.osm('Croydon, London')
ealing = geocoder.osm('Ealing, London')
enfield = geocoder.osm('Enfield, London')
haringey = geocoder.osm('Haringey, London')
harrow = geocoder.osm('Harrow, London')
havering = geocoder.osm('Havering, London')
hillingdon = geocoder.osm('Hillingdon, London')
hounslow = geocoder.osm('Hounslow, London')
kingston_upon_thames = geocoder.osm('Kingston upon Thames, London')
merton = geocoder.osm('Merton, London')
newham = geocoder.osm('Newham, London')
redbridge = geocoder.osm('Redbridge, London')
richmond_upon_thames = geocoder.osm('Richmond upon Thames, London')
sutton = geocoder.osm('Sutton, London')
waltham_forest = geocoder.osm('Waltham Forest, London')
greenwich = geocoder.osm('Greenwich, London')
brent = geocoder.osm('Brent, London')
bromley = geocoder.osm('Bromley, London')
city_of_london = geocoder.osm('City of London, London')
#create latitude and longitude, intensity for heat map
#intensity is number of pubs scaled down so heat dots are more readable
camden_latlng = [camden.lat, camden.lng, 276]
hackney_latlng = [hackney.lat,hackney.lng, 327]
hammersmith_latlng = [hammersmith.lat, hammersmith.lng, 149]
islington_latlng = [islington.lat, islington.lng, 255]
kensington_and_chelsea_latlng = [kensington_and_chelsea.lat, kensington_and_chelsea.lng, 110]
lambeth_latlng = [lambeth.lat, lambeth.lng, 168]
lewisham_latlng = [lewisham.lat, lewisham.lng, 79]
southwark_latlng = [southwark.lat, southwark.lng, 209]
tower_hamlets_latlng = [tower_hamlets.lat, tower_hamlets.lng, 1]
wandsworth_latlng = [wandsworth.lat, wandsworth.lng, 175]
westminster_latlng = [westminster.lat, westminster.lng, 390]
barking_latlng = [barking.lat, barking.lng, 4]
barnet_latlng = [barnet.lat, barnet.lng, 109]
bexley_latlng = [bexley.lat, bexley.lng, 4]
croydon_latlng = [croydon.lat, croydon.lng, 26]
ealing_latlng = [ealing.lat, ealing.lng, 7]
enfield_latlng = [enfield.lat, enfield.lng, 87]
haringey_latlng = [haringey.lat, haringey.lng, 95]
harrow_latlng = [harrow.lat, harrow.lng, 9]
havering_latlng = [havering.lat, havering.lng, 0]
hillingdon_latlng = [hillingdon.lat, hillingdon.lng, 8]
hounslow_latlng = [hounslow.lat, hounslow.lng, 1]
kingston_upon_thames_latlng = [kingston_upon_thames.lat, kingston_upon_thames.lng, 1]
merton_latlng = [merton.lat, merton.lng, 56]
newham_latlng = [newham.lat, newham.lng, 42]
redbridge_latlng = [redbridge.lat, redbridge.lng, 0]
richmond_upon_thames_latlng = [richmond_upon_thames.lat, richmond_upon_thames.lng, 3]
sutton_latlng = [sutton.lat, sutton.lng, 6]
waltham_forest_latlng = [waltham_forest.lat, waltham_forest.lng, 1]
greenwich_latlng = [greenwich.lat, greenwich.lng, 0]
brent_latlng = [brent.lat, brent.lng, 72]
bromley_latlng = [bromley.lat, bromley.lng, 22]
city_of_london_latlng = [city_of_london.lat, city_of_london.lng, 244]
#create list of boroughs with laitutide and longitude, intensity
large_boroughs = [camden_latlng, hackney_latlng, hammersmith_latlng, islington_latlng, kensington_and_chelsea_latlng,
                  lambeth_latlng, lewisham_latlng, southwark_latlng, tower_hamlets_latlng, wandsworth_latlng,
                  westminster_latlng, barking_latlng, barnet_latlng, bexley_latlng, croydon_latlng, ealing_latlng,
                  enfield_latlng, haringey_latlng, harrow_latlng, havering_latlng, hillingdon_latlng, hounslow_latlng,
                  kingston_upon_thames_latlng, merton_latlng, newham_latlng, redbridge_latlng,
                  richmond_upon_thames_latlng, sutton_latlng, waltham_forest_latlng, greenwich_latlng, brent_latlng,
                  bromley_latlng, city_of_london_latlng]
map_heatmap = folium.Map(location=[51.51, -0.12], zoom_start=12)
plugins.HeatMap(large_boroughs).add_to(map_heatmap)
map_heatmap.save('ldn_pubs_heat.html')
print('Success! Open ldn_pubs_heat.html in the browser...')
