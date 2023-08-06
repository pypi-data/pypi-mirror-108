'''
Created with love by Sigmoid
​
@Author - Stojoc Vladimir - vladimir.stojoc@gmail.com
'''
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

class ExpandingMeanTransformer(BaseEstimator, TransformerMixin):

    def __init__(self,index : list = None, min_int_freq : int = 10) -> None:
        """
        Constructor of the Expanding mean encoding class
        :param categorical_index: list, default = 'auto'
            A parameter that specifies the list of indexes of categorical columns that should be transformed.
        :param min_int_freq: int, default = 5
            A parameter that indicates the number of minimal values in a categorical column for the transformer
            to be applied.
        """
        self.index = index
        self.__min_int_freq = min_int_freq

    def fit(self, X : 'np.array', y : 'np.array', **fit_params : dict):
        '''
            The fit function of the ExpandingMean, fits up the model.
        :param X: 2-d numpy array or pd.DataFrame
            The 2-d numpy array or pd.DataFrame that represents the feature matrix.
        :param y: 1-d numpy array or pd.DataFrame
            The 1-d numpy array or pd.DataFrame that represents the target array.
        :param fit_params: dict
            The fit parameters that control the fitting process.
        :return: MeanEncoding
            The fitter ExpandingMean object.
        '''
        self.shape = X.shape
        return self

    def transform(self, X : 'np.array', y : 'np.array', **fit_params : dict) -> 'np.array':
        '''
            The transform function of the ExpandingMean, transforms the passed data..
        :param X: 2-d numpy array or pd.DataFrame
            The 2-d numpy array or pd.DataFrame that represents the feature matrix.
        :param y: 1-d numpy array or pd.DataFrame, default = None
            The 1-d numpy array or pd.DataFrame that represents the target array.
        :param fit_params: dict
            The fit parameters that control the fitting process.
        :return: np.array
            The transformed data.
        '''
                
        #Get categorical columns
        if self.shape[1] == X.shape[1]:
            self.X_copy = X.copy()

            #set columns which will be transformed if index list was not given
            if self.index is None:
                self.index = [i for i in range(self.X_copy.shape[1]) if isinstance(self.X_copy[0 ,i],str) and len(set(self.X_copy[:, i])) < self.__min_int_freq and len(set(self.X_copy[:, i])) != 2]

            #creating Pandas DataFrame from numpy arrays
            self.df = np.column_stack([self.X_copy,y])
            self.df = pd.DataFrame(self.df)
            self.df = self.df.convert_dtypes()
            #Empirical mean encoding, calculating cumulative sum and count of the column
            for col in self.index:
                cumsum = self.df.groupby(col)[self.df.columns[-1]].cumsum()-self.df[self.df.columns[-1]]
                cumcnt = self.df.groupby(col)[self.df.columns[-1]].cumcount()
                self.df.iloc[:,col]=cumsum/cumcnt
                self.df.iloc[:,col].fillna(self.df.iloc[:,col].mean(),inplace=True)
        
        else:
            raise ValueError(f'Was passed an array with {X.shape[1]} features, while where required {self.shape[1]} features')

        return self.df.iloc[:,:-1].values

    def fit_transform(self, X : 'np.array', y : 'np.array', **fit_params : dict):
        '''
            Function that fits and transform the data
        :param X: 2-d numpy array
            A parameter that stores the data set without the target vector.
        :param y: 1-d numpy array
            A parameter that stores the target vector.
        :param fit_params: dict
            Additional fit parameters.
        :return: 2-d numpy array
            The transformed 2-d numpy array.
        '''
        return self.fit(X, y).transform(X,y)

    def apply(self, df : 'pd.DataFrame', target: str, columns : list = None) -> 'pd.DataFrame':
        '''
            This function allows applying the transformer on certain columns of a data frame.
        :param df: pandas DataFrame
            The pandas DataFrame on which the transformer should be applied.
        :param target: string
             The target name of the value that will be predicted
        :param columns: list
            The list if the names of columns on which the transformers should be applyed.
        :return: pandas DataFrame
            The new pandas DataFrame with transformed columns.
        '''
        # Checking if columns aren't set as None.
        if columns is not None:
            # Checking if passed columns exist in the passed DataFrame.   
            columns_difference = set(columns) - set(df.columns)
            if len(columns_difference) != 0:
                raise ValueError(f"Columns {', '.join(list(columns_difference))} are not present in the passed data frame")
            elif target in columns:
                raise ValueError(f"Target column {target} was passed as a feature name")
            else:
                # Setting upe the categorical index
                columns_list = list(df.columns)
                self.index = []
                for col in columns:
                    self.index.append(columns_list.index(col))
                # Removing the target name from the columns list.v
                columns_list.remove(target)
        else:
            columns_list = list(df.columns)
            columns_list.remove(target)
            self.index = None
        # Transforming the data frame.
        df_copy = df.copy()
        df_copy[columns_list] = self.fit_transform(df_copy[columns_list].values)
        df_copy[target] = df[target]
        return df_copy