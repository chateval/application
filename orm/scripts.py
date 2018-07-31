import requests
from orm.models import Baseline, ModelResponse, EvaluationDatasetText

def get_baseline_messages(evalset_id, get_all=True):
    messages = list()
    baseline = Baseline.objects.filter(evaluationdataset=evalset_id)[0].model
    if get_all:
        responses = ModelResponse.objects.filter(model=baseline, evaluationdataset=evalset_id)
    else:
        responses = ModelResponse.objects.filter(model=baseline, evaluationdataset=evalset_id)[:50]
    for response in responses:
        messages.append(dict({'prompt': response.prompt.prompt_text, 'response': response.response_text}))
    return messages

def get_messages(model_id, evalset_id, get_all=True):
    messages = list()
    if get_all:
        responses = ModelResponse.objects.filter(model=model_id, evaluationdataset=evalset_id)
    else:
        responses = ModelResponse.objects.filter(model=model_id, evaluationdataset=evalset_id)[:50]
    for response in responses:
        messages.append(dict({'prompt': response.prompt.prompt_text, 'response': response.response_text}))
    return messages

def upload_responses(responses, dataset, model, submission):
    prompts = EvaluationDatasetText.objects.filter(evaluationdataset=dataset)
    model_responses = list()
    print(len(responses))
    print(len(prompts))
    for i in range(min(len(responses), len(prompts))):
        model_response = ModelResponse(model_submission=submission, evaluationdataset=dataset, 
            prompt=prompts[i], model=model, response_text=responses[i])
        model_responses.append(model_response)
    ModelResponse.objects.bulk_create(model_responses)