import math
import time
from datetime import datetime

import ephem
import requests


def iterate_pointing_params(latitude, longitude, altitude):
    """
    Iterate over azimuth and elevation tuples pointing towards the ISS in real time, forever.
    """
    response = requests.get("https://api.wheretheiss.at/v1/satellites/25544/tles?format=json")
    iss_data = response.json()

    iss = ephem.readtle(
        'ISS',
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
        iss.compute(observer)
        yield math.degrees(iss.az), math.degrees(iss.alt),


if __name__ == '__main__':
    # pycamp_mendoza lat, lon, alt: -34, -68, 1075
    for azimuth, elevation in iterate_pointing_params(-34, -68, 1075):
        print('ISS: azimuth {}, elevation {}'.format(azimuth, elevation))
        time.sleep(1.0)
