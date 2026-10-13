from src.telecom.pipeline import Node, Pipeline # import the framework classes
from .nodes import clean_data # import # import the actual node function(s) for this pipeline

def create_pipeline() -> Pipeline: # factory function, called by the registry
    return Pipeline([
        Node(
            func=clean_data,
            input="telecom_data",
            outputs="processed_data",
            name="processed_Data_node"
        ),
        ])