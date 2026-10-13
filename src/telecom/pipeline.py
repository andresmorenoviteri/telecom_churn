class Node: 
    """represents a single unit of work: a function plus its declared inpus/outputs"""
    def __init__(self, func, inputs, outputs, name):
        # func: the actual python function to run (e.g. a cleaning or training function)
        self.func = func

        # inputs: a list of dataset names (strings) this node needs, matching catalog.yaml entries
        self.inputs = inputs if isinstance(inputs, list) else [inputs]

        # outputs: list of dataset names this node produces, also matching catalog.yaml entries
        self.outputs = outputs if isinstance(outputs, list) else [outputs]

        # name: human-readable identifier
        self.name = name

    def run(self, catalog): # executes this node using data pulled from the given DataCatalog
        # load all required inputs from the catalog, by name, into a list of actual data objects
        input_data = [catalog.load(name) for name in self.inputs]

        # call the wrapped function with those inputs unpacked as positional arguments
        result = self.func(*input_data)

        # if the function returns multiple outputs, wrap single result in a list for uniform handling
        if len(self.outputs) == 1:
            result = [result]

        # save each returned value back into the catalog under its corresponding output name
        for name, data in zip(self.outputs, result):
            catalog.save(name, data)

        # return the result too, useful for debugging/testing without touching the catalog
        return result

    def __repr__(self): # defines how this object prints, e.g. in a list or during debugging
        return f"Node(name={self.name}, inputs={self.inputs}, outputs={self.outputs})"



class Pipeline:
    """represents a sequence of nodes and figures out valid execution order based on their declared inputs/outputs"""
    def __init__(self, nodes: list):
        self.nodes = nodes # stores the list of Node objects passed in

    def run(self, catalog): # executes all nodes in dependency
        remaining = list(self.nodes) # nodes not yet executed
        done_outputs = set() # names of datasets already produced

        # collect every output name produced by some node in this pipeline
        all_pipeline_outputs = set()
        for node in self.nodes:
            all_pipeline_outputs.update(node.outputs)

        while remaining: # keep looping until every node has run
            progressed = False # tracks if we executed anything this pass

            for node in list(remaining): # try each not-yet-run node
                # a node is ready if all its inputs are already available
                # (either produced by a previous node, or pre-existing in the catalog)
                ready = all(
                    inp in done_outputs # already prodcued by an earlier node this run
                    or inp not in all_pipeline_outputs # or it's a true external input, not something this pipeline produces
                    for inp in node.inputs
                )
                if ready:
                    node.run(catalog) # execute the node (load input, saves outputs)
                    done_outputs.update(node.outputs) # mark its outputs as available
                    remaining.remove(node) # remove from pending list
                    progressed = True

            if not progressed: # no node could run this pass = circular or missing dependency
                raise RuntimeError(
                    f"Cannot resolve pipeline order for: {remaining}"
                )
            
