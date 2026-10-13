import argparse # standard library for parsing command-line arguments
from src.telecom.pipeline_registry import register_pipelines #  get the name -> Pipeline mapping
from src.telecom.runner import run_pipeline # the function that actually executes a pipeline

def main():
    parser = argparse.ArgumentParser() # set up the CLI parser
    parser.add_argument("--pipeline", required=True) # require a --pipeline flag. e.g. --pipeline data_processing
    args = parser.parse_args() # read what the user typed

    pipelines = register_pipelines() # get all registerd pipelines
    if args.pipeline not in pipelines: # validate the name they gave
        raise ValueError(f"Unknown pipeline: {args.pipeline}")

    run_pipeline(pipelines[args.pipeline]) # run the chisen pipeline end-to-end

if __name__ == "__main__": # only runs when this file is excuted directly (not on import)
    main()
