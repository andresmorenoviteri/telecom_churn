from src.telecom.pipeline import Node, Pipeline
from src.telecom.runner import run_pipeline

def add_one(x):
    return x + 1

n1 = Node(func=add_one, inputs="some_number", outputs="incremented_number", name="add_function")
n2 = Node(func=add_one, inputs="incremented_number", outputs="incremented_twice", name="add_function_2")

pipeline = Pipeline(nodes=[n2, n1])
data_catalog = run_pipeline(pipeline)

print(f"final value: {data_catalog.load('incremented_twice')}")