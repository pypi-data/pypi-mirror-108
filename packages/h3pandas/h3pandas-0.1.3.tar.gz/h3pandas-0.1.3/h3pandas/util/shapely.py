from typing import Union, Set
import shapely
from h3 import h3

MultiPolyOrPoly = Union[shapely.geometry.polygon.Polygon, shapely.geometry.multipolygon.MultiPolygon]

# TODO: Write everything properly

def extract_coords(p):
    outer = list(p.exterior.coords)
    inner = [list(g.coords) for g in p.interiors]
    return outer, inner

def polyfill(geometry: MultiPolyOrPoly,
                     res: int,
                     geo_json: bool = False) -> Set[str]:
    """h3.polyfill() accepting a shapely polygon

    Args:
        See h3.polyfill()

    Returns:
        Set of hex addresses
    """
    if isinstance(geometry, shapely.geometry.polygon.Polygon):
        outer, inner = extract_coords(geometry)
        return h3.polyfill_polygon(outer, res, inner, geo_json)

    elif isinstance(geometry, shapely.geometry.multipolygon.MultiPolygon):
        h3_addresses = []
        for poly in geometry.geoms:
            h3_addresses.extend(polyfill(poly, res, geo_json))

        return set(h3_addresses)
    else:
        raise ValueError(f"Unknown type {type(geometry)}")
