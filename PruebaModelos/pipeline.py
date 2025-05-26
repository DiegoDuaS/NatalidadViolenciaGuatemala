from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

#Creacion de Pipelines para cada modelo
def crear_pipeline_regresion(modelo):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('model', modelo)
    ])
    return pipeline

def crear_pipeline_knn(modelo):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('model', modelo)
    ])
    return pipeline

def crear_pipeline_svm(modelo):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('model', modelo)
    ])
    return pipeline

def crear_pipeline_regresion_lineal(modelo):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()), 
        ('model', modelo)
    ])
    return pipeline

def crear_pipeline_random_forest(modelo):
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('model', modelo)
    ])
    return pipeline

