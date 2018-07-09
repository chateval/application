import xmltodict
import argparse
import re
import codecs
import pickle
import os
from .utils import *
import glob

def retrieve():
  mturk = create_mturk_client(True)
  hit_files = glob.glob('eval/scripts/human/hits/*.txt')
  print(hit_files)
  worker_results_list = []
  for file in hit_files:
    print('Reading HIT ids from: ' + file)
    #import pdb; pdb.set_trace()
    with open(file, 'r') as f_in:
      for hit_id in f_in:
        print('Processing: ' + hit_id)
        hit_id = hit_id.strip()

        '''
        try:
          worker_results = mturk.list_assignments_for_hit(
              HITId=hit_id, AssignmentStatuses=['Submitted'])
        except Error as e:
          print('Could not find results for HIT: ' + hit_id)
          continue

        worker_results_list.append(worker_results)
        '''




  '''
  out_file_name = os.path.join(os.path.dirname(args.hit_list_path), 'amt_hit_responses.pkl') 
  pickle.dump(worker_results_list, open(out_file_name, "wb"))
  '''