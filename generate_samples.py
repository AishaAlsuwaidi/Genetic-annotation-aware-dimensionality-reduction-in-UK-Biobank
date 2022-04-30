#!/usr/bin/env python
# coding: utf-8


import argparse
import random

from pymongo import MongoClient
from tqdm import tqdm


parser = argparse.ArgumentParser(
    description='Generates a panel of samples from the UK BioBank data')
parser.add_argument('--output', type=str, default='.',
                    help='output folder path')
parser.add_argument('--icd10-codes', nargs='+', default=None,
                    help='space separated list of ICD10 codes')
parser.add_argument('--icd9-codes', nargs='+', default=None,
                    help='space separated list of ICD9 codes')

args = parser.parse_args()
icd10_codes = args.icd10_codes
icd9_codes = args.icd9_codes

available_samples = set()
with open('/Users/aisha/Desktop/FileGeneration/generateDiseaseFiles/core/available_samples') as f:
    available_samples = set(f.read().splitlines())

print('Connecting to MongoDB...')
with MongoClient(host='10.11.64.36') as client:
    coll = client.ukb_icd.collections

    query = {'$or': []}
    if icd10_codes is not None:
        query['$or'].append({'icd10': {'$in': icd10_codes}})
    if icd9_codes is not None:
        query['$or'].append({'icd9': {'$in': icd9_codes}})

    # Collect all IDs matching the query.
    n = coll.count_documents(query)
    matched_ids = []
    print('Querying for matching samples...')
    for i in tqdm(coll.find(query, {'eid': 1, '_id': 0}), total=n):
        if i['eid'] in available_samples:
            matched_ids.append(i['eid'])

    # Collect all IDs that don't match the query.
    query = {'eid': {'$not': {'$in': matched_ids}}}
    m = coll.count_documents(query)
    negative_ids = []
    print('Querying for non-matching samples...')
    for i in tqdm(coll.find(query, {'eid': 1, '_id': 0}), total=m):
        if i['eid'] in available_samples:
            negative_ids.append(i['eid'])

# Random sampling of control samples.
print('Resampling...')
random.shuffle(negative_ids)
negative_ids = negative_ids[:len(matched_ids*2)]

# Write out.
print('Writing to patient_ids.txt and control_ids.txt')
with open('patient_ids.txt', 'w') as pf:
    for i in matched_ids:
        pf.write(f'{i}_{i}\n')

with open('control_ids.txt', 'w') as cf:
    for i in sorted(negative_ids):
        cf.write(f'{i}_{i}\n')

