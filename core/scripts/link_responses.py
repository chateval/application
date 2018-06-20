from .auto_models import Model, EvaluationDataset, EvaluationDatasetText, ModelResponse

def load_responses(path, dataset):
    with open(path) as f:
        model = Model.objects.all()
        data = f.read()
        responses = data.split('\n')
        evaluation_dataset = EvaluationDataset.objects.all().filter(name=dataset)
        prompts = EvaluationDatasetText.objects.all().filter(evaluationdataset=evaluation_dataset[0])
        
        for i in range(len(responses)):
            model_response = ModelResponse(evaluationdataset=evaluation_dataset[0], prompt=prompts[i], model=model[0], response_text=responses[i])
            model_response.save()
        
        