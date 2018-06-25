#!/bin/bash

source ~/venvs/mturk/bin/activate

ROOT=/data2/chatbot_eval_issues/results//AMT_NCM_Test_NCM_Cakechat

if [ -e "${ROOT}/amt_hit_responses.pkl" ]
then
  echo "Accessing saved responses"
else
  echo 'Retrieving responses from AMT'
  python3.6 retrieve_responses.py \
  -d "${ROOT}/hits.txt" 
fi

python3.6 analyze_2choice_responses.py \
--target_list="${ROOT}/order.txt" \
--source_file="${ROOT}/neural_conv_model_eval_source.txt" \
--responses_path="${ROOT}/amt_hit_responses.pkl" \
