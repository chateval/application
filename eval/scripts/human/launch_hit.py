import boto3
import argparse
import os
import random
import codecs
import html

from .utils import *
from .html_gen import *

from .generate_hit import * 

from orm.models import ModelResponse, EvaluationDatasetText

def launch_hits(dataset, model1, model2):
  n_examples_per_hit = 10
  max_assignments = 1
  sandbox = True

  # Create your connection to MTurk
  mturk = create_mturk_client(sandbox)

  hits_out_path = 'eval/scripts/human/hits/' + str(model1.model_id) + '_' + str(model2.model_id) + '_' + str(dataset.evalset_id) + '_hits.txt'
  order_out_path = os.path.join(os.path.dirname(model1.name + model2.name), 'order.txt')

  # If you want to launch with more than 2 targets being compared, use the
  # launch_multichoice.py script.
  # assert len(args.target_files) == 2
  '''
  with open(order_out_path, 'w') as fout:
    fout.write('\n'.join(args.target_files))
  '''

  '''
  TODO: Write to order_out_path order of the models
  '''

  # Query to get the prompts of dataset being compared
  prompts = EvaluationDatasetText.objects.filter(evaluationdataset=dataset)
  model1_responses = ModelResponse.objects.filter(evaluationdataset=dataset, model=model1)
  model2_responses = ModelResponse.objects.filter(evaluationdataset=dataset, model=model2)
  examples = []

  for idx in range(len(prompts)):
    example = Example(prompts[idx].prompt_text, "ex-%03d" % (idx))
    example.add_target_line(model1_responses[idx].response_text)
    example.add_target_line(model2_responses[idx].response_text)
    examples.append(example)
    
  print('Read in %d examples, each with %d possible targets.' % (len(examples), len(examples[0].target_lines)))
  #assert args.n_examples_per_hit <= len(examples)

  random.shuffle(examples)

  # TODO: For each set of k examples, create d HITs, where k is the number of
  # examples shown in a hit, and d is the number of random permutations of those
  # k HITs that we want to show.
  count = 0
  hit_ids = []

  while count < len(examples):
    print('Creating HIT for examples %s through %s' % (count, count+n_examples_per_hit-1))
    for idx in range(max_assignments):
      hit_id = create_HIT(examples[count:count+n_examples_per_hit], mturk) # second argument - hit_id="cb_eval_%d_%d" % (count, idx)
      if hit_id == 0:
        print('ERROR: Failed to create hit')
      else:
        hit_ids.append(hit_id)
      count += n_examples_per_hit

  # Write all the hit_ids to a file to make it easy to extact the results
  with open(hits_out_path, 'a') as f_out:
    for hit_id in hit_ids:
      f_out.write('%s\n' % (hit_id))
  
  # TODO: Upload hits file to S3 bucket