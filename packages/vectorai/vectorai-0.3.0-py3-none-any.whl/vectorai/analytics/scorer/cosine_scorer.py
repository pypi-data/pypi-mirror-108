from .base_scorer import AbstractScorer
from numpy import inner
from numpy.linalg import norm

class CosineScorer(AbstractScorer):
    """
        Score with Cosine.
    """
    def score(a, b):
        """
            Score cosine.
        """
        return inner(a, b) / (norm(a) * norm(b))

class RegularisedCosineScorer(AbstractScorer):
    """
        Score with Cosine - regularised by a specific doc attribute
    """
    def cosine_score(a, b):
        """
            Score cosine.
        """
        return inner(a, b) / (norm(a) * norm(b))

    def score(self, doc_1: dict, doc_2: dict, reg_field: str, noise=1e-7):
        """
            Args:
                doc_1: First document 
                doc_2: Second document
                reg_field: The field to regularise with
                noise: A default value to avoid division by zero
        """
        return self.cosine_score(a, b) / (self.get_field(reg_field) + noise)
