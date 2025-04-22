#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2024/08/06 09:23:42

@author: Javiera Jilberto Vallejos
'''

import os
import glob
import numpy as np
from subprocess import Popen
import shutil
import pydicom as pdcm

main_fldr = '/home/jilberto/Desktop/Dicom/DSP-3/5011191/'
output_fldr = '/home/jilberto/Desktop/Dicom/DSP-3/5011191/'

to_convert = {
            'SA': '5011200',
            # 'LA_2CH': '5011198',
            # 'LA_3CH': '5011201',
            # 'LA_4CH': '5011199',
            # 'LA_2CHr': '5011202',
            # 'SA_LGE': '5011206',
            # 'LA_4CH_LGE': '5011208',
            # 'LA_3CH_LGE': '5011212',
            }


# main_fldr = '/home/jilberto/Desktop/Dicom/DSP-1/4981/'
# output_fldr = '/home/jilberto/Desktop/Dicom/DSP-1/4981/'

# to_convert = {
#             'SA': '4986',
#             # 'LA_2CH': '5011198',
#             # 'LA_3CH': '5011201',
#             # 'LA_4CH': '5011199',
#             # 'LA_2CHr': '5011202',
#             # 'SA_LGE': '5011206',
#             # 'LA_4CH_LGE': '5011208',
#             # 'LA_3CH_LGE': '5011212',
#             }

images = []
for scan_name, scan_fldr in to_convert.items():
    tmp_fldr = 'tmp/'
    if not os.path.exists(tmp_fldr):
        os.makedirs(tmp_fldr)
        
    all_files = glob.glob(f'{main_fldr}/{scan_fldr}/*', recursive=True)

    # Read only dcm files
    dcm_files = []
    for file in all_files:
        try:
            img = pdcm.dcmread(file)
            dcm_files.append(file)
        except:
            pass

    dcm_files.sort()

    # Second check: Fixing study times
    study_times = []
    for scan in dcm_files:
        img = pdcm.dcmread(scan)
        study_times.append(int(img.StudyTime))

    times, counts = np.unique(study_times, return_counts=True)
    if len(times) > 1:
        fix_time = times[np.argmax(counts)]
        time = times[np.argmin(counts)]
        ind_scans = np.where(study_times == time)[0]
        print('Scan times of {} scans are different. Fixing it.'.format(len(ind_scans)))

        for scan in dcm_files:
            img = pdcm.dcmread(scan)
            img.StudyTime = str(fix_time)
            img.save_as(scan)

    # Third check: Make trigger time to be the same
    trigger_times = []
    for scan in dcm_files:
        img = pdcm.dcmread(scan)
        trigger_times.append(float(img.TriggerTime))

    times, counts = np.unique(trigger_times, return_counts=True)
    if len(times) > 1:
        fix_time = times[np.argmax(counts)]
        time = times[np.argmin(counts)]
        ind_scans = np.where(trigger_times == time)[0]
        print('Trigger times of {} scans are different. Fixing it.'.format(len(ind_scans)))

        for scan in dcm_files:
            name = os.path.basename(scan)
            img = pdcm.dcmread(scan)
            img.TriggerTime = str(fix_time)
            img.save_as(f'{tmp_fldr}/{name}')
    else:
        for scan in dcm_files:
            name = os.path.basename(scan)
            img = pdcm.dcmread(scan)
            img.save_as(f'{tmp_fldr}/{name}')

    for scan in dcm_files:
        name = os.path.basename(scan)
        img = pdcm.dcmread(scan)
        # img.save_as(f'{tmp_fldr}/{name}')
        images.append(img)
        print(os.path.basename(scan), img.AcquisitionNumber, img.SeriesNumber, img.InstanceNumber, img.RepetitionTime, img.TriggerTime)

    # Convert to nii
    # print(scan_name)
    with open('dcm2niix.log', 'w') as f:
        p = Popen(['dcm2niix', '-o', output_fldr, '-f', scan_name, '-z', 'y', '-v', '2', tmp_fldr])
        p.wait()

    # Clean
    shutil.rmtree(tmp_fldr)

    # Find .json files and remove
    json_files = glob.glob(output_fldr + '/*.json', recursive=True)
    for json_file in json_files:
        os.remove(json_file)

    print('Done!')