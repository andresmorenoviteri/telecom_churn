import pandas as pd

class DataCatalog: 
    """ define a class tat wraps access to all datasets described in catalog.yaml"""

    def __init__(self, catalog_config: dict): # constructor, runs when you create a DataCatalog object
        self._catalog = catalog_config # store the loaded catalog dict (from load_Catalog()) as an internal attribute

    def load(self, name: str): # function to load a dataset by its name
        entry = self._catalog[name] # look up that dataset's config entry (a dict with filepath/type) from the catalog
        dtype = entry["type"] # extract the data type, e.g. "pandas.CSVDataSet"

        if dtype == "MemoryDataSet":
            return entry["value"]

        filepath = entry["filepath"] # extract the path file where the data lives, e.g. "data/01_raw/Telecom_customer_churn.csv"

        if dtype == "pandas.CSVDataSet":
            return pd.read_csv(filepath)
        elif dtype == "pandas.ParquetDataSet":
            return pd.read_parquet(filepath)
        else:
            raise ValueError(f"Unsupported data type: {dtype}")

    def save(self, name: str, data):
        entry = self._catalog[name]
        dtype = entry["type"]

        if dtype == "MemoryDataSet":
            entry["value"] = data
            return
        
        filepath = entry["filepath"]

        if dtype == "pandas.CSVDataSet":
            data.to_csv(filepath, index=False)
        elif dtype == "pandas.ParquetDataSet":
            data.to_parquet(filepath)
        else:
            raise ValueError(f"Unsupported data type: {dtype}")

        