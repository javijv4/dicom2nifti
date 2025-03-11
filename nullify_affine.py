#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
Created on 2025/03/11 15:04:59

@author: Javiera Jilberto Vallejos 
'''

import os
import nibabel as nib
import numpy as np

path = '/home/jilberto/University of Michigan Dropbox/Javiera Jilberto Vallejos/Projects/Desmoplakin/Models/DSPPatients2/nifti/DSP-6/SA_LGE.nii.gz'
img = nib.load(path)

new_img = nib.Nifti1Image(img.get_fdata(), np.eye(4))

fldr = os.path.dirname(path)
file = os.path.basename(path)
new_file = file.replace('.nii.gz', '_itk.nii.gz')

nib.save(new_img, f'{fldr}/{new_file}')