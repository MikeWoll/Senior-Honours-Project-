"""
This Creates a plot of average O3 Value vs Average Date between an altitude range
"""
import matplotlib.pyplot as pyplot
import os
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

#make sure the path is the location in the directory of the data
path = "Mozaic_1995_2000_Rio"
data_files = os.listdir(path)

#Lists to hold data appended to them
Date_list = []
O3_avg_list = []
#altitude Max and Min range
alt_min = 5000
alt_max = 8000

for file in data_files:

    with open(os.path.join(path,file)) as current_file:

        #prints for airport departures and arivales
        all_lines = current_file.readlines()
        depart_time = all_lines[64]
        #creates a numpy array of the Date for each flight and append the date
        Date_array = str(np.char.strip((np.array(depart_time)) , "start_UTC_time: "))
        Date_list.append(np.datetime64(Date_array)) 

    with open(os.path.join(path,file)) as current_file:    
        #opens folder and starts reading data at header=line#       
        df = pd.read_csv(current_file, sep = " ", header=72)

    #Sets the parameters and what column the code should read
    df = df[df["baro_alt_AC"] < 120000]       
    df = df[df["baro_alt_AC"] > -9999]
    df = df[df["O3_PM"] > -9999]
    df = df[df["UTC_time"] > -9999]
    df = df[df["lon"] < -40.7]
    df = df[df["lon"] > -45.7]
    df = df[df["lat"] < -20.3]
    df = df[df["lat"] > -25.3]        

    #this is to convert altitude and O3 into an array        
    Alt_array = np.asarray(df["baro_alt_AC"])
    O3_array = np.asarray(df["O3_PM"])      

    #creates a range of height   
    Alt_range = (Alt_array < alt_max) & (Alt_array > alt_min) 

    O3_alt_range = O3_array[Alt_range]
    #average O3 value over altitude range
    O3_alt_avg = np.nanmean(O3_alt_range)
    #append the value to the O3 list above
    O3_avg_list.append(O3_alt_avg)

#turns the Lists into arrays   
Date_asarray = np.asarray(Date_list)
O3_asarray = np.asarray(O3_avg_list)    

#list to hold average values over bins
Date_avg = []
Date_std = []
O3_avg = []
O3_std = []

min_date = np.datetime64("1995-01-01T00:00:01")
max_date = np.datetime64("1999-12-30T22:00:01")

## iterate in this way, avoid error
for ii in np.arange( min_date , max_date, dtype='datetime64[M]'):
    #use mdates.date2num to convert datetime into number values, then it works
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range)
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    Date_mean = np.nanmean(Date_range)
    Date_std_val = np.std(Date_range)

    O3_avg.append(O3_avg_val)
    O3_std.append(O3_std_val)
    Date_avg.append(Date_mean)
    Date_std.append(Date_std_val)

test_dateavg = np.asarray(Date_avg)
test_o3avg = np.asarray(O3_avg)
test_o3std = np.asarray(O3_std)
color1= "b"
color2 = "lightsteelblue"

fig, ax=pyplot.subplots(1, 1, figsize=(15, 7))

pyplot.scatter(mdates.num2date(test_dateavg[~np.isnan(test_dateavg)]), test_o3avg[~np.isnan(test_dateavg)], color = color1 )
#plot of average O3 measurmeant per month vs Date.
pyplot.errorbar(mdates.num2date(test_dateavg[~np.isnan(test_dateavg)]), test_o3avg[~np.isnan(test_dateavg)], yerr = test_o3std[~np.isnan(test_dateavg)] , xerr = None , color = color1 , ecolor = color2 , elinewidth = 3 , capsize = 3  )
pyplot.title("Date vs O3"  + "\n" + "Altitude between: " + str(alt_min) + "-" + str(alt_max), fontsize = 35 )
pyplot.xlabel("Date", fontsize = 35)
pyplot.ylabel("O3 in ppb", fontsize = 35)

# Minor ticks every month.
fmt_month = mdates.MonthLocator()
# Minor ticks every year.
fmt_year = mdates.YearLocator()

ax.xaxis.set_minor_locator(fmt_month)
# '%b' to get the names of the month
ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax.xaxis.set_major_locator(fmt_year)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# fontsize for month labels
ax.tick_params(labelsize=8, which='both')
# create a second x-axis beneath the first x-axis to show the year in YYYY format
sec_xaxis = ax.secondary_xaxis(-0.1)
sec_xaxis.xaxis.set_major_locator(fmt_year)
sec_xaxis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Hide the second x-axis spines and ticks
sec_xaxis.spines['bottom'].set_visible(False)
sec_xaxis.tick_params(length=0, labelsize=30)

#Sets the Y axis size
ax.set_ylim(20, 77)

pyplot.tight_layout()
pyplot.show()

