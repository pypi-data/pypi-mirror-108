# package raftel contains the function to plot list of s2id easily

import math
import s2sphere
from staticmap import StaticMap, Polygon

def _rad_to_degree(x):
    """
    Convert radian to degree (duh)
    """
    return x * 180 / math.pi


def get_s2id(lat, lon, level):
    """
    Given coordinates and the level, return the s2id that contains the coordinate
    """

    pos = s2sphere.LatLng.from_degrees(lat, lon)
    s2cell = s2sphere.CellId.from_lat_lng(pos).parent(level)

    return s2cell.id()


def get_region(lat, lon, radius, level):
    """
    Get a list of s2ids within the radius from specific lat and long at specified level
    Thanks to Gaurav's answer posted here: https://stackoverflow.com/questions/44649831/using-python-s2-s2sphere-library-find-all-s2-cells-of-a-particular-level-with
    """

    earthCircumferenceMeters = 1000 * 40075.017
    radius_radians = (2 * math.pi) * (float(radius) / earthCircumferenceMeters)
    
    latlng = s2sphere.LatLng.from_degrees(float(lat), float(lon)).normalized().to_point()

    region = s2sphere.Cap.from_axis_height(latlng, (radius_radians*radius_radians)/2)
    coverer = s2sphere.RegionCoverer()
    coverer.min_level = int(level)
    coverer.max_level = int(level)
    coverer.max_cells = 2**30
    covering = coverer.get_covering(region)
 
    s2ids = [cell.id() for cell in covering]

    return s2ids


def plot_s2id(s2ids, color='#00ff0088', auto_render=True, m=None):
    """
    Given list of s2id, plot the area in the map
    """
    if m is None:
        m = StaticMap(800, 600, 5, 5, url_template='http://a.tile.stamen.com/toner/{z}/{x}/{y}.png')

    for s2 in s2ids:

        s2cell = s2sphere.CellId(int(s2))
        s = s2sphere.Cell(s2cell)

        lon0, lat0 = _rad_to_degree(s.get_latitude(0, 0)), _rad_to_degree(s.get_longitude(0, 0))
        lon1, lat1 = _rad_to_degree(s.get_latitude(1, 1)), _rad_to_degree(s.get_longitude(1, 1))
        points = [[lat0, lon0], [lat0, lon1], [lat1, lon1], [lat1, lon0]]

        region = Polygon(points, color, 'black', 20)
        m.add_polygon(region)

    if auto_render:
        return m.render()
    return m
