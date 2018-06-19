from .auto_models import EvaluationDataset, EvaluationDatasetText

def load_dataset(path, name, long_name, source, description):
    with open(path) as f:
        data = f.read()
        prompts = data.split('\n')
        print(prompts)
        evaluation_dataset = EvaluationDataset(name=name, long_name=long_name, source=source, description=description)
        evaluation_dataset.save()
        
        for prompt in prompts:
            evaluation_dataset_text = EvaluationDatasetText(evaluationdataset=evaluation_dataset, prompt_text=prompt, num_turns=1)
            evaluation_dataset_text.save()