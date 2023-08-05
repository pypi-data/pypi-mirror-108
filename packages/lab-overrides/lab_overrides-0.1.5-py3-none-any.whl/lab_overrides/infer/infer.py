import tensorflow as tf
import pandas as pd
import numpy as np


def infer(data: pd.DataFrame) -> np.ndarray:
    new_model = tf.keras.models.load_model('/Users/tovahallas/Downloads/8543fd2b-2e42-4b47-91a9-ab0e163bb3c3_SavedModel')
    new_model.summary()
    prediction = new_model.predict(data)
    return prediction