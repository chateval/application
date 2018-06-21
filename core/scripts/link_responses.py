from .auto_models import Model, EvaluationDataset, EvaluationDatasetText, ModelResponse

def load_responses(response_file, dataset, model):
    with open(response_file) as f:
        data = f.read()
        responses = data.split('\n')
        prompts = EvaluationDatasetText.objects.all().filter(evaluationdataset=dataset)
        
        for i in range(len(responses)):
            model_response = ModelResponse(evaluationdataset=dataset, prompt=prompts[i], model=model, response_text=responses[i])
            model_response.save()