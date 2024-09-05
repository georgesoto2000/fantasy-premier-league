import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
import shap


class FeatureImportance:
    def plot_importance(
        importances: np.array, feature_names: list, X: pd.DataFrame, fname: str
    ) -> None:
        """Display Factor Importances

        Args:
            importances (np.array): importances
            feature_names (list): feature names
            X (pd.DataFrame): x data
            fname (str): filename to save as
        """
        indices = np.argsort(importances)[::-1]
        names = [feature_names[i] for i in indices]
        plt.figure(figsize=(10, 6))
        plt.title("Feature Importances")
        plt.bar(range(X.shape[1]), importances[indices])
        plt.xticks(range(X.shape[1]), names, rotation=90)
        plt.xlabel("Features")
        plt.ylabel("Importance")
        plt.savefig(fname)
        plt.show()

    def SHAP(model: GradientBoostingRegressor, X: pd.DataFrame) -> None:
        """Creates SHAP plot

        Args:
            model (GradientBoostingRegressor): trained model
            X (pd.DataFrame): X data
        """
        shap.initjs()
        explainer = shap.Explainer(model, X)
        shap_values = explainer(X)
        shap.plots.beeswarm(shap_values.abs, order=shap_values.abs.max(0))
