import numpy as np

R = 6378137.0
R_km = R/1000


def haversine(points_a, points_b, radians=False):
    """ 
    Calculate the great-circle distance bewteen points_a and points_b
    points_a and points_b can be a single points or lists of points
    """
    if radians:
        lat1, lon1 = _split_columns(points_a)
        lat2, lon2 = _split_columns(points_b)

    else:
    # convert all latitudes/longitudes from decimal degrees to radians
        lat1, lon1 = _split_columns(np.radians(points_a))
        lat2, lon2 = _split_columns(np.radians(points_b))

    # calculate haversine
    lat = lat2 - lat1
    lon = lon2 - lon1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon * 0.5) ** 2
    h = 2 * R_km * np.arcsin(np.sqrt(d))
    return h  # in kilometers


def haversine_pdist(points, radians = False):
    """ 
    Calculate the great-circle distance bewteen each pair in a set of points
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


def haversine_cdist(points_a, points_b, radians=False):
    """ 
    Calculate the great-circle distance bewteen each combination of points in two lists
    """
    if not radians:
        points_a = np.radians(points_a)
        points_b = np.radians(points_b)
    
    if points_a.ndim == 1:
        m = 1
    else:
        m = points_a.shape[0]

    if points_b.ndim == 1:
        n = 1
    else:
        n = points_b.shape[0]
    
    result = np.zeros((m, n), dtype=np.float64)
    for idx in range(0, points_a.shape[0]):
        result[idx,:] = haversine(points_a[idx], points_b, radians=True)
    return result

def _split_columns(array):
    if array.ndim == 1:
        return array[0], array[1] # just a single row
    else:
        return array[:,0], array[:,1]


