import math
import time
from datetime import datetime

import ephem
import requests


API_URL = "https://api.wheretheiss.at/v1/satellites/{norad_id}/tles?format=json"


def iterate_pointing_params(sate_name, norad_id, latitude, longitude, altitude):
    """
    Iterate over azimuth and elevation tuples pointing towards a satellite in real time, forever.
    """
    response = requests.get(API_URL.format(norad_id=norad_id))
    iss_data = response.json()

    satellite = ephem.readtle(
        sate_name,
        iss_data['line1'],
        iss_data['line2'],
    )

    # don't set lat/lon as floats or ints, that means a different thing
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.elevation = altitude

    while True:
        observer.date = datetime.utcnow()
        satellite.compute(observer)
        yield math.degrees(satellite.az), math.degrees(satellite.alt),


if __name__ == '__main__':
    # pycamp_mendoza lat, lon, alt: -34, -68, 1075
    # iss norad id: 25544

    sate_name = 'ISS'
    real_time_pointer = iterate_pointing_params(
        sate_name=sate_name, norad_id=25544,  # satellite
        latitude=-34, longitude=-68, altitude=1075,  # observer
    )

    for azimuth, elevation in real_time_pointer:
        print('{}: azimuth {}, elevation {}'.format(sate_name, azimuth, elevation))
        time.sleep(1.0)
