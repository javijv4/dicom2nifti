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
import nibabel as nib

main_fldr = '/home/jilberto/Desktop/Dicom/DSP-10/6531/'
output_fldr = '/home/jilberto/Desktop/Dicom/DSP-10/6531/'

to_convert = {
            'SA': '6536',
            'LA_2CH': '6535',
            'LA_3CH': '6537',
            'LA_4CH': '6534',
            # 'SA_LGE': '67017',
            # 'LA_4CH': '4985',
            # 'LA_3CH_LGE': '66621',
            # 'LA_2CH_LGE': '67019',
            }


images = []
img_timestep = {}
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
    slice_location = []
    instance_numbers = []
    for scan in dcm_files:
        img = pdcm.dcmread(scan)
        trigger_times.append(float(img.TriggerTime))
        slice_location.append(np.round(float(img.SliceLocation),5))
        instance_numbers.append(int(img.InstanceNumber))
    trigger_times = np.array(trigger_times)

    # Need to calculate the slice duration
    order = np.argsort(instance_numbers)
    trigger_times = trigger_times[order]

    diff_trigger_times = np.abs(np.diff(trigger_times))
    med_trigger_time = np.median(diff_trigger_times)
    diff_trigger_times = diff_trigger_times[(diff_trigger_times < (med_trigger_time + 10)) & (diff_trigger_times > (med_trigger_time - 10))]  # Remove outliers
    img_timestep[scan_name] = np.abs(np.mean(diff_trigger_times))

    for scan in dcm_files:
        name = os.path.basename(scan)
        img = pdcm.dcmread(scan)
        img.save_as(f'{tmp_fldr}/{name}')

    # Convert to nii
    # print(scan_name)
    with open('dcm2niix.log', 'w') as f:
        p = Popen(['dcm2niix', '-o', output_fldr, '-f', scan_name, '-z', 'y', '-m', 'y', tmp_fldr])
        p.wait()

    # Clean
    shutil.rmtree(tmp_fldr)

    # Find .json files and remove
    json_files = glob.glob(output_fldr + '/*.json', recursive=True)
    for json_file in json_files:
        os.remove(json_file)

    print('Done!')


# Fix slice duration in the nifti files
for scan_name, scan_fldr in to_convert.items():
    files = glob.glob(f'{output_fldr}/{scan_name}*.nii.gz')
    if len(files) != 1:
        print(f'Something went wrong with {scan_name}. Expected 1 file, found {len(files)}.')
        continue
    img = nib.load(files[0])
    header = img.header
    zooms = header.get_zooms()
    new_zooms = (zooms[0], zooms[1], zooms[2], img_timestep[scan_name])
    header.set_zooms(new_zooms)
    header['slice_duration'] = img_timestep[scan_name]
    new_img = nib.Nifti1Image(img.get_fdata(), img.affine, header=header)
    nib.save(new_img, f'{output_fldr}/{scan_name}.nii.gz')
    
