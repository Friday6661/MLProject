from typing import Any, Dict, Optional

import numpy as np
import pandas as pd


class FillingMissingValue:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def fill_column_with_mode(self, df: pd.DataFrame, column_name: str):
        mode_value = df[column_name].mean()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(mode_value, inplace=True)

    def fill_column_with_mean(self, df: pd.DataFrame, column_name: str):
        mean_value = df[column_name].mean()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(mean_value, inplace=True)
        return df
    
    def fill_column_with_median(self, df: pd.DataFrame, column_name: str):
        median_value = df[column_name].median()
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna(median_value, inplace=True)

    def fill_column_with_unknown(self, df: pd.DataFrame, column_name: str):
        df[column_name].replace("", np.nan, inplace=True)
        df[column_name].fillna("Unknown", inplace=True)
        return df