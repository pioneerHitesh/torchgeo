#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import hashlib
import json
import os
import shutil

NUM_SAMPLES = 3


data_dir = "su_sar_moisture_content"

LABELS = {
    "type": "Feature",
    "properties": {
        "percent(t)": 132.6666667,
        "site": "Blackstone",
        "date": "6/30/15",
        "slope(t)": 0.599961042,
        "elevation(t)": 1522.0,
        "canopy_height(t)": 0.0,
        "forest_cover(t)": 130.0,
        "silt(t)": 36.0,
        "sand(t)": 38.0,
        "clay(t)": 26.0,
        "vv(t)": -12.80108143,
        "vh(t)": -20.86413967,
        "red(t)": 2007.5,
        "green(t)": 1669.5,
        "blue(t)": 1234.5,
        "swir(t)": 3226.5,
        "nir(t)": 2764.5,
        "ndvi(t)": 0.158611467,
        "ndwi(t)": -0.07713057,
        "nirv(t)": 438.5596345,
        "vv_red(t)": -0.006376628,
        "vv_green(t)": -0.007667614,
        "vv_blue(t)": -0.010369446,
        "vv_swir(t)": -0.003967482,
        "vv_nir(t)": -0.004630523,
        "vv_ndvi(t)": -80.70716267,
        "vv_ndwi(t)": 165.9663796,
        "vv_nirv(t)": -0.029188919,
        "vh_red(t)": -0.010393096,
        "vh_green(t)": -0.012497238,
        "vh_blue(t)": -0.016900883,
        "vh_swir(t)": -0.006466493,
        "vh_nir(t)": -0.007547166,
        "vh_ndvi(t)": -131.5424422,
        "vh_ndwi(t)": 270.5041557,
        "vh_nirv(t)": -0.047574236,
        "vh_vv(t)": -8.063058239,
        "slope(t-1)": 0.599961042,
        "elevation(t-1)": 1522.0,
        "canopy_height(t-1)": 0.0,
        "forest_cover(t-1)": 130.0,
        "silt(t-1)": 36.0,
        "sand(t-1)": 38.0,
        "clay(t-1)": 26.0,
        "vv(t-1)": -12.93716855,
        "vh(t-1)": -20.92368901,
        "red(t-1)": 1792.0,
        "green(t-1)": 1490.0,
        "blue(t-1)": 1102.5,
        "swir(t-1)": 3047.0,
        "nir(t-1)": 2574.0,
        "ndvi(t-1)": 0.179116009,
        "ndwi(t-1)": -0.084146807,
        "nirv(t-1)": 461.0691997,
        "vv_red(t-1)": -0.007219402,
        "vv_green(t-1)": -0.008682663,
        "vv_blue(t-1)": -0.011734393,
        "vv_swir(t-1)": -0.004245871,
        "vv_nir(t-1)": -0.005026095,
        "vv_ndvi(t-1)": -72.22787422,
        "vv_ndwi(t-1)": 153.7452097,
        "vv_nirv(t-1)": -0.02805906,
        "vh_red(t-1)": -0.011676166,
        "vh_green(t-1)": -0.014042744,
        "vh_blue(t-1)": -0.018978403,
        "vh_swir(t-1)": -0.00686698,
        "vh_nir(t-1)": -0.008128861,
        "vh_ndvi(t-1)": -116.8164094,
        "vh_ndwi(t-1)": 248.6569562,
        "vh_nirv(t-1)": -0.0453808,
        "vh_vv(t-1)": -7.986520458,
        "slope(t-2)": 0.599961042,
        "elevation(t-2)": 1522.0,
        "canopy_height(t-2)": 0.0,
        "forest_cover(t-2)": 130.0,
        "silt(t-2)": 36.0,
        "sand(t-2)": 38.0,
        "clay(t-2)": 26.0,
        "vv(t-2)": -13.07325567,
        "vh(t-2)": -20.98323835,
        "red(t-2)": 1721.5,
        "green(t-2)": 1432.0,
        "blue(t-2)": 1056.5,
        "swir(t-2)": 2950.0,
        "nir(t-2)": 2476.0,
        "ndvi(t-2)": 0.179768568,
        "ndwi(t-2)": -0.087357002,
        "nirv(t-2)": 445.0984812,
        "vv_red(t-2)": -0.007594107,
        "vv_green(t-2)": -0.009129368,
        "vv_blue(t-2)": -0.012374118,
        "vv_swir(t-2)": -0.004431612,
        "vv_nir(t-2)": -0.00527999,
        "vv_ndvi(t-2)": -72.72270011,
        "vv_ndwi(t-2)": 149.6532084,
        "vv_nirv(t-2)": -0.029371603,
        "vh_red(t-2)": -0.012188927,
        "vh_green(t-2)": -0.014653099,
        "vh_blue(t-2)": -0.019861087,
        "vh_swir(t-2)": -0.007112962,
        "vh_nir(t-2)": -0.008474652,
        "vh_ndvi(t-2)": -116.7236217,
        "vh_ndwi(t-2)": 240.2009889,
        "vh_nirv(t-2)": -0.047142912,
        "vh_vv(t-2)": -7.909982677,
        "slope(t-3)": 0.599961042,
        "elevation(t-3)": 1522.0,
        "canopy_height(t-3)": 0.0,
        "forest_cover(t-3)": 130.0,
        "silt(t-3)": 36.0,
        "sand(t-3)": 38.0,
        "clay(t-3)": 26.0,
        "vv(t-3)": -12.35794964,
        "vh(t-3)": -20.25746909,
        "red(t-3)": 1367.333333,
        "green(t-3)": 1151.0,
        "blue(t-3)": 827.3333333,
        "swir(t-3)": 2349.333333,
        "nir(t-3)": 2051.0,
        "ndvi(t-3)": 0.216978329,
        "ndwi(t-3)": -0.050717071,
        "nirv(t-3)": 413.3885932,
        "vv_red(t-3)": -0.009037993,
        "vv_green(t-3)": -0.010736707,
        "vv_blue(t-3)": -0.014937087,
        "vv_swir(t-3)": -0.005260194,
        "vv_nir(t-3)": -0.006025329,
        "vv_ndvi(t-3)": -56.95476465,
        "vv_ndwi(t-3)": 243.6644995,
        "vv_nirv(t-3)": -0.029894269,
        "vh_red(t-3)": -0.014815311,
        "vh_green(t-3)": -0.017599886,
        "vh_blue(t-3)": -0.024485257,
        "vh_swir(t-3)": -0.008622646,
        "vh_nir(t-3)": -0.009876874,
        "vh_ndvi(t-3)": -93.36171601,
        "vh_ndwi(t-3)": 399.4211186,
        "vh_nirv(t-3)": -0.049003454,
        "vh_vv(t-3)": -7.899519455,
    },
    "geometry": {"type": "Point", "coordinates": [-115.8855556, 42.44111111]},
}

STAC = {
    "assets": {
        "documentation": {
            "href": "../_common/documentation.pdf",
            "type": "application/pdf",
        },
        "labels": {"href": "labels.geojson", "type": "application/geo+json"},
        "training_features_descriptions": {
            "href": "../_common/training_features_descriptions.csv",
            "title": "Training Features Descriptions",
            "type": "text/csv",
        },
    },
    "bbox": [-115.8855556, 42.44111111, -115.8855556, 42.44111111],
    "collection": "su_sar_moisture_content",
    "geometry": {"coordinates": [-115.8855556, 42.44111111], "type": "Point"},
    "id": "su_sar_moisture_content_0001",
    "links": [
        {"href": "../collection.json", "rel": "collection"},
        {"href": "../collection.json", "rel": "parent"},
    ],
    "properties": {
        "datetime": "2015-06-30T00:00:00Z",
        "label:description": "",
        "label:properties": ["percent(t)"],
        "label:type": "vector",
    },
    "stac_extensions": ["label"],
    "stac_version": "1.0.0-beta.2",
    "type": "Feature",
}


def create_file(path: str) -> None:
    label_path = os.path.join(path, "labels.geojson")
    with open(label_path, "w") as f:
        json.dump(LABELS, f)

    stac_path = os.path.join(path, "stac.json")
    with open(stac_path, "w") as f:
        json.dump(STAC, f)


if __name__ == "__main__":
    # Remove old data
    if os.path.isdir(data_dir):
        shutil.rmtree(data_dir)

    os.makedirs(os.path.join(os.getcwd(), data_dir))

    for i in range(NUM_SAMPLES):
        sample_dir = os.path.join(data_dir, data_dir + f"_{i}")
        os.makedirs(sample_dir)
        create_file(sample_dir)

    # Compress data
    shutil.make_archive(data_dir, "gztar", ".", data_dir)

    # Compute checksums
    with open(data_dir + ".tar.gz", "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
        print(f"{data_dir}.tar.gz: {md5}")
