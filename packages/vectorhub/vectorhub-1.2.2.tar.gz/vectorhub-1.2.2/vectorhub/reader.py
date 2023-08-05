"""
The reader class for VectorHub. 
Basic requirements for reader class: 
i) Read offline images 
ii) Read online images
"""
from abc import abstractmethod

class Reader:
    @abstractmethod
    def read(self, input_object):
        pass

    @abstractmethod
    def bulk_read(self):
        pass
