import numpy as np
class Pooler:
    def pool(self, array, pooling_strategy: str):
        """
        Custom pooling strategies.
        vector_operation: One of ['mean', 'minus', 'sum', 'min', 'max']
        """
        return self._vector_operation(array, pooling_strategy=vector_operation)

    def _vector_operation(self, vectors, vector_operation: str = "mean", axis=0):
        """
            Args:
                Vectors: the list of vectors to include
                vector_operation: One of ['mean', 'minus', 'sum', 'min', 'max']
                axis: The axis to which to perform the operation
        """
        if vector_operation == "mean":
            return np.mean(vectors, axis=axis).tolist()
        elif vector_operation == 'minus':
            return np.subtract(vectors, axis=axis).tolist()
        elif vector_operation == "sum":
            return np.sum(vectors, axis=axis).tolist()
        elif vector_operation == "min":
            return np.min(vectors, axis=axis).tolist()
        elif vector_operation == "max":
            return np.max(vectors, axis=axis).tolist()
        else:
            return np.mean(vectors, axis=axis).tolist()
