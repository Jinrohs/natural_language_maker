#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import csv
from collections import defaultdict

def convert_geocode(lat, lon):
    grid = find_grid(zoom, lat, lon)
    res = worldgeo_data["{0}/{1}".format(grid[0], grid[1])]
    if not len(res):
        return None
    return res[0]

def find_grid(zoom, lat, lon):
    ngrid = 2 ** zoom
    xmin = -180.0
    xmax = 180.0
    ymin = 90.0
    ymax = -90.0    
    dx = (xmax - xmin)/float(ngrid)
    dy = (ymax - ymin)/float(ngrid)
    nx = int(round((lon - xmin)/dx))
    ny = int(round((lat - ymin)/dy))	
    return (nx, ny)

zoom = 6
worldgeo_data = defaultdict(list)
with open("worldgeo.csv") as fp:
    reader = csv.reader(fp)
    header = next(reader)
    for line in reader:
        name, lat, lon = (line[2], float(line[7]), float(line[8]))
        grid = find_grid(zoom, lat, lon)
        #print name, grid, lon, lat
        worldgeo_data["{0}/{1}".format(grid[0], grid[1])].append(name)

if __name__ == '__main__':
    geo = [53.9, 27.5] # ベラルーシ
    print convert_geocode(geo[0], geo[1])


