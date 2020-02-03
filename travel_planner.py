import tsp
import numpy as np
import math
import requests

def get_api(source, dest):
    gmaps_key = 'AIzaSyDY_S0w86f3HM9RLeisjeAefQ-bs0w6T2M'
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    r = requests.get(url + 'origins=' + source +
                     '&destinations=' + dest +
                     '&key=' + gmaps_key)
    x = r.json()
    x = dict(x)
    distance = str(x['rows'][0]['elements'][0]['distance']['text']).replace(" km", "").replace(",", "")
    return float(distance)


def distance_calculation():
    #determine the ending of a loop.
    flag = 1
    #geolist
    list = []
    # get the starting point
    dimensions = input("please enter 1 to start your journey ...\nand enter 0 to end...")
    if dimensions == "1":
        dimensions = input("\nplease input the source & dest to start your journey...")
        list.append(dimensions)
        while flag == 1:
                #prompt the in-between places
            dimensions = input("\nplease input any place within your journey...")
            if dimensions == "0":
                flag = 0
            else:
                list.append(dimensions)
    else:
        print("\nyour journey ends...\n")

    print("the places you wanna go are ",list," , and you wanna go back to ",list[0]," after this busy day..")

    #construct a source-destination pair
    source_dest_pair = []
    for i in range(0,len(list)):
        #source;
        source = list[i]
        for j in range(i+1,len(list)):
            #destination
            temp = []
            temp.append(source)
            dest = list[j]
            temp.append(dest)
            source_dest_pair.append(temp)

    ####
    distance_list=[]
    loops = int(math.factorial(len(list)) / (2*math.factorial(len(list)-2)))
    #as if we've got the distance;
    for i in range(loops):
        distance_list.append(get_api(source_dest_pair[i][0],source_dest_pair[i][1]))

    #print(distance_list)


    distance_matrix=[]
    for i in range(0,len(list)):
        temp_matrix = [0] * len(list)
        distance_matrix.append(temp_matrix)

    temp_list_row = distance_list.copy()

    for i in range(0,distance_matrix.__len__()):
        # for each source
        for j in range(i+1,distance_matrix.__len__()):
            distance_matrix[i][j] = temp_list_row.pop(0)

    temp_list_col = distance_list.copy()

    for i in range(0,distance_matrix.__len__()):
        # for each source
        for j in range(i+1,distance_matrix.__len__()):
            distance_matrix[j][i] = temp_list_col.pop(0)


    print(distance_matrix)
    # print(distance_list)



    r = range(len(distance_matrix))
    #
    #construct a path matrix and put it into a dictionary
    shortestpath = {(i,j): distance_matrix[i][j] for i in r for j in r}

    #print(tsp.tsp(r,shortestpath)[1])
    print("----------------------------------------------")
    print("\nyour travel routine is ")

    for i in range(len(tsp.tsp(r,shortestpath)[1])):
        print(list[tsp.tsp(r,shortestpath)[1][i]],end=" -> ")
    print(list[0],end="")
    print(", and the total distance of travel is: ",tsp.tsp(r,shortestpath)[0], " km.")


if __name__ == '__main__':
    #assumption: 1. 一天是一个loop；
    # 2. 来回距离一样；
    # 3. be as specific as you can about the name of your place of interest
    # 4. by car.
    distance_calculation()

import gmaps