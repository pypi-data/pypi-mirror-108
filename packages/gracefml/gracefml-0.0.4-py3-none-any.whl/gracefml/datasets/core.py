import pandas as pd
from os.path import dirname, join


def load_boston() -> pd.DataFrame:
    """Load and return the boston house-prices dataset (regression).
    ==============   ==============
    Samples total               506
    Dimensionality               13
    Features         real, positive
    Targets           real 5. - 50.
    ==============   ==============

    Parameters
    ----------

    Returns
    -------
    data : :class:pd.DataFrame

    Examples
    --------
    >>> from sklearn.datasets import load_boston
    >>> X, y = load_boston(return_X_y=True)
    >>> print(X.shape)
    (506, 13)
    """
    module_path = dirname(__file__)

    return pd.read_csv(join(module_path, "data", "boston_house_prices.gz"))
