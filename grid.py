
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
import time
import pandas as pd
import os

# original algorithm (Dijkstra 1959)
# Least cost route based on elevation, developed by Liang Diao
# ldiao@sfu.ca
# https://sites.google.com/view/liangdiao/home



start_time = time.time()

# require a grid stored as excel, each grid should have elevation, id attached
# empty column: mark prev visit
# need
excel_file = 'grid_clean.xlsx'
dt = pd.read_excel(
     os.path.join(excel_file),
     engine='openpyxl',
)
#dt = pd.read_excel(excel_file)
# set all nodes to unvisited, set all distance to source = 0
dt['visit'] = 0
dt['distance'] = 999999999
dt['mark'] = 0
# set initial node one point on the border
n0 = [60,151]
# set final node Haifa: [33,138]
n1 = [33,138]

#dt.loc[dt.b > 0, 'd'] = 1
print(dt.head())

# input a coordinate, return the id
def crd_id(n):
    if len(dt.loc[(dt['x'] == n[0]) & (dt['y']==n[1])]['id'])!=0:
        return dt.loc[(dt['x'] == n[0]) & (dt['y']==n[1])]['id'].values[0]
    else:
        return 'no'
#print(crd_id(n0))


# input an id, return the coordinate
def id_crd(id):
    if id <= len(dt):
        return [dt.loc[(dt['id'] == id)]['x'].values[0],dt.loc[(dt['id'] == id)]['y'].values[0]]
    else:
        return 'no'
#print(id_crd(623))

# update the distance of a node
def set_dis(id,d):
    dt.loc[dt.id == id, 'distance'] = d
'''
print(dt.loc[(dt.id == crd_id(n0))])
set_dis(crd_id(n0),100)
print(dt.loc[(dt.id == crd_id(n0))])
'''

# update the node to be visited
def set_visited(n):

    id = crd_id(n)
    dt.loc[dt.id == id, 'visit'] = 1
    print("node visited:",n[0], n[1])

# mark the best route
def set_mark(id):
    dt.loc[dt.id == id, 'mark'] = 1

# input a node, given a list of the neighbours
def neighbour(n):
    l=[]
    #print(n[0])
    #print(dt.loc[(dt['x'] == n[0]-1) & (dt['y']==n[1]-1)])
    #loop through the neighbours of the current node. and return the id of neighbours
    for (i,j) in zip([-1,-1,1,1],[-1,1,-1,1]):
        if crd_id([n[0]+i,n[1]+j]) != 'no' and dt.loc[(dt['id'] == crd_id([n[0]+i,n[1]+j]))]['visit'].values[0] == 0:
            l.append(crd_id([n[0]+i,n[1]+j]))
    return l
#set_visited(672)
#print(neighbour(n1))

#update the tentative distance of the current node's neighbours
def update_nb(n):
    id = crd_id(n)
    #print('current node d:', dt.loc[dt.id == id, 'visit'].values[0])
    for (i,j) in zip([0,0,-1,1],[-1,1,0,0]):

        id_nb = crd_id([n[0]+i,n[1]+j])
        if id_nb != 'no' and dt.loc[(dt['id'] == id_nb)]['visit'].values[0] == 0:
            current_d = dt.loc[(dt['id'] == id_nb)]['distance'].values[0]
            new_d = dt.loc[(dt['id'] == id)]['distance'].values[0]+terrain(id,id_nb)
            if new_d < current_d:
                print('tentative distance:',new_d)

                dt.loc[dt.id == id_nb, 'prev'] = id
                dt.loc[dt.id == id_nb, 'distance'] = new_d
        else: pass

#formula of the distance between two coordination, based on elevation diff.
def terrain(id1, id2):

    # according to Langmuir (1984), it takes 0.72 seconds to travel 1 meter horizontally;
    # an additional 6 seconds for each vertical meter uphill
    # going down a steep slope (>21.25%) adds an additional 2 seconds per vertical meter
    # going down a gentle slope (<21.25%) saves 2 seconds per vertical meter

    # the distance between grids in this file are 2.5km
    d = 2500 * 0.72
    if dt.loc[(dt['id'] == id1)]['elevation'].values[0] - \
            dt.loc[(dt['id'] == id2)]['elevation'].values[0] < 0:
        d += abs(dt.loc[(dt['id'] == id1)]['elevation'].values[0] -
                 dt.loc[(dt['id'] == id2)]['elevation'].values[0]) * 6
    elif dt.loc[(dt['id'] == id1)]['elevation'].values[0] - \
            dt.loc[(dt['id'] == id2)]['elevation'].values[0] > 531.25:
        d += abs(dt.loc[(dt['id'] == id1)]['elevation'].values[0] -
                 dt.loc[(dt['id'] == id2)]['elevation'].values[0]) * 2
    else:
        d += -abs(dt.loc[(dt['id'] == id1)]['elevation'].values[0] -
                  dt.loc[(dt['id'] == id2)]['elevation'].values[0]) * 2
    # print("terrain:",d)
    return d

# find the new current node with the lowest tentative distance among all unvisited nodes.
def current_node():
    min_d = dt.loc[(dt['visit'] == 0)]['distance'].min()
    id = dt.loc[(dt['distance'] == min_d) & (dt['visit'] == 0)]['id'].values[0]

    return id_crd(id)




#initialization staring node n0 end node n1, set initial node distance =0
def main_search(n0,n1):
    set_dis(crd_id(n0),0)
    print(dt.loc[(dt['id'] == crd_id(n1))]['distance'].values[0])

    while dt.loc[(dt['id'] == crd_id(n1))]['visit'].values[0] == 0:

        update_nb(n0)
        set_visited(n0)
        n0 = current_node()
        print(n0[0],n0[1])
        #print(dt.loc[(dt['id'] == crd_id(n0))]['distance'].values[0])

# mark the visited nodes reversely. starting from the end n1
def main_route(n1):
    temp_id = crd_id(n1)
    while len(dt.loc[(dt['id'] == temp_id)]['prev']) != 0:
        set_mark(temp_id)
        temp_id = dt.loc[(dt['id'] == temp_id)]['prev'].values[0]


main_search(n0,n1)
main_route(n1)
dt.to_csv("grid_result.csv", encoding='utf-8', index=False)
# The optimal route is labeled where “Mark” == 1
print(dt.loc[(dt['id'].isin(neighbour(n0)))][["id", "elevation", "distance"]])

print(dt.loc[(dt['x'] > 5) & (dt['x'] < 15) & (dt['y'] > 33) & (dt['y'] < 39)][
          ["id", "x", "y", "elevation", "distance", "visit", "prev","mark"]])

print("running time: --- %s seconds ---" % (time.time() - start_time))

#dataset[] dt.loc[(dt['x'] == n0[0]) & dt['y'].isin(n0[1])]
#movies["Net Earnings"] = movies["Gross Earnings"] - movies["Budget"]
#movies.to_excel('output.xlsx')

