#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/03/11 15:04:59

@author: Javiera Jilberto Vallejos 
'''

import os
import nibabel as nib
import numpy as np

img_path = '/home/jilberto/University of Michigan Dropbox/Javiera Jilberto Vallejos/Projects/Desmoplakin/Models/DSPPatients2/DSP-7/Images/la_4ch_seg_mod.nii.gz'
affine_path = '/home/jilberto/University of Michigan Dropbox/Javiera Jilberto Vallejos/Projects/Desmoplakin/Models/DSPPatients2/DSP-7/Images/la_4ch_seg.nii.gz'

img = nib.load(img_path)
affine_img = nib.load(affine_path)
header = affine_img.header
affine = affine_img.affine

data = (np.round(img.get_fdata())).astype(int)
new_img = nib.Nifti1Image(data, affine, header=header)

fldr = os.path.dirname(img_path)
file = os.path.basename(img_path)

nib.save(new_img, f'{fldr}/{file}')