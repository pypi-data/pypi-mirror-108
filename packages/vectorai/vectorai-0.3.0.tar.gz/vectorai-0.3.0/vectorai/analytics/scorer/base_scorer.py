"""
    Base Scorer
"""
from abc import abstractmethod
from ...utils import UtilsMixin

class AbstractScorer(UtilsMixin):
    """
        Abstract Scoring System For Calculating Scores
    """
    def __init__(self, documents):
        pass
    
    @abstractmethod
    def score(self, vector_1, vector_2):
        pass
  
    def score_across_documents(self, other_documents: list, anchor_document: dict, vector_field: str):
        """
            Score between anchor document and other documents. 
            Args:
                Docs: List of documents (Python dictionaries)
                Anchor_document: Document (Python dictionary) 
                vector_field: The alias for the vector 
        """
        similarity_scores = [self.score(self.get_field(vector_field, doc),
                self.get_field(vector_field, anchor_document))]
        for i, doc in enumerate(other_documents):
            similarity_score = self.score(
                self.get_field(vector_field, doc),
                self.get_field(vector_field, anchor_document)
            )
            similarity_scores.append(similarity_score)
        return similarity_scores
