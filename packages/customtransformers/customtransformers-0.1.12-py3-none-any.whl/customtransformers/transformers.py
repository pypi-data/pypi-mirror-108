import re
import logging
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import MissingIndicator
import numpy as np
import pandas as pd

# pylint: disable=unused-argument
# pylint: disable=missing-function-docstring
# pylint: disable=no-self-use

class MissingIndicatorPandas(BaseEstimator, TransformerMixin):
    """Create binary indicator of missing value for each columns
    """
    def __init__(self):
        self.indicator = MissingIndicator(features="all")
        self.colnames = None
        self.missing_colnames = None

    def fit(self, X, y=None):
        self.colnames = list(X.columns)
        self.missing_colnames = [x + "_missingindicator" for x in self.colnames]
        self.indicator.fit(X)
        return self

    def transform(self, X, y=None):
        input_size = X.shape[0]

        missing_indicator = pd.DataFrame(self.indicator.transform(X))
        res = pd.concat([X.reset_index(drop=True), missing_indicator.reset_index(drop=True)], axis=1)
        res.columns = self.colnames + self.missing_colnames

        assert res.shape[0] == input_size
        return res

class GetFeaturesAtStep(BaseEstimator, TransformerMixin):
    """Get features at a given steps
    """

    def __init__(self):
        self.X_state = None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        self.X_state = X
        return X

class OrderColumns(BaseEstimator, TransformerMixin):
    """Order columns same in fit and transform
    """
    def __init__(self):
        self.col_order = None

    def fit(self, X, y=None):
        self.col_order = list(X.columns)
        return self

    def transform(self, X, y=None):
        return X[self.col_order]


class DropHostNameInFile(BaseEstimator, TransformerMixin):
    """ Drop hostname ("hostname" column name) that are in a given file
    """

    def __init__(self, file_path):
        self.file_path = file_path

        self.hostname = pd.read_csv(self.file_path, index_col=False, header=None).dropna()
        self.hostname = self.hostname.iloc[:, 0].tolist()

        self.hostnamelike = None
        self.hostnamelike = [x for x in self.hostname if "%" in x]
        self.hostnamelike = [x.replace("%", "") for x in self.hostnamelike]
        self.hostnamelike = ".*(" + "|".join(self.hostnamelike) + ").*"

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        nrows_before = X.shape[0]
        if "desthost" in X.columns:
            X = X.loc[X.desthost.map(lambda x: x not in self.hostname)]
            logging.warning(f"Deleted {nrows_before - X.shape[0]} because exact match in black list: {self.file_path}")
            nrows_before = X.shape[0]

            logging.warning(f"{X.desthost.isna().sum()} missing hostname")

            X.desthost = X.desthost.fillna("missing")

            X = X.loc[X.desthost.map(lambda x: not bool(re.match(self.hostnamelike, x))), :]

            logging.warning(f"Deleted {nrows_before - X.shape[0]} because regex match in black list: {self.file_path}")

        return X


class DropConnectMethod():
    """Drop alls rows with connect method
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if "httpmethod" in X.columns:
            nrows_before = X.shape[0]
            X = X.loc[X.httpmethod != "CONNECT", :]
            logging.warning(f"Deleted {nrows_before - X.shape[0]} with CONNECT method ({nrows_before} before, {X.shape[0]} after)")
        return X


class DropTargetIfExist():
    """Drop target columns (if exists)
    """

    def __init__(self, target_col):
        self.target_col = target_col
        self.target = None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        if self.target_col in X.columns:
            self.target = X.loc[:, self.target_col]
            return X.drop(self.target_col, axis=1, errors="ignore")

        return X


class DropId():
    """Drop Id columns (if exists)
    """

    def __init__(self, id_columns):
        self.id_columns = id_columns
        self.id = None

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        self.id = X[self.id_columns]
        return X.drop(self.id_columns, errors="ignore", axis=1)


class DropSmallPeriodRows():
    """Drop rows with an activity periods (time difference between first and last queries) too small
    """

    def __init__(self, period_col: str = "activityperiod", min_activity_period: int = 10):
        self.min_activity_period = min_activity_period
        self.period_col = period_col

    def is_higher_than_activity_period(self, x):
        return pd.isnull(x) or np.isnan(x) or x > self.min_activity_period

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        n_rows_before = X.shape[0]
        if self.period_col in X.columns:
            res = X.loc[X.loc[:, self.period_col].map(self.is_higher_than_activity_period), :]
            logging.warning(f"dropped {n_rows_before - res.shape[0]} rows because" \
                            f" of activity period of less than "\
                            f"{self.min_activity_period} minutes")
            return res

        return X

class SelectColumnsWithPrefix(BaseEstimator, TransformerMixin):
    """Select all columns starting with a string
    """
    def __init__(self, prefix, accept_numpy=False):
        self.prefix = prefix
        self.regex = f"^{self.prefix}"
        self.accept_numpy = accept_numpy
        self.selected_columns = None
        self.columns_index = None
        self.n_features_in_ = None

    def fit(self, X, y=None):
        self.selected_columns = list(X.filter(regex=self.regex, axis=1).columns)
        self.n_features_in_ = len(self.selected_columns)
        self.columns_index = [i for i, colname in enumerate(X.columns) if colname in self.selected_columns]
        return self

    def transform(self, X, y=None):
        if isinstance(X, np.ndarray) and (self.accept_numpy is False):
            raise ValueError("SelectColumnsWithPrefix cannot accept np.array by default, please pass 'accept_numpy=True' parameters to accept numpy array in transform")

        if not isinstance(X, np.ndarray) and not isinstance(X, pd.DataFrame):
            raise ValueError(f"Input for SelectColumnsWithPrefix should be pd.DataFrame or np.array, found {type(X)}")

        if isinstance(X, pd.DataFrame):
            return X.loc[:, self.selected_columns]

        if isinstance(X, np.ndarray) and (self.accept_numpy is True):
            return X[:, self.columns_index]

        raise NotImplementedError


class ReplaceInf(BaseEstimator, TransformerMixin):
    """Replace all infinite value with missing values
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        res = X.replace([np.inf, -np.inf], np.nan)
        return res


class RelativeVariable(BaseEstimator, TransformerMixin):
    """
    Class used to create relative variable depending of length of a series

    Attributes:
    !warnings : Relative value computtion will be applied to all columns
    matching 'cols + absolute_col' names.

        cols (list): different high-level columns to apply relative computation
        absolute_col (list): list of name of columns to apply relative computation
        drop_old (bool): if we should drop all (=absolute) column
        colname_of_denominator (str): cols will be divided by colname_of_divisor columns

    """

    def __init__(self, cols, absolute_col, drop_old=True, colname_of_denominator="timedifflength"):
        self.cols = cols
        self.absolute_col = absolute_col
        self.matching_regex = ".*(" + "|".join(self.cols) + ")+" + "(" + "|".join(absolute_col) + ")+.*"
        self.drop_old = drop_old
        self.colname_of_denominator = colname_of_denominator

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        rows_before = X.shape[0]

        columns_to_modify = [x for x in X.columns if bool(re.match(self.matching_regex, x))]

        logging.debug("Applying relative transform to %s", columns_to_modify)

        for col in columns_to_modify:
            X.loc[:, col + "relative"] = X.loc[:, col] / X.loc[:, self.colname_of_denominator]

        if self.drop_old:
            X = X.drop(columns_to_modify, axis=1)
            assert rows_before == X.shape[0]

        return X


class GetFeaturesNames(BaseEstimator, TransformerMixin):
    """Get columns name at a given steps
    """

    def __init__(self):
        self.features_names_after_transform = None
        self.features_names = None

    def fit(self, df, y=None):
        self.features_names = df.columns
        return self

    def transform(self, df):
        self.features_names_after_transform = df.columns
        return df

class SameColumns(BaseEstimator, TransformerMixin):
    """Ensure that columns are the same in fit and transform
    """
    def __init__(self):
        self.features = None

    def fit(self, df, y=None):
        self.features = list(df.columns)
        return self

    def transform(self, df):
        return df.loc[:, self.features]


class Debug(BaseEstimator, TransformerMixin):
    """Get columns name at a given steps
    """

    def fit(self, df, y=None):
        return self

    def transform(self, df):
        logging.debug(f"SHAPE = {df.shape}")
        return df


class DropColumnsWithRegex(BaseEstimator, TransformerMixin):
    """
    Class used to drop columns matchning regex in list

    Attributes:
    regex: (list) list of regex to exclude from columns

    """

    def __init__(self, regex):
        self.regex = regex
        self.columns = None

    def fit(self, X, y=None):
        self.columns = X.columns
        for regex in self.regex:
            logging.debug(f"Dropping columns matching : {regex}")
            self.columns = [x for x in self.columns if not re.match(regex, x)]

        logging.debug(f"{len(self.columns)} Selected columns")
        return self

    def transform(self, X, y=None):
        columns_data = X.columns
        columns_diff = set(self.columns) - set(columns_data)
        if len(columns_diff) > 0:
            logging.warning(f"X should contains columns in transformer, but {columns_diff} is missing from X columns")

        if "target" in columns_data:
            return X.reindex(columns=self.columns)

        return X.reindex(columns=[x for x in self.columns if x != "target"])


class SimilarColumns(BaseEstimator, TransformerMixin):
    """ Ensure that similar columns are in test and train dataset.
    If a column is in test but not in train, then the column will be created in
    train dataset with missing value everywhere.

    Parameters
    ----
    None

    Attributes
    ----
    after transform return pandas dataframe with same columns name
    as in fitted dataset.
    """
    def __init__(self):
        self.col = None

    def fit(self, df, y=None, **fit_params):
        """ Fit transformer
        """
        # pylint: disable=unused-argument
        self.col = df.columns
        return self

    def transform(self, df, **transform_params):
        """ Transform / Apply transformer
        """
        # pylint: disable=unused-argument
        for col in self.col:
            if col not in df.columns:
                df[col] = np.nan
        # reorder columns
        df = df.loc[:, self.col]
        return df
