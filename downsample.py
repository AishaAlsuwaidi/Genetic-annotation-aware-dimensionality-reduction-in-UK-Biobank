#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from collections import Counter
import argparse
import random
from pymongo import MongoClient
from tqdm import tqdm
import numpy as np
import xml.etree.ElementTree as ETree

coding = {
    'Ethnic background': {
        -1: None,
        -3: None,
        1: 'White',
        1001: 'British',
        1002: 'Irish',
        1003: None,
        2: None,
        2001: None,
        2002: None,
        2003: None,
        2004: None,
        3: None,
        3001: 'Indian',
        3002: 'Pakistani',
        3003: 'Bangladeshi',
        3004: None,
        4: None,
        4001: 'Caribbean',
        4002: 'African',
        4003: None,
        5: 'Chinese',
        6: None,
    },
    'Gender': {
        0: 'Female',
        1: 'Male',
    }
}



parser = argparse.ArgumentParser(
    description='Generates a panel of samples from the UK BioBank data')
parser.add_argument('--disease-name', type=str, default=None,
                    help='disease name')


args = parser.parse_args()
val = args.disease_name

xmldata = ''+val+'_snp_result.xml'
prstree = ETree.parse(xmldata)
root = prstree.getroot()
  
store_items = []
all_items = []
  
for storeno in root: 
    store_Nr = storeno.attrib.get('uid')
    itemsF = storeno.find('SNP_ID').text
  
    store_items = [store_Nr]
    all_items.append(store_items)
  
SNPs = pd.DataFrame(all_items, columns=['uid'])
SNPs['uid'] = 'rs' +SNPs['uid']
SNPs.to_csv(r''+val+'snps.txt', header=None, index=None, sep=' ', mode='a')

EthnicBackground = pd.read_csv('/Users/aisha/Desktop/Final/flashpca_S/ukb45833_ethnicity_gender.tsv', delimiter='\t')
print(val)

aaa = pd.read_csv('all_ids.txt', delimiter='\t', header= None)
aaa[0] = aaa[0].str.split('_', expand=True)
aaa.to_csv(r''+val+'_IDs.txt', header=None, index=None, sep='\t', mode='a')


ID = pd.read_csv(val+'_IDs.txt', header = None)

EthnicBackground.columns = ['ID','Ethnic background', 'Gender']
for feature in coding:
    EthnicBackground[feature] = EthnicBackground[feature].map(coding[feature])
ID = ID.rename({0: 'ID'}, axis=1)
data = ID.copy(deep=True)
data = pd.merge(data, EthnicBackground, on='ID')
data = data.dropna()
data = data.reset_index()

data_sampled = {}
data_len = {}
for i in np.unique(data['Ethnic background']):
    data_sampled[i] = np.where(data['Ethnic background'] == i)[0]
    data_len[i] = len(data_sampled[i])
maxi = max(x for x in data_len.values() if x < 1000)

downsampled = {}
for i in data_sampled:
    if data_len[i] < maxi:
        continue
    print(i)
    downsampled[i] = np.random.choice(data_sampled[i], size=maxi, replace=False)
sampled_id = []
for i in downsampled.keys():
        for y in downsampled[i]:
            sampled_id.append(data.at[y, 'ID'])
df = pd.DataFrame(sampled_id)
df.to_csv(r'./'+val+'_downsampled.txt', header=None, index=None, sep='\t', mode='a')




