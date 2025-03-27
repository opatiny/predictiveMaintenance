from sklearn.decomposition import PCA
import numpy as np

def apply_pca(feature_matrix, n_components=2):
    """
    Apply PCA to reduce the dimensionality of the feature matrix.

    Parameters:
    feature_matrix (array-like): The matrix of feature vectors.
    n_components (int): The number of principal components to keep.

    Returns:
    reduced_features (array-like): The reduced feature matrix.
    """
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(feature_matrix)
    return reduced_features