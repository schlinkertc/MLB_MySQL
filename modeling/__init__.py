"""Custom classes for modeling"""
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier,VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.model_selection import KFold,StratifiedKFold
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import metrics
from sklearn.metrics import precision_score,recall_score,f1_score,roc_auc_score,roc_curve
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.preprocessing import PolynomialFeatures

class PipeLine():
    
    def __init__(self,data,Y,output_type,steps,*args,**kwargs):
        """
        A series of steps applied to a dataset.
        Including but not limited to:
            - cross validation
            - grid-search / random search
            - synthetic minority over sampling 
            - model performance metrics 
            - encoding categorical/ordinal variables
            - filling missing values 
        Data takes the form of a pandas dataframe for now. 
        *args: series of transformers like a normal sklearn pipeline
        """
        pipeline = Pipeline(steps)
        
        # Y can be a series or a string
        # if string, it represents a column index
        if type(Y)==str:
            X = data.drop(columns=[Y])
            Y = data[Y]

        if type(Y)==pd.Series or type(Y)==pd.DataFrame:
            Y = Y
            X = data
            
        
        if 'kfold' in kwargs.keys() and output_type=='categorical':
            kfold = StratifiedKFold(n_splits=5)
            reports = []
            for train, test in kfold.split(X, Y):
                fit = pipeline.fit(X.iloc[train], Y.iloc[train])
                prediction = pipeline.predict(X.iloc[test])

                reports.append(
                    pd.DataFrame(
                        metrics.classification_report(
                            Y.iloc[test],prediction,output_dict=True
                        )
                    )
                )

            df_concat = pd.concat([x for x in reports])

            by_row_index = df_concat.groupby(df_concat.index)
            df_means = by_row_index.mean()
            self.report = df_means
            