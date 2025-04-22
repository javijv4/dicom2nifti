#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/04/22 12:26:57

@author: Javiera Jilberto Vallejos 
'''

import os
import pydicom as pdcm
from subprocess import Popen
import glob

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


images = []
for scan_name, scan_fldr in to_convert.items():
    tmp_fldr = f'{output_fldr}/{scan_fldr}_d/'
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

    for scan in dcm_files:
        fname = os.path.basename(scan)

        with open('dcmdjpeg.log', 'w') as f:
            p = Popen(['dcmdjpeg', scan, f'{tmp_fldr}/{fname}'], stdout=f, stderr=f)
            p.wait()