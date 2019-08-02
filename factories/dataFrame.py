import pandas as pd

class DataFrameFactory:

    @staticmethod    
    # returns a Pandas DataFrame from the list
    def generateDataFrame(data:any):
        return pd.DataFrame(data)
    
    @staticmethod
    def createDataFrame(values, cols):
        return pd.DataFrame(values, columns=cols)

    @staticmethod
    # returns a new dataframe which is the concatenation of the ones passed
    def joinDataFrames(df1, df2):
        return pd.concat([df1, df2], axis=1)

    @staticmethod
    def convertDataFrameToList(df:any):
        return df.reset_index().to_dict(orient="records")
