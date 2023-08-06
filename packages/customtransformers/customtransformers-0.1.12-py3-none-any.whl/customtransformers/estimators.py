import numpy as np

from sklearn.ensemble import VotingClassifier
from sklearn.utils.validation import check_is_fitted

class MaxClassifier(VotingClassifier):  # pylint: disable=too-many-ancestors
    """Overwrite of VotingClassfier to use max instead of average of predicted probabilities
    """

    def __init__(self, estimators, **kwargs):
        VotingClassifier.__init__(self, estimators, **kwargs)
        self.voting = "soft"  # Soft to call predict_proba

    def _predict_proba(self, X: np.array) -> float:
        """Predict proba using max of computed probabilities

        Args:
            X (np.array): input.

        Returns:
            float: Computed probabilities.
        """
        check_is_fitted(self)
        mymax = np.amax(self._collect_probas(X), axis=0)
        return mymax
