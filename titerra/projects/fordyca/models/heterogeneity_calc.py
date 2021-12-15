import math
import statistics

"""
Finds nearest three neighbors for each cluster and calculates that distance from the neighbor to that cluster. 
Then list of distances for each of clusters variance will be measured to determine degree of 
heterogenity in the environmnent. 
"""

class clusterCalc():

    def __init__(self, clusterList, diagonal, arena_x = 0, arena_y = 0):
        self.clusterList = clusterList
        self.nearestNeighbors = {}
        self.diagonal = diagonal
        self.arena_x = arena_x 
        self.arena_y = arena_y
        self.area = self.arena_x * self.arena_y
        # self.nest_center_x = nest_center_x
        # self.nest_center_y = nest_center_y

    def calcNearestNeighbors(self):

        completeList = []

        for cluster in self.clusterList:
            nearestNeighbors = []
            nearestDistance = []
            coordinate = cluster.cluster_center
            (x, y) = coordinate
            for indiv_cluster in self.clusterList:
                indiv_coordinate = indiv_cluster.cluster_center
                x_ind, y_ind = indiv_coordinate
                if (indiv_coordinate == coordinate):
                    continue
                elif len(nearestNeighbors) < 3:
                    dist = math.sqrt((x - x_ind) ** 2 + (y - y_ind) ** 2)
                    nearestNeighbors.append(indiv_coordinate)
                    nearestDistance.append(dist)
                else:
                    dist = math.sqrt((x - x_ind)**2 + (y - y_ind)**2)
                    if min(nearestDistance) > dist:
                        index = nearestDistance.index(min(nearestDistance))
                        nearestDistance[index] = dist
                        nearestNeighbors[index] = (x_ind, y_ind)

            self.nearestNeighbors[coordinate] = nearestDistance
            nearestDistance.sort() # so that variance comparisons compare similar neighbors
            completeList.append(nearestDistance)
        return completeList

    # This will calculate the variance for the distances measured for each cluster and will be probably be a scaled metric to be
    # integrated into the existing PDF
    def calcVariance(self):
        complete_list = self.calcNearestNeighbors()
        complete_variance =  [statistics.variance(i) for i in zip(*complete_list)] # this is an array of variance of each neighbor, ordered from least to greatest distance
        return statistics.mean(complete_variance) # calculate mean variance across three neighbors

    def run(self):
        if (len(self.clusterList) == 1): # Handles SS case directly
           cx, cy  = self.clusterList[0].cluster_center
           dist = math.sqrt((cx - 3.2)**2 + (cy - 8)**2)
           return (dist / self.diagonal)*(1/self.area)

        elif (len(self.clusterList) == 2): # Handles DS case directly 
           leftx, lefty = (16, 8)
           cx1, cy1 = self.clusterList[0].cluster_center
           cx2, cy2 = self.clusterList[1].cluster_center
           left_calc = math.sqrt((cx1 - leftx) ** 2 + cy1 ** 2)
           right_calc = math.sqrt((cx2 + leftx) **2 + cy2 ** 2) 
           return (((left_calc + right_calc) / 2) / self.diagonal)*(2/self.area)

        self.calcNearestNeighbors()
        variance = self.calcVariance()
        return (variance / self.diagonal)*(len(self.clusterList)/self.area)


