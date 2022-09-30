import pickle
import pandas as pd
from sklearn.decomposition import PCA, FastICA

def predict(model="finalized_model.sav", signal="ecg_3.csv"): 
    clf = pickle.load(open(model, "rb")) 
    transformer = FastICA(n_components=18, random_state=0, whiten = 'unit-variance') 
    X_ = pd.read_csv(signal) 
    X_transformed = transformer.fit_transform(X_) 

    X_transformed = pd.Series(X_transformed)

    X_ICA = pd.merge(X_, X_transformed, left_index=True, right_index=True) 
    pca = PCA(n_components=26) 
    X_PCA = pd.DataFrame(pca.fit_transform(X_ICA)) 

    return clf.predict([X_PCA])

print(predict())