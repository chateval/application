'''Launches a HIT on Amazon Mechanic Turk for rank-based evaluation of chatbot models'''
import boto3
import argparse
import os
import random
import codecs
import html

from .utils import *
from .html_gen import *

def create_HIT(examples, mturk):
  if len(examples) == 0:
    return 0
  num_target_candidates =  len(examples[0].target_lines)

  # For each of the provided examples, generate the html that allows
  # Turker to specify ranking. Also count the total number of reuqired radio buttons.
  tables_html = ''
  num_required = 0
  for idx in range(len(examples)):
    html, num_radio_buttons = generate_2choice_html(examples[idx])
    tables_html += html
    num_required += num_radio_buttons

  instructions = generate_2choice_instructions()

  # Generate the full HTML for the hit. The tables html gets inserts in the right place.
  question_html_value = generate_HIT_html(num_required, tables_html, instructions)

  with codecs.open('task.html', 'w', encoding='utf-8') as fout:
    fout.write(question_html_value)

  question_html_value = question_html_value.encode('ascii', 'xmlcharrefreplace').decode()

  try:
    # These parameters define the HIT that will be created
    # question is what we defined above
    # max_assignments is the # of unique Workers you're requesting
    # title, description, and keywords help Workers find your HIT
    # duration is the # of seconds Workers have to complete your HIT
    # reward is what Workers will be paid when you approve their work
    # Check out the documentation on CreateHIT for more details
    response = mturk.create_hit(
            Question=question_html_value,
            MaxAssignments=1,
            Title="Evaluate a chatbot system.",
            Description="Rank the responses of a chatbot",
            Keywords="question, answer, chatbot, research, dialog, rank",
            AssignmentDurationInSeconds=180,
            LifetimeInSeconds=86400,
            Reward="0.02")
            # UniqueRequestToken=hit_id)
  except Exception as e:
    print(e)
    #import pdb; pdb.set_trace()
    print('Problem creating HIT')
    
    exit(1)

  # The response included several fields that will be helpful later
  hit_type_id = response['HIT']['HITGroupId']
  hit_id = response['HIT']['HITId']
  print("Your HIT has been created. You can see it at: "),
  print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
  print("Your HIT ID is: {}".format(hit_id))

  return hit_id
