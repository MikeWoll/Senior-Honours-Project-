"""
This script plot creates vertivle profile plots of O3.
Uses all MOZAIC flights information.
"""

import matplotlib.pyplot as pyplot
import os
import pandas as pd
import numpy as np

def main():
    path = "1998_Wet to Dry"
    data_files = os.listdir(path)
    
    #A function used to flatten lists within lists to a sigle list
    def flatten_list(_2d_list):
            flat_list = []
            # Iterate through the outer list
            for element in _2d_list:
                if type(element) is not float:
                    # If the element is of type list, iterate through the sublist
                    for item in element:
                        flat_list.append(item)
                else:
                        flat_list.append(element)
            return flat_list
        
    #individual lists created to hold lists of everyflight information 
    Alt_list = []
    Date_list = []
    O3_list = []
    
    #Loop to go through files
    for file in data_files:        
        with open(os.path.join(path,file)) as current_file:          
            #read line discription            
            all_lines = current_file.readlines()
            depart_time = all_lines[64]                      
            Date_list.append(depart_time)
            
        #opens folder reading the information            
        with open(os.path.join(path,file)) as current_file:    
            #opens folder and starts reading data at header=line#       
            df = pd.read_csv(current_file, sep = " ", header=72)            
        #Sets the parameters and what column the code should read      
        df = df[df["baro_alt_AC"] > -9999]
        df = df[df["O3_PM"] > -9999]
        df = df[df["UTC_time"] > -9999]
        df = df[df["lon"] < -40.7]
        df = df[df["lon"] > -45.7]
        df = df[df["lat"] < -20.3]
        df = df[df["lat"] > -25.3]
             
        #appends single flight information into list above
        O3_list.append(df["O3_PM"])
        Alt_list.append(df["baro_alt_AC"])
                              
    #turns lists or lists into a flattened array
    Alt_f_list = np.asarray(flatten_list(Alt_list))
    O3_f_list = np.asarray(flatten_list(O3_list))
        
    #list to hold average values over bins
    Alt_avg = []
    Alt_std = []
    O3_avg = []
    O3_std = []   
        
    #Bin Ranges
    dz = 500
    min_altitude = 1000
    max_altitude = 12000
    for ii in np.arange(min_altitude , max_altitude, dz):
            
        #O3 values within Altitude range, Average value, Std Value
        O3_range = O3_f_list[(Alt_f_list < ii + dz ) & (Alt_f_list > ii)]
        O3_avg_val = np.nanmean(O3_range)
        O3_std_val = np.std(O3_range)
      
        #Altitude values within Altitude range, Average value, Std Value
        Alt_range = Alt_f_list[(Alt_f_list < ii + dz ) & (Alt_f_list > ii)]
        Alt_mean = np.nanmean(Alt_range)
        Alt_std_val = np.std(Alt_range)
                
        O3_avg.append(O3_avg_val)
        O3_std.append(O3_std_val)        
        Alt_avg.append(Alt_mean)
        Alt_std.append(Alt_std_val)
    
    #finds number of flights used    
    N_flights = int(len(Date_list))              
    N = str(N_flights)
    
    fig, ax=pyplot.subplots(1, 1, figsize=(12, 8))
    size = 25
    #plot of average O3 vs altitude in bin ranges
    pyplot.errorbar(O3_avg, Alt_avg, yerr = None, xerr = O3_std, color = 'b', ecolor = 'lightsteelblue' , elinewidth = 5 , capsize = 5  )         
    pyplot.title("Veritcle Profile for O3" + "\n" + "Season: " + path + "\n" + "Number of flights:" + N , fontsize= size)
    pyplot.xlabel("O3 Value in ppb", fontsize= size)
    pyplot.ylabel("Altitude in meters", fontsize= size)
    ax.set_xlim(10, 82) #10, 82
    pyplot.show 
main()