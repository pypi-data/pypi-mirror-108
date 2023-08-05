import requests
from typing import Union, List
from ...base import Base2Vec
from ...import_utils import is_all_dependency_installed
# TODO: Change encoders-image-tfhub into general encoders-image
if is_all_dependency_installed('encoders-image'):
    import io
    import imageio
    import numpy as np
    import matplotlib.pyplot as plt
    from urllib.request import urlopen, Request
    from skimage import transform

class ImageReader:
    def read(self, image: str):
        """
            An method to read images. 
            Args:
                image: An image link/bytes/io Bytesio data format.
                as_gray: read in the image as black and white
        """
        if type(image) == str:
            if 'http' in image:
                try:
                    b = io.BytesIO(urlopen(Request(
                        image, headers={'User-Agent': "Mozilla/5.0"})).read())
                except:
                    import tensorflow as tf
                    return tf.image.decode_jpeg(requests.get(image).content, channels=3, name="jpeg_reader").numpy()
            else:
                b = image
        elif type(image) == bytes:
            b = io.BytesIO(image)
        elif type(image) == io.BytesIO:
            b = image
        else:
            raise ValueError("Cannot process data type. Ensure it is is string/bytes or BytesIO.")
        try:
            return np.array(imageio.imread(b, pilmode="RGB"))
        # TODO: Flesh out exceptions
        except:
            return np.array(imageio.imread(b)[:, :, :3])

    def bulk_read(self, images: List[str]):
        return [self.read(x) for x in images]
