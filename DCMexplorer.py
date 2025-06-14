#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:08:25 2020

@author: javijv4
"""

import pydicom as pdcm
import os

path = '/home/jilberto/Desktop/Dicom/DSP-10/6531/'
lista = os.listdir(path)

new_list = []
for l in lista:
   try:
       int(l)
   except:
       continue
   new_list.append(l)
# lista = list(map(int, new_list))
lista.sort()

SA_scan = None
for scan in lista:
    folder = path + str(scan) + '/'
    file = os.listdir(folder)[0]
    try:
        img = pdcm.dcmread(folder + file, force=True)
        print(scan, img.SeriesDescription)
    except:
        continue
