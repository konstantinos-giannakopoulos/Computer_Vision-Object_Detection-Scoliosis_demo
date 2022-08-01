#!/path/to/python

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 13:19:58 2021

@author: pongyuen
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys, os
import cv2

#def resource_path(relative_path):
#    if hasattr(sys, '_MEIPASS'):
#        return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)

#def resource_path(relative_path):
#    if getattr(sys, 'frozen', False):
#        # If the application is run as a bundle, the PyInstaller bootloader
#        # extends the sys module by a flag frozen=True and sets the app 
#        # path into variable _MEIPASS'.
#        application_path = sys._MEIPASS
#        return os.path.join(sys._MEIPASS, relative_path)
#    else:
#        application_path = os.path.dirname(os.path.abspath(__file__))
#        return os.path.join(os.path.abspath("."), relative_path)


def resource_path(relative_path):
    application_path = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(application_path, relative_path)


def count_how_many_times_slope_changes(angles):
    num_slope_changes = -1;
    last_sign = None
    for angle in angles :
        sign = np.sign(angle)
        if(sign != last_sign) :
            last_sign = sign
            num_slope_changes += 1
    return num_slope_changes

def define_shape(num_slope_changes):
    if(num_slope_changes <= 2):
        shape = 'C'
    else:
        shape = 'S'
    return shape

def split_angles_wrt_slope(angles):
    split_lists = []
    slopes = []
    length = len(angles)
    i = 0
    while i < length: 
        sign = np.sign(angles[i])
        split_list = []
        while(np.sign(angles[i]) == sign):
            split_list.append(angles[i])
            if (i+1 < length):
                i += 1
            else:
                i += 1
                break
        split_lists.append(split_list)
        if(sign<0):
            slopes.append(False)
        else:
            slopes.append(True)
    return split_lists, slopes



def remove_lists_with_one_element_and_small_angle(split_lists):
    filtered_lists = []
    length = len(split_lists)
    i = 1
    threshold = 3
    filtered_lists.append(split_lists[0])
    
    while i < length:
        split_list = split_lists[i]
        if(len(split_list) == 1):
            if(split_list[0] >= threshold) :
                filtered_lists.append(split_list)
        else:
            filtered_lists.append(split_list)
        i += 1
    return filtered_lists
            

def find_max_angle_in_each_slope(split_lists):
    max_angles = []
    for split_list in split_lists :
        print(split_list)
        max_angle_in_each_slope = np.max(np.absolute(split_list))
        print(max_angle_in_each_slope)
        max_angles.append(max_angle_in_each_slope)
    return max_angles
    

def estimate_Cobb_Angle(max_angles):
    cobb_angles = [max_angles[i + 1] + max_angles[i] for i in range(len(max_angles)-1)]
    return(cobb_angles)





def get_datapoint_from_angle(max_angles,final_datapoints__array, slopes):
    datapoints_with_slopes = []
    i = 0;
    for angle in max_angles:
        if(slopes[i] == False):
            angle = -angle;
        p = final_datapoints__array[np.where(final_datapoints__array[:,2] == angle)]
        datapoints_with_slopes.append(p)
        i += 1
    return datapoints_with_slopes


def draw_datapoints_to_image(datapoints,image_file):
    #image_file = '01-July-2019-91.jpg'
    orig_image = cv2.imread(image_file)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    
    for datapoint in datapoints:
        x,y = int(datapoint[0]), int(datapoint[1])
        modified_image = cv2.circle(image, (x,y), radius=5, color=(0, 0, 255), thickness=-1)
    
    final_image = 'sagittal/final_output.jpg'
    final_image = resource_path(final_image)
    cv2.imwrite(final_image, modified_image)
    print('Final Image saved.')

'''
def draw_lines_to_image(datapoints_with_slopes):
    image_file = 'sagittal/final_output.jpg'
    orig_image = cv2.imread(image_file)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    length = 200
    
    for datapoint in datapoints_with_slopes:
        datapoint = datapoint[0]
        x,y,angle = int(datapoint[0]),int(datapoint[1]),datapoint[2]
        
        theta = angle * np.pi / 180.0
        x2 = int(x + length * np.cos(theta))
        y2 = int(y + length * np.sin(theta))
        #print(theta,x2,y2)
        x1 = int(x - length * np.cos(theta))
        y1 = int(y - length * np.sin(theta))
        
        modified_image = cv2.line(image, (x-150,y), (x+150,y), color=(0, 255, 0), thickness=18)
        modified_image = cv2.line(image, (x1,y1), (x2,y2), color=(0, 0, 255), thickness=20)
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(modified_image,str(round(angle,2)),(x+100,y), font, 4,(255,0,0),5,cv2.LINE_AA)
    
    final_image = "sagittal/final_final_output.jpg"
    cv2.imwrite(final_image, modified_image)
    print('Final Image saved.')

    
def show_all_angles_to_image(final_datapoints__array):
    image_file = "sagittal/final_final_output.jpg"
    orig_image = cv2.imread(image_file)
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
    length = 200
    
    for datapoint in final_datapoints__array:
        #datapoint = datapoint[0]
        x,y,angle = int(datapoint[0]),int(datapoint[1]),round(datapoint[2],2)
        
        #modified_image = cv2.line(image, (x-100,y), (x+100,y), color=(0, 255, 0), thickness=5)
        #modified_image = cv2.line(image, (x1,y1), (x2,y2), color=(0, 0, 255), thickness=10)
    
        if (angle < 0):
            color = (250,20,20)  
        else:
            color = (50,250,20) 
    
        font = cv2.FONT_HERSHEY_SIMPLEX
        modified_image = cv2.putText(image,str(round(angle,2)),(x-600,y), font, 4,color,8,cv2.LINE_AA)
    
    final_image = "sagittal/final_final_output.jpg"
    cv2.imwrite(final_image, modified_image)
    print('Final Image saved.')
'''


def main(file):

    #file = "center_form_boxes_res_b_91.csv"
    #pwd = os.getcwd()
    #print(pwd)
    #print(os.path.dirname(file))
    #os.chdir(os.path.dirname(file))
    
    # read model output
    df = pd.read_csv(file)
    x,y,width,height,thetas = df['x_center'], df['y_center'],  df['width'], df['height'], df['angle']
    # convert thetas to degrees degrees
    thetas_in_degrees = thetas*(180/np.pi)
    #print('Degrees: ', degrees, '\n')
    
    # Find average y-distance (height) between datapoints.
    #average_datapoint_distance = np.average(height)
    #print('Average Datapoint Distance: ', average_datapoint_distance, '\n')
    
    center_datapoints = list(zip(x,y,thetas_in_degrees))
    #print('Center Datapoints: ', center_datapoints, '\n')
    
    # sort datapoints vertically
    sorted_datapoints = sorted(center_datapoints, key=lambda item: item[1])
    #print('Sorted Datapoints: ', sorted_datapoints, '\n')
    
    # reverse sprted datapoints list (bottom-up)
    rev_sorted_datapoints = sorted_datapoints[::-1]
    rev_sorted_datapoints_array = np.asarray(rev_sorted_datapoints)
    print('Reversed Sorted Datapoints: ', rev_sorted_datapoints, '\n')
    print('Reversed Sorted Datapoints Array:\n', rev_sorted_datapoints_array, '\n')
    
    final_datapoints__array = rev_sorted_datapoints_array
    
    image_file = 'sagittal/input_image.jpg'
    image_file = resource_path(image_file)
    # draw center datapoints in the image
    draw_datapoints_to_image(final_datapoints__array,image_file)
    
    # fill missing datapoints
    #final_datapoints_with_adding_extra__array = fillin_missing_datapoints(final_datapoints__array)
    
    #filter out angles less than 5 degrees
    unfiltered_angles = final_datapoints__array[:,2]
    print(unfiltered_angles)
    
    #filtered_angles = np.array(list(filter(lambda a: np.absolute(a) >= 5, unfiltered_angles)))
    
    #The angles
    #angles = rev_sorted_final_datapoints_array[:,2]
    angles = unfiltered_angles
    print(angles)
    
    
    
    
    '''
    
    print('\n\n------------ Results ------------')
    num_slope_changes = count_how_many_times_slope_changes(angles)
    print('The slope chages: ', num_slope_changes, ' times')
    
    shape = define_shape(num_slope_changes)
    print('Type of Scoliosis: ', shape,'-shape')
    
    split_lists, slopes = split_angles_wrt_slope(angles)
    #print(split_lists)
    
    filtered_lists = remove_lists_with_one_element_and_small_angle(split_lists)
    
    max_angles = find_max_angle_in_each_slope(filtered_lists)
    #print(max_angles)
    
    cobb_angles = estimate_Cobb_Angle(max_angles)
    print('Cobb Angle Estimation: ', cobb_angles)
    
    datapoints_with_slopes = get_datapoint_from_angle(max_angles,final_datapoints__array,slopes)
    #datapoints_with_slopes_array = np.array(datapoints_with_slopes)
    print('Datapoints with slopes: ', datapoints_with_slopes)
    
    # drawing
    #draw_lines_to_image(datapoints_with_slopes)
    #show_all_angles_to_image(final_datapoints__array)
    
    return num_slope_changes, shape, cobb_angles
    '''



if __name__ == '__main__': main()