source ~/venvs/mturk/bin/activate

ROOT=/data2/chatbot_eval_issues/results/AMT_NCM_Test_NCM_Cakechat

cd ~/Chatbot_evaluation/amt_eval/
python3.6 launch_2choice.py \
-n 10 \
-t "${ROOT}/neural_conv_model_eval_responses.txt" "${ROOT}/neural_conv_model_cakechat_responses.txt" \
-s "${ROOT}/neural_conv_model_eval_source.txt" \
-m 2 \
