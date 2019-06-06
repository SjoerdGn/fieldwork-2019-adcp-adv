# (c) 2019
# Sanne de Smet
# Sjoerd Gnodde

# Hydrological Fieldwork 2019
# Group 4

# Code reading data from the StreamPro device

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as spio
import getpass
import os
import csv

def streampro_q_func():
    #Vbeam = 6.32 # distance of vertical sample

    tierap = "3"  # The tierap being looked at right now

    device = "StreamPro"
    plot_vert_prof = False # Plot vertical profile
    save_vert_prof = False # Save vertical profile to file

    plot_cross_sec = False

    save_mid_depths = False

    save_extra_width = False

    save_discharge_figures = True

    folder_file_save = "../output_images/{}.png"
    folder_csv_save = "../data/{}.csv"
    depths_adcp_for_adv = folder_csv_save.format('depths_adcp_for_adv_{}'.format(device))
    diff_travel_streampro = folder_csv_save.format('diff_travel_{}'.format(device))
    ##################################

    # Number of days in total
    numdays = 6

    # Name of the computer
    myhost = getpass.getuser()

    # Base folder
    datafolder = 'C:/Users/username/Documents/Fieldwork/fieldwork-2019-adcp-adv/data/'.replace('username', myhost)# basefolder
    basefolder = datafolder+device

    # Subfolders
    daynames = [i[3:] for i in os.listdir(basefolder)]

    # Four different qs per time period
    allqs = [np.zeros(numdays) for i in range(4)]

    # Every q ever, so no means
    every_q = {}
    every_q['Right_q'] = {}
    every_q['Left_q'] = {}
    every_q['Top_q'] = {}
    every_q['Middle_q'] = {}

    # Test tierap
    try: 
        tierap = int(tierap)
        print("Transect {} used".format(tierap))
    except:
        print("Transect {} used".format(tierap))


    # Open Excel with ADV results
    advexcel = datafolder+'ADVmeasurements.xlsx'


    # Count the number of days
    day = 0


    # loop over all roots
    for root, dirs, files in os.walk(basefolder, topdown=True):

        # Don't look in the basefolder
        if root == basefolder:
            continue

        # Per time period, save the number of depth cells
        tot_xs = {}
        len_xs = 1000

        # which folder are we doing right now?
        print(daynames[day])

        # the files that are needed are the totaldata files and one of the distance_rl for every day part.
        goodfiles =[file for file in files if file[-13:] == 'total_ASC.TXT']


        # Remember the number of the file
        filenum = 0

            # Total Qs to be saved
        tot_rightq = np.zeros(len(goodfiles))
        tot_leftq = np.zeros_like(tot_rightq)
        tot_topq = np.zeros_like(tot_rightq)
        tot_middleq = np.zeros_like(tot_rightq)

        # Read the Excel of the ADV measurements
        adv = pd.read_excel(advexcel, sheet_name=daynames[day])
        meas_locs = adv.iloc[2, 1:].dropna()


        # Set Vbeam (location that is used now)
        Vbeam = adv[tierap][2]

        # Save depths in middle
        tot_middepths = np.zeros((len(meas_locs), len(goodfiles)))


        # Loop over the correct files in the folder
        for file in goodfiles:
            # Load direction from file in folder
            data = pd.read_csv(root+'/'+file, delimiter = ';')
            direction = int(np.loadtxt(root+'/direction.txt', delimiter = ',')[filenum])
            print(file, direction)



            # Water velocity in the direction of the river
            Velocity = data['northV'] #only the velocity to the north is in direction of the river
            Velocity = [Velocity.iloc[i].split(',') for i in range(len(Velocity))]
            for i in range(len(Velocity)):
                Velocity[i] = [float(Velocity[i][j]) for j in range(len(Velocity[i])) if float(Velocity[i][j])>-50]

                #velocity is negative for all days except Monday so need to change it to positive values
                if daynames[day][0] != 'M':
                    Velocity[i] = [float(Velocity[i][j])*-1 for j in range(len(Velocity[i]))] 



            #corresponding depth of the bin with the velocity
            Depth_bin = data['depthbin'].iloc[0].split(',')
            Depth_bin = [float(Depth_bin[i])*-1 for i in range(len(Depth_bin))]

            # the depth of bin is wrong for wednesday afternoon (wrong blanking zone) so changed back
            if daynames[day][0:11]  == 'Wednesday a':
                Depth_bin = [float(Depth_bin[i]) + 0.54 for i in range(len(Depth_bin))]

             #Total_width = data['totalwidth'].iloc[-1] #these values are not correct always the same

            #Bin_size = data['binsize'].iloc[0] Not needed

            # all the separate Qs
            TopQ = data['topQ'].iloc[-1]

            MiddleQ = data['middleQ'].iloc[-1]

            LeftQ = data['LeftQ'].iloc[-1]

            RightQ = data['RightQ'].iloc[-1]


             # Save total Qs such that average can be taken
            tot_rightq[filenum] = RightQ
            tot_leftq[filenum] = LeftQ
            tot_topq[filenum] = TopQ
            tot_middleq[filenum] = MiddleQ

            Distance = data['Distancetravelled']
            Distance = [Distance.iloc[i] for i in range(len(Distance))]

            if direction==1:  # flip if reverse
                Distance = np.max(Distance)-Distance


            # DEBUG NANS:
            #print([len(Velocity[i]) for i in range(len(Velocity))])
            #print(Middepths)
            #print(Distance)


            filenum +=1




        # For the new data: do not take the mean, but rather save them all
        every_q['Right_q'][daynames[day]] = tot_rightq
        every_q['Left_q'][daynames[day]] = tot_leftq
        every_q['Top_q'][daynames[day]] = tot_topq
        every_q['Middle_q'][daynames[day]] = tot_middleq



        print()
        day +=1

    return every_q