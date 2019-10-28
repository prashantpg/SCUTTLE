# Installation of pysicktim library is required for this program.

# This File performs the following:
# 1) grab a subset of the readings from the lidar for lightweight purposes
# 2) assign the proper angle value to the reading, with respect to robot x-axis
# 3) create a 2d array of [distances, angles] from the data

import numpy as np # for array handling
import pysicktim as lidar # required for communication with TiM561 lidar sensor

np.set_printoptions(suppress=True)  # Suppress Scientific Notation
start_angle = -135.0 # lidar points will range from -135 to 135 degrees

def polarScan(num_points):

    lidar.scan() #take reading

    # LIDAR data properties
    dist_amnt = lidar.scan.dist_data_amnt   # Number of distance data points reported from the lidar
    angle_res = lidar.scan.dist_angle_res   # Angular resolution reported from lidar

    # create the column of distances
    scan_points = np.asarray(lidar.scan.distances) #store the reported readings and cast as numpy.array
    inc_ang = (dist_amnt/(num_points+1))*angle_res  # Calculate angle increment for scan_points resized to num_points
    scan_points = np.asarray(np.array_split(scan_points,num_points))  # Split array into sections
    scan_points = [item[0] for item in scan_points]   # output first element in each section into a list
    scan_points = np.asarray(scan_points) # cast the list into an array
    scan_points = np.reshape(scan_points,(scan_points.shape[0],1)) # Turn scan_points row into column

    #create the column of angles
    angles = np.zeros(54)
    x = len(angles)
    for i in range(x): #run this loop
        angles[i] = (i*lidar.scan.dist_angle_res*lidar.scan.dist_data_amnt/num_points)+(start_angle)
    angles = np.reshape(angles,(angles.shape[0],1))  # Turn angles row into column

    #create the polar coordinates of scan
    scan_points = np.hstack((scan_points,angles))    # Turn two (54,) arrays into a single (54,2) matrix
    scan_points = np.round(scan_points,3) # Round each element in array to 3 decimal places

    return(scan_points)

# UNCOMMENT THIS SECTION TO RUN AS A STANDALONE PROGRAM
while (1):
    lidarData = polarScan(50)
    print(LidarData)
    time.sleep(2)
