from .pedestrian_eval import validate
def pedestrian_evaluation(dataset, predictions, output_folder, **_): validate(dataset, predictions, output_folder)