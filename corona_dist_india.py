import requests
from geopy.geocoders import Nominatim
import folium
import os
import webbrowser
import time


def check_key(dick,key):
	if key in dick.keys():
		dick[key]=dick[key]+1
		return dick
	else:
		dick[key]=1
		return dick

def data_cities():
	r=requests.get("https://api.covid19india.org/raw_data.json")
	data=r.json()
	patients=data["raw_data"]
	dick={}
	dummy={}
	for patient in patients:
		if patient["detectedcity"]=="":
			if patient["detecteddistrict"]=="" and patient["detectedstate"]!="":
				pat_city=patient["detectedstate"]
				dick=check_key(dick,pat_city)
				dummy=check_key(dummy,pat_city)
			elif patient["detecteddistrict"]!="":
				pat_city=patient["detecteddistrict"]
				dick=check_key(dick,pat_city)
				dummy=check_key(dummy,pat_city)
			#map_lat_lon(pat_city)
		elif patient["detectedcity"]!="":
			pat_city=patient["detectedcity"]
			dick=check_key(dick,pat_city)
			dummy=check_key(dummy,pat_city)
	ip_map=folium.Map(location=["19.07","72.87"])
	print(len(dick.keys()))
	for key in dick.keys():
		if dummy[key]<50:
			dummy.pop(key)
	dick=dummy
	print(len(dick.keys()))
	for key in dick.keys():
		ip_map=map_lat_lon(ip_map,key,dick[key])
	ip_map.save("corona.html")
	webbrowser.open("file://"+os.path.realpath("corona.html"))

def map_lat_lon(imap,city,count):
	geolocator = Nominatim(user_agent="san")
	locate = geolocator.geocode(city)
	if locate!=None:
		try:
			print(locate)
			lat=locate.latitude
			lon=locate.longitude
			print(city)
			print(lat,lon)
			#ip_map=folium.Map(location=[lat,lon])
			#htm="<i>"+count+"</i>"
			folium.Marker([lat,lon],popup=count,tooltip=city).add_to(imap)
			#time.sleep(1)
			return imap
		except:
			return imap
	return imap



data_cities()
#ip_map.save("corona.html")
#webbrowser.open("file://"+os.path.realpath("corona.html"))
