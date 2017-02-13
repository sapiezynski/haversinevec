import numpy as np

R = 6378137.0
R_km = R/1000


def haversine(points, ref, radians=False):
    """ Calculate the great-circle distance bewteen a point or a set of points and a reference
    on the Earth surface.
    The ref can be a single point or a list of points that has the same length as the list
    """
    if radians:
        lat1, lon1 = split_columns(points)
        lat2, lon2 = split_columns(ref)

    else:
    # convert all latitudes/longitudes from decimal degrees to radians
        lat1, lon1 = split_columns(np.radians(points))
        lat2, lon2 = split_columns(np.radians(ref))

    # calculate haversine
    lat = lat2 - lat1
    lon = lon2 - lon1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon * 0.5) ** 2
    h = 2 * R_km * np.arcsin(np.sqrt(d))
    return h  # in kilometers


def haversine_pdist(points, radians = False):
    """ Calculate the great-circle distance bewteen each pair in a set of points
    """ 
    c = points.shape[0]
    result = np.zeros((c*(c-1)/2,), dtype=np.float64)
    vec_idx = 0
    if not radians:
        points = np.radians(points)
    for idx in range(0, c-1):
        ref = points[idx]
        temp = haversine(points[idx+1:c,:], ref, radians=True)
        result[vec_idx:vec_idx+temp.shape[0]] = temp
        vec_idx += temp.shape[0]
    return result

def split_columns(array):
    if len(array.shape) == 1:
        return array[0], array[1] # just a single row
    else:
        return array[:,0], array[:,1]