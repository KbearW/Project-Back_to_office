import requests
import pprint

def geocode(location):
    url_location = requests.utils.quote(location)
    r = requests.get(f'https://api.mapbox.com/geocoding/v5/mapbox.places/{url_location}.json',
        {'access_token':'pk.eyJ1IjoiYmVhbmJhZzczOCIsImEiOiJja29rZ3d0aGIwMDh3MnBtMWp6dGcwMHVvIn0.prLY8xe96YLzfR5rBc8x3g'})
    
    # location= "4 World Trade Center, New York, New York 10006"
    # long:-74.012288, lat:40.7106775
    # return {"lat":111, "long":22}
    office_longitude=r.json()['features'][0]['center'][0]
    office_latitude=r.json()['features'][0]['center'][1]

    # print(location)
    # print(office_longitude, office_latitude)
    # print("Geocode function is working")

    return [r.json()['features'][0]['center'][0], r.json()['features'][0]['center'][1]]



# pprint.pprint(geocode("4 World Trade Center, New York, New York 10006"))
