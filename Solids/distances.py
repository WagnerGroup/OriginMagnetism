import math
import os
import numpy as np
import json

#Define function to calculate distances from every atom and dump all to json
def calcdistances(coordinates):
    distances = []
    siteindex = []
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            distancestore = {'sites':[0,0],'distance':0}
            site = [int(coordinates[i]['site']),int(coordinates[j]['site'])]
            if 1==1:
                siteindex.append(site)
                xdist = (coordinates[i]['x']-coordinates[j]['x'])**2
                ydist = (coordinates[i]['y']-coordinates[j]['y'])**2
                zdist = (coordinates[i]['z']-coordinates[j]['z'])**2
                distancestore['distance']=round((math.sqrt((xdist)+(ydist)+(zdist))),2)
                distancestore['sites']=site
                distances.append(distancestore)

    with open('distances.json', 'w') as outfile:
        json.dump(distances, outfile)

#Make list of x,y,z coordinates for every atom
def main():
        f = open("autogen.d12.o")
        coordinates = []
        tempcoord ={'site':'0','x':0,'y':0,'z':0}
        for line in f.readlines():
         check = line.split()
         if len(check)==8 and check[0].isdigit() and (check[1]=='225' or check[1]=='208'):
            tempcoord['site']=str(int(check[0])-1)
            tempcoord['x']=float(check[2])
            tempcoord['y']=float(check[3])
            tempcoord['z']=float(check[4])
            coordinates.append(tempcoord)
            tempcoord={'site':'0','x':0,'y':0,'z':0}
        f.close()
        calcdistances(coordinates)
main()
