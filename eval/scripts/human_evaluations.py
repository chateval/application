import sys, os, json
from analyze_2choice_responses import *

response_files = dict()
response_files['NCM'] = dict()
response_files['DBDC'] = dict()
all_amt_experiments = dict()
all_amt_experiments['NCM'] = []
all_amt_experiments['DBDC'] = []

data = []
for line in open(os.path.abspath(os.path.join('setc_runs.csv'))).readlines():
    evalset,m1,m2,folder = line.strip('\n').split(',')

    target_files = open(os.path.abspath(os.path.join(folder + '/order.txt'))).readlines()
    target_files = [os.path.abspath(os.path.join(x.strip().replace('/data2/chatbot_eval_issues/results/',''))) for x in target_files]
    print('Model 1 is: ' + target_files[0], m1)                                                                                      
    print('Model 2 is: ' + target_files[1], m2)                                                                                      
    response_files[evalset][m1] = target_files[0]
    response_files[evalset][m2] = target_files[1]
    print(response_files)
    print(open(response_files[evalset][m1]).readlines()[0:5])

    if evalset == 'NCM':
        examples = utils.process_source_and_responses(
            os.path.abspath(os.path.join('Chatbot_evaluation/eval_data/ncm/neural_conv_model_eval_source.txt')), target_files)
        if 'Human' in m1:
            human_responses['NCM'][m1] = [_.strip('\n') for _ in open(response_files[evalset][m1]).readlines()]
        if 'Human' in m2:
            human_responses['NCM'][m2] = [_.strip('\n') for _ in open(response_files[evalset][m2]).readlines()]
    elif evalset == 'DBDC':
        examples = utils.process_source_and_responses(
            os.path.abspath(os.path.join(
            'Chatbot_evaluation/eval_data/dbdc/dbdc_eval_minus_CIC_200rand.txt')), target_files)
        
        
    examples_dict = {}
    for example in examples:
        examples_dict[example.key] = example
        
    worker_results_list = pickle.load(open(folder + '/amt_hit_responses.pkl','rb'))

    utils.process_amt_hit_responses(worker_results_list, examples_dict)


    for (key, ex) in examples_dict.items():
        #print(key, ex)                                                                                                                
        if len(ex.votes) < 3:
            continue
        for worker, vote in zip(ex.workers, ex.votes):
            if 1: # vote != -1:                                                                                                        
                print(worker + '\t' +  m1.replace(' ','_')+'-'+m2.replace(' ','_')+'-'+key + '\t' +  str(vote))
                data.append((worker, str(vote), m1.replace(' ','_')+'-'+m2.replace(' ','_')+'-'+key))



    l = [ex.votes for ex in examples_dict.values()]
    all_votes = [item for sublist in l for item in sublist]
    all_amt_experiments[evalset].append({'model1':m1,  'model2': m2,
                                       'm1win':sum([x == 0 for x in all_votes]),
                                       'm2win':sum([x == 1 for x in all_votes]),
                                       'tie':  sum([x == -1 for x in all_votes])})