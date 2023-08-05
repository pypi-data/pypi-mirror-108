from .infer.infer import infer
import pandas as pd

def infer():
    # generate df
    df = pd.DataFrame()
    prediction = infer(df)