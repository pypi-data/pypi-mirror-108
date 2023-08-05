import numpy as np
import pandas as pd


class Regression:
    """Class for a Regression Analysis

    Attributes
    ----------
    deg : int
            The degree of polynoms used in the model
    """

    def __init__(self, deg=1):
        self.deg = deg

    def fit(self, X, y):
        """Estimates the Regression parameters beta

        Parameters
        ----------
        X : DataFrame
                The input feature matrix without threshold column
        y : DataFrame
                The dependent variable

        Returns
        ----------
        beta : 1-dim DataFrame with Regression parameters beta

        """
        nr_columns = len(X.columns)
        X_pol = X
        deg = self.deg
        if deg > 1:
            X_pol = pd.DataFrame()
            for d in range(deg):
                for i in range(nr_columns):
                    X_pol.insert(
                        len(X_pol.columns),
                        f"f{i + 1}deg{d + 1}",
                        X.iloc[:, i] ** (d + 1),
                    )

        X_pol.insert(0, "constant", 1)

        X_t = X_pol.transpose()

        beta = np.array(np.linalg.pinv(X_t.dot(X_pol)).dot(X_t.dot(y)))
        beta = np.around(beta, 2)
        self.beta = beta

        return beta

    def predict(self, X):
        """Predicts new observations by applying beta estimations

        Parameters
        ----------
        X : DataFrame
                The observed features to be predicted on

        Returns
        ----------
        y : The predicted dependend variable

        """
        nr_columns = len(X.columns)
        X_pol = X
        deg = self.deg
        if deg > 1:
            X_pol = pd.DataFrame()
            for d in range(deg):
                for i in range(nr_columns):
                    X_pol.insert(
                        len(X_pol.columns),
                        f"f{i + 1}deg{d + 1}",
                        X.iloc[:, i] ** (d + 1),
                    )

        X.insert(0, "constant", 1)
        y = X_pol.dot(self.beta)

        return y
