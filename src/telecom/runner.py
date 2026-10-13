from src.telecom.config import load_catalog
from src.telecom.catalog import DataCatalog

def run_pipeline(pipeline):
    catalog_config = load_catalog()
    data_catalog = DataCatalog(catalog_config)
    pipeline.run(data_catalog)
    return data_catalog