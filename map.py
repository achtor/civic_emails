import folium
import pandas as pd
data = pd.read_csv('crimedata.csv')
#Import location
map_osm = folium.Map(location=[data.coords.ix[0],  data.coords.ix[1]],zoom_start=14,tiles='OpenStreetMap',width=1400,height=700)
for x in range(0,len(data.index)-1):
	map_osm.simple_marker([data.latitude.ix[x],data.longitude.ix[x]],
		popup=data.date.ix[x]+': '+data.primary_type.ix[x]+' (CPD Comment: '
		+data.description.ix[x]+')')
map_osm.circle_marker(location=[data.coords.ix[0],  data.coords.ix[1]],
	radius=75,
	popup='Your Location',
	fill_color='#FF0000')
map_osm.create_map(path='osm.html')