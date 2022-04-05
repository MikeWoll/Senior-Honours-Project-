"""
This creates a plot showing each years average date vs O3 value using MOZAIC data
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
alt_min = 8000
alt_max = 12000

for file in data_files:

    with open(os.path.join(path,file)) as current_file:

        #Read airport departure times
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
    #sets the area to look within
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
Date_avg_1995 = []
Date_std_1995 = []
O3_avg_1995 = []
O3_std_1995 = []

#time period to loop over
min_date_1995 = np.datetime64("1995-01-01T00:00:01")
max_date_1995 = np.datetime64("1995-12-31T23:59:59")

## iterate in this way, avoid error
for ii in np.arange( min_date_1995 , max_date_1995, dtype='datetime64[M]'):
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range) 
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    year = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))    #subtract year behind 
    normalize = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))   #leave as 1994 for normalization
    Date_mean = np.nanmean(Date_range) - year + normalize
    Date_std_val = np.std(Date_range)

    O3_avg_1995.append(O3_avg_val)
    O3_std_1995.append(O3_std_val)
    Date_avg_1995.append(Date_mean)
    Date_std_1995.append(Date_std_val)

#turns the list of values into an array
dateavg_1995 = np.asarray(Date_avg_1995)
o3avg_1995 = np.asarray(O3_avg_1995)
o3std_1995 = np.asarray(O3_std_1995)


#Loop repeated for next year
Date_avg_1996 = []
Date_std_1996 = []
O3_avg_1996 = []
O3_std_1996 = []


min_date_1996 = np.datetime64("1996-01-01T00:00:01")
max_date_1996 = np.datetime64("1996-12-31T23:59:59")

## iterate in this way, avoid error
for ii in np.arange( min_date_1996 , max_date_1996, dtype='datetime64[M]'):
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range) 
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    year = mdates.date2num(np.datetime64("1995-12-31T23:59:59"))    #subtract year behind 
    normalize = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))   #leave as 1994 for normalization
    Date_mean = np.nanmean(Date_range) - year + normalize
    Date_std_val = np.std(Date_range)

    O3_avg_1996.append(O3_avg_val)
    O3_std_1996.append(O3_std_val)
    Date_avg_1996.append(Date_mean)
    Date_std_1996.append(Date_std_val)

dateavg_1996 = np.asarray(Date_avg_1996)
o3avg_1996 = np.asarray(O3_avg_1996)
o3std_1996 = np.asarray(O3_std_1996)

#Next Year repeated
Date_avg_1997 = []
Date_std_1997 = []
O3_avg_1997 = []
O3_std_1997 = []

min_date_1997 = np.datetime64("1997-01-01T00:00:01")
max_date_1997 = np.datetime64("1997-12-31T23:59:59")

## iterate in this way, avoid error
for ii in np.arange( min_date_1997 , max_date_1997, dtype='datetime64[M]'):
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range) 
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    year = mdates.date2num(np.datetime64("1996-12-31T23:59:59"))    #subtract year behind 
    normalize = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))   #leave as 1994 for normalization
    Date_mean = np.nanmean(Date_range) - year + normalize
    Date_std_val = np.std(Date_range)

    O3_avg_1997.append(O3_avg_val)
    O3_std_1997.append(O3_std_val)
    Date_avg_1997.append(Date_mean)
    Date_std_1997.append(Date_std_val)

dateavg_1997 = np.asarray(Date_avg_1997)
o3avg_1997 = np.asarray(O3_avg_1997)
o3std_1997 = np.asarray(O3_std_1997)

#Next Year repeated
Date_avg_1998 = []
Date_std_1998 = []
O3_avg_1998 = []
O3_std_1998 = []

min_date_1998 = np.datetime64("1998-01-01T00:00:01")
max_date_1998 = np.datetime64("1998-12-31T23:59:59")

## iterate in this way, avoid error
for ii in np.arange( min_date_1998 , max_date_1998, dtype='datetime64[M]'):
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range) 
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    year = mdates.date2num(np.datetime64("1997-12-31T23:59:59"))    #subtract year behind 
    normalize = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))   #leave as 1994 for normalization
    Date_mean = np.nanmean(Date_range) - year + normalize
    Date_std_val = np.std(Date_range)

    O3_avg_1998.append(O3_avg_val)
    O3_std_1998.append(O3_std_val)
    Date_avg_1998.append(Date_mean)
    Date_std_1998.append(Date_std_val)

dateavg_1998 = np.asarray(Date_avg_1998)
o3avg_1998 = np.asarray(O3_avg_1998)
o3std_1998 = np.asarray(O3_std_1998)

#Next Year repeated
Date_avg_1999 = []
Date_std_1999 = []
O3_avg_1999 = []
O3_std_1999 = []

min_date_1999 = np.datetime64("1999-01-01T00:00:01")
max_date_1999 = np.datetime64("1999-12-31T23:59:59")

## iterate in this way, avoid error
for ii in np.arange( min_date_1999 , max_date_1999, dtype='datetime64[M]'):
    O3_range = O3_asarray[(mdates.date2num(Date_asarray)< mdates.date2num(ii+1)) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    O3_avg_val = np.nanmean(O3_range) 
    O3_std_val = np.std(O3_range)

    Date_range = mdates.date2num(Date_asarray)[(mdates.date2num(Date_asarray) < mdates.date2num(ii+1) ) & (mdates.date2num(Date_asarray) > mdates.date2num(ii))]
    year = mdates.date2num(np.datetime64("1998-12-31T23:59:59"))    #subtract year behind 
    normalize = mdates.date2num(np.datetime64("1994-12-31T23:59:59"))   #leave as 1994 for normalization
    Date_mean = np.nanmean(Date_range) - year + normalize
    Date_std_val = np.std(Date_range)

    O3_avg_1999.append(O3_avg_val)
    O3_std_1999.append(O3_std_val)
    Date_avg_1999.append(Date_mean)
    Date_std_1999.append(Date_std_val)

dateavg_1999 = np.asarray(Date_avg_1999)
o3avg_1999 = np.asarray(O3_avg_1999)
o3std_1999 = np.asarray(O3_std_1999)

#define colors for each year
c_1995= "blue"
c_1996= "red"
c_1997= "green"
c_1998= "purple"
c_1999= "orange"

#change plot size
fig, ax=pyplot.subplots(1, 1, figsize=(15, 10))

#plots for every year
pyplot.scatter(mdates.num2date(dateavg_1995[~np.isnan(dateavg_1995)]), o3avg_1995[~np.isnan(dateavg_1995)], color = c_1995 )
#plot of average O3 measurmeant per month vs Date.                                                           yerr = o3std_1995[~np.isnan(dateavg_1995)]
pyplot.errorbar(mdates.num2date(dateavg_1995[~np.isnan(dateavg_1995)]), o3avg_1995[~np.isnan(dateavg_1995)], yerr = None , xerr = None , color = c_1995 , ecolor = c_1995 , elinewidth = 3 , capsize = 3  )


pyplot.scatter(mdates.num2date(dateavg_1996[~np.isnan(dateavg_1996)]), o3avg_1996[~np.isnan(dateavg_1996)], color = c_1996 )
pyplot.errorbar(mdates.num2date(dateavg_1996[~np.isnan(dateavg_1996)]), o3avg_1996[~np.isnan(dateavg_1996)], yerr = None , xerr = None , color = c_1996 , ecolor = c_1996 , elinewidth = 3 , capsize = 3  )


pyplot.scatter(mdates.num2date(dateavg_1997[~np.isnan(dateavg_1997)]), o3avg_1997[~np.isnan(dateavg_1997)], color = c_1997 )
pyplot.errorbar(mdates.num2date(dateavg_1997[~np.isnan(dateavg_1997)]), o3avg_1997[~np.isnan(dateavg_1997)], yerr = None , xerr = None , color = c_1997 , ecolor = c_1997 , elinewidth = 3 , capsize = 3  )


pyplot.scatter(mdates.num2date(dateavg_1998[~np.isnan(dateavg_1998)]), o3avg_1998[~np.isnan(dateavg_1998)], color = c_1998 )
pyplot.errorbar(mdates.num2date(dateavg_1998[~np.isnan(dateavg_1998)]), o3avg_1998[~np.isnan(dateavg_1998)], yerr = None , xerr = None , color = c_1998 , ecolor = c_1998 , elinewidth = 3 , capsize = 3  )


pyplot.scatter(mdates.num2date(dateavg_1999[~np.isnan(dateavg_1999)]), o3avg_1999[~np.isnan(dateavg_1999)], color = c_1999 )
pyplot.errorbar(mdates.num2date(dateavg_1999[~np.isnan(dateavg_1999)]), o3avg_1999[~np.isnan(dateavg_1999)], yerr = None , xerr = None , color = c_1999 , ecolor = c_1999 , elinewidth = 3 , capsize = 3  )


#changes the position of the label
position = mdates.date2num(np.datetime64(str("1995-02-21T23:59:59")))
label = mdates.num2date(position[~np.isnan(position)])
Height = 57

#labels for the graphs
pyplot.title("Date vs Average O3 value"  + "\n" + "Altitude between: " + str(alt_min) + "-" + str(alt_max), fontsize=35 )
pyplot.xlabel("Month" , fontsize=35)
pyplot.ylabel("O3 in ppb" , fontsize=35)
pyplot.text(label, Height, "1995-" + c_1995 + "\n" + "1996-" + c_1996 + "\n" + "1997-" + c_1997 + "\n" + "1998-" + c_1998 + "\n" + "1999-" + c_1999 , fontsize=30)

# Minor ticks every month.
fmt_month = mdates.MonthLocator()
ax.xaxis.set_major_locator(fmt_month)
# '%b' to get the names of the month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

# fontsize for month labels
ax.tick_params(labelsize=30, which='both')

#Sets the Y axis size
ax.set_ylim(20, 77)
pyplot.tight_layout()
pyplot.show()