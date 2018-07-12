import xmltodict
import argparse
import re
import codecs
import pickle
import os
from .utils import *
import glob

from orm.models import EvaluationDatasetText, EvaluationDataset, HumanEvaluationsABComparison, Model, HumanEvaluations

def retrieve():
  mturk = create_mturk_client(True)
  hit_files = glob.glob('eval/scripts/human/hits/*.txt')
  print(hit_files)
  worker_results_list = []
  for file in hit_files:
    print('Reading HIT ids from: ' + file)
    
    # Extracting the models and dataset that the comparison was made for
    parts_of_file = file
    parts_of_file = parts_of_file[24:]
    parts_of_file = parts_of_file.split('_')
    mturk_run_id = parts_of_file[3]
    human_evaluation = HumanEvaluations.objects.filter(mturk_run_id=mturk_run_id)[0]
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=human_evaluation.evaluationdataset)

    '''
    print(parts_of_file[0])
    print(parts_of_file[1])
    model1 = Model.objects.filter(model_id=parts_of_file[0])[0]
    model2 = Model.objects.filter(model_id=parts_of_file[1])[0]
    dataset = EvaluationDataset.objects.filter(evalset_id=parts_of_file[2])[0]
    '''
    
    
    #import pdb; pdb.set_trace()
    with open(file, 'r') as f_in:
      for hit_id in f_in:
        #print('Processing: ' + hit_id)
        hit_id = hit_id.strip()
        try:
          worker_results = mturk.list_assignments_for_hit(
              HITId=hit_id, AssignmentStatuses=['Submitted'])
        except Error as e:
          print('Could not find results for HIT: ' + hit_id)
          print(e)
          continue
        if worker_results['NumResults'] > 0:
          for assignment in worker_results['Assignments']:
            print(assignment)
            xml_doc = xmltodict.parse(assignment['Answer'])
            print(xml_doc)
            # This code assumes there are multiple fields in HIT layout
            for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
              if type(answer_field) == str:
                continue
              try:
                input_field = answer_field['QuestionIdentifier']
                rank = int(answer_field['FreeText'])
                worker_id = assignment['WorkerId']
                accept_time = assignment['AcceptTime']
              except Exception as e:
                #import pdb; pdb.set_trace()
                print(e)

              parsed = re.search(r'(ex-\d+)-target-(.+)', input_field)
              example_key = parsed.group(1) # prompt id (index from 0)
              target_index_or_tie = parsed.group(2) 
              
              #example = examples_dict[example_key]
              if 'tie' in target_index_or_tie:
                print("tie")
                #example.votes.append(-1)
                target_index = -1
              else:
                target_index = int(target_index_or_tie)
                target_index = 0 if target_index == 1 else 0

              # TODO - Add the HumanEvaluationsABComparison object 
              '''
              prompt_id = example_key
              worker_id = worker_id
              HIT = hit_id
              accept_datetime = accept_time
              value = target_index
              '''
              human_evaluation_abcomparison = HumanEvaluationsABComparison(mturk_run_id=human_evaluation, prompt=prompts[example_key], worker_id = worker_id, hit = hit_id, accept_datetime = accept_time, value = target_index)
              human_evaluation_abcomparison.save()
        print(worker_results)
        print('\n\n\n')
  '''
  out_file_name = os.path.join(os.path.dirname(args.hit_list_path), 'amt_hit_responses.pkl') 
  pickle.dump(worker_results_list, open(out_file_name, "wb"))
  '''