from .auto_models import Metric

def load_dataset(path):
    with open(path) as f:
        data = f.read()
        metrics = data.split('\n')
        print(metrics)
        for metric in metrics:
            met = Metric(name=metric)
            met.save()