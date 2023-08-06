import mlflow
import numpy as np
import pandas as pd


class BaseMlflowModel (mlflow.pyfunc.PythonModel):

    def __init__(self, model: object, model_params: dict):
        super().__init__()
        self.model_params = model_params
        self.model = model(**self.model_params)
        # self.conda_env = CondaEnv()
        # TODO - check if model and model_params are ok

    def predict(self, dataset: pd.DataFrame) -> np.ndarray:
        result = self.model.predict(dataset)
        return result

    def fit(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        X_train, y_train = self._preprocessing(X_train, y_train)
        self.model.fit(X_train, y_train)

    def _preprocessing(self, X_train, y_train):
        return X_train, y_train

    def eval_metrics(self, y_hat: pd.DataFrame, y: pd.DataFrame) -> dict:
        """
        returns the common metrics for the model
        """

        err_sum = np.sum(np.abs(y_hat - y))
        acc = np.sum(y) / (np.sum(y)+err_sum)

        return {'accuracy': float(acc)}


# class CondaEnv:

#     conda_env = {
#         'channels': ['defaults'],
#                  'dependencies': [
#                      'python={}'.format(PYTHON_VERSION),
#                      'pip',
#                      {
#                          'pip': [
#                              'mlflow',
#                                  'xgboost=={}'.format(self.__version__),
#                                  'cloudpickle=={}'.format(
#                                      cloudpickle.__version__),
#                          ],
#                  },
#                      ],
#         'name': 'xgb_env'
#         }

#        def __init__(self,):
#             pass

#         def add(self, libr):
#             pass
