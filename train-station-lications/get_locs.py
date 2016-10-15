import os
import time

import pandas
from mapbox import Geocoder


df_list = pandas.read_html(
    'https://en.wikipedia.org/wiki/List_of_railway_stations_in_India',
    header=0
)

for df in df_list[:-2]:
    df = df['State'].fillna(value='India')


geocoder = Geocoder()
geocoder.session.params['access_token'] = os.environ['MAPBOX_ACCESS_TOKEN']


with open('locations.csv', 'w') as f:
    for df in df_list:
        locations = df['Station Name'].str.cat(', '+df['State']+', India')
        for location in locations:
            time.sleep(1)
            response = geocoder.forward(location)
            try:
                latlong = response.geojson()['features'][0]['geometry']['coordinates']
                f.write("{}, {}, {}\n".format(location, latlong[0], latlong[1]))
            except:
                print response.geojson()
                f.write("{}, NA, NA\n".format(location))
                pass
