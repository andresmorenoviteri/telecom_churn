from src.telecom.pipelines.data_processing.pipeline import create_pipeline as dp_pipeline # import each sub-pipeline's factory function
from src.telecom.pipelines.data_science.pipeline import create_pipeline as ds_pipeline
from src.telecom.pipelines.model_training.pipeline import create_pipeline as mt_pipeline

def register_pipelines() -> dict: # returns a name -> Pipeline mapping,
    return {
        "data_processing": dp_pipeline(), # build and register the data_rpcessing pipeline
        "data_science": ds_pipeline(), # build and register the data_science pipeline
        "model_training": mt_pipeline(), # build and register the model_training pipeline
    }