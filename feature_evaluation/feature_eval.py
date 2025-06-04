import numpy as np
import pandas as pd
from itertools import combinations
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def import_features(xlsx_path, feature_suffixe = None, forbiden_signals = None):

    data = pd.read_excel(xlsx_path, index_col=0)
    
    if forbiden_signals :
        for i in forbiden_signals:
            try :
                data.drop(i)
            except:
                None

    if feature_suffixe :
        renamed_index = [i+feature_suffixe for i in data.index]
        data.index = renamed_index

    return data


def get_paired_features(features : pd.DataFrame) :
    pairs = [(i, j) for i, j in combinations(features.index, 2)]
    pair_dfs = [features.loc[[i, j]] for i, j in pairs]

    return pair_dfs


def cluster_points(data: np.ndarray, n_clusters: int = 3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(data) #(n_samples, n_features)
    centers = kmeans.cluster_centers_
    
    return labels, centers


def get_cluster_preds(paired_features : list):
    preds_list = []
    centers_list = []
    for pair in paired_features :
        data = pair.to_numpy().transpose()
        preds, centers = cluster_points(data)
        preds_list.append(preds)
        centers_list.append(centers)


    return preds_list, centers_list


def get_ari_scores(pred_list : list, true : list):
    ari_scores = []
    for pred in pred_list :
        ari_scores.append(adjusted_rand_score(true, pred))

    return ari_scores

def plot_scores(feature_scores : dict):
    # Bar plot horizontal
    plt.figure(figsize=(16, 10))
    plt.barh(feature_scores.keys(), feature_scores.values())
    plt.yticks(fontsize=9)
    plt.xlabel("ari score")
    plt.ylabel('best features pairs')
    plt.tight_layout()
    plt.show()

def plot_results(X, pred, true, axe_labels, same_axe_scale= False):
    if same_axe_scale :
        x_min = np.min(X[:,0])
        x_max = np.max(X[:,0])
        y_min = np.min(X[:,1])
        y_max = np.max(X[:,1])

        min_ = np.min([x_min, y_min])*0.9
        max_ = np.max([x_max, y_max])*1.1


    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].scatter(X[:, 0], X[:, 1], c=true, cmap='viridis', s=40)
    axes[0].set_title("True Labels")
    axes[0].set_xlabel(axe_labels[0])
    axes[0].set_ylabel(axe_labels[1])
    if same_axe_scale :
        axes[0].set_xlim(min_,max_)
        axes[0].set_ylim(min_,max_)


    axes[1].scatter(X[:, 0], X[:, 1], c=pred, cmap='viridis', s=40)
    axes[1].set_title("KMeans Predictions")
    axes[1].set_xlabel(axe_labels[0])
    axes[1].set_ylabel(axe_labels[1])

    if same_axe_scale :
        axes[1].set_xlim(min_,max_)
        axes[1].set_ylim(min_,max_)

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    forbiden_signals = pd.read_excel("forbiden_signals.xlsx").to_numpy().ravel().tolist()
    forbiden_signals = [i.split(".csv")[0] for i in forbiden_signals]

    means = import_features("means_clean.xlsx", "_mean", forbiden_signals)
    vars = import_features("vars_clean.xlsx", "_var", forbiden_signals)
    
    frequs = import_features("fft_peaks_transposed.xlsx")
    frequs = frequs.dropna()
    
    true_var_mean = [0,0,0,0,0,0,1,1,1,2,2] #integrer labelisation automatique

    frequ_cols = list(frequs.columns)
    true_frequ = [i.split("_")[0] for i in frequ_cols]
    mapping = {'Mecatis': 0, 'MILL': 1, 'Locle': 2}
    true_frequ = [mapping[elem] for elem in true_frequ]

    rescale_data = True

    if rescale_data : 
        scaler_means = StandardScaler()
        means_np = means.to_numpy().transpose()
        means_scaled = scaler_means.fit_transform(means_np)
        means = pd.DataFrame(means_scaled.transpose(), columns=means.columns, index=means.index)

        scaler_vars = StandardScaler()
        var_np = vars.to_numpy().transpose()
        vars_scaled = scaler_vars.fit_transform(var_np)
        vars = pd.DataFrame(vars_scaled.transpose(), columns=vars.columns, index=vars.index)

        scaler_frequs = StandardScaler()
        frequs_np = frequs.to_numpy().transpose()
        frequs_scaled = scaler_frequs.fit_transform(frequs_np)
        frequs = pd.DataFrame(frequs_scaled.transpose(), columns=frequs.columns, index=frequs.index)

    #choose either vars with means or frequences alone as features to evaluate
    features_we_want = "var_mean"
    if features_we_want == "frequ" :
        features = frequs
        true = true_frequ
    elif features_we_want == "var_mean" :
        features = pd.concat([means, vars], axis=0)
        true = true_var_mean

    paired_features = get_paired_features(features)
    cluster_preds, cluster_centers = get_cluster_preds(paired_features)
    ari_scores = get_ari_scores(cluster_preds, true)
    
    paire_names = ["/".join(i.index) for i in paired_features]

    features_ari_scores = dict(zip(paire_names, ari_scores))
    features_ari_scores = dict(sorted(features_ari_scores.items(), key=lambda item: item[1], reverse=True)) # sorted decroissant
    
    best_scores = dict(list(features_ari_scores.items())[:50])
    #best_scores = dict(list(features_ari_scores.items()))
    plot_scores(best_scores)
    
    print(len(paire_names))
    # a mettre dans une fonction et jupyter notebook
    for index in range(5):
        features_to_plot_key = list(best_scores.keys())[index]
        features_to_plot = features_to_plot_key.split("/")
        print(features_to_plot)
        X = np.stack((features.loc[features_to_plot[0]].to_numpy(), features.loc[features_to_plot[1]].to_numpy()), axis=-1)
        index_pred = paire_names.index(features_to_plot_key)
        pred = cluster_preds[index_pred]
        plot_results(X, pred, true, axe_labels=features_to_plot)

