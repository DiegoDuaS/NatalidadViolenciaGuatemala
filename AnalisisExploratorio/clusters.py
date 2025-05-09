from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import sklearn
import statsmodels.stats.diagnostic as diag
import statsmodels.api as sm
import seaborn as sns
import scipy.cluster.hierarchy as sch
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
from sklearn.feature_selection import mutual_info_classif, VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

def elbow(X_scale):
    numeroClusters = range(1,20)
    wcss = []
    for i in numeroClusters:
        kmeans = KMeans(n_clusters=i, random_state=42)
        kmeans.fit(X_scale)
        wcss.append(kmeans.inertia_)

    plt.plot(numeroClusters, wcss, marker='o')
    plt.xticks(numeroClusters)
    plt.xlabel("K clusters")
    plt.ylabel("WSS")
    plt.title("Gráfico de Codo")
    plt.show()


def compute_feature_scores(X, labels, method, n_components, threshold):
    if method == "mutual_info":
        if labels is None:
            raise ValueError("Mutual Information requires labels.")
        scores = mutual_info_classif(X, labels, discrete_features=False)
    
    elif method == "pca":
        if n_components is None:
            raise ValueError("Specify n_components for PCA.")
        pca = PCA(n_components=n_components)
        pca.fit_transform(X)
        scores = pca.explained_variance_ratio_  # Variance explained by each component
    
    elif method == "random_forest":
        if labels is None:
            raise ValueError("Random Forest feature importance requires labels.")
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, labels)
        scores = rf.feature_importances_  # Feature importance scores
    
    elif method == "variance_threshold":
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(X)
        scores = selector.variances_  # Variance of each feature
    
    else:
        raise ValueError("Invalid method. Choose from 'mutual_info', 'pca', 'random_forest', 'variance_threshold'.")
    
    return scores

def get_features(X, v_threshold, n_pca, mi_crit, rf_crit):
    test_cluster_amount = 3
    labels = KMeans(
        n_clusters=test_cluster_amount, 
        random_state=42).fit_predict(X)
    methods = ["mutual_info",
               "pca",
               "random_forest",
               "variance_threshold"]
    fields = {}
    for m in methods:
        if m=="pca":
            feature_scores = compute_feature_scores(
                X=X, labels=labels, 
                method="pca", 
                n_components=n_pca, 
                threshold=0)
        elif m=="variance_threshold":
            feature_scores = compute_feature_scores(
                X=X, labels=labels, 
                method="variance_threshold", 
                n_components=0, 
                threshold=v_threshold)
        else:
            feature_scores = compute_feature_scores(
                X=X, labels=labels, 
                method=m, 
                n_components=0, 
                threshold=0)

        sorted_features = sorted(zip(X.columns, feature_scores), key=lambda x: x[1], reverse=True)
        current = {}
        for feature, score in sorted_features:
            if m == "variance_threshold":
                if(score>v_threshold):
                    current[feature] = score
            elif m== "pca":
                current[feature] = score
            elif m== "random_forest":
                if(score>rf_crit):
                    current[feature] = score
            else:
                if(score>mi_crit):
                    current[feature] = score
        fields[m] = current
    return fields        

def sillhouette(range_n_clusters, X):

    for n_clusters in range_n_clusters:
        # Create a subplot with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches(18, 7)

        # The 1st subplot is the silhouette plot
        # The silhouette coefficient can range from -1, 1 but in this example all
        # lie within [-0.1, 1]
        ax1.set_xlim([-0.1, 1])
        # The (n_clusters+1)*10 is for inserting blank space between silhouette
        # plots of individual clusters, to demarcate them clearly.
        ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

        # Initialize the clusterer with n_clusters value and a random generator
        # seed of 10 for reproducibility.
        clusterer = KMeans(n_clusters=n_clusters, random_state=10)
        cluster_labels = clusterer.fit_predict(X)

        # The silhouette_score gives the average value for all the samples.
        # This gives a perspective into the density and separation of the formed
        # clusters
        silhouette_avg = silhouette_score(X, cluster_labels)
        print(
            "For n_clusters =",
            n_clusters,
            "The average silhouette_score is :",
            silhouette_avg,
        )

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, cluster_labels)

        y_lower = 10
        for i in range(n_clusters):
            # Aggregate the silhouette scores for samples belonging to
            # cluster i, and sort them
            ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]

            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = cm.nipy_spectral(float(i) / n_clusters)
            ax1.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7,
            )

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("The silhouette plot for the various clusters.")
        ax1.set_xlabel("The silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        ax1.set_yticks([])  # Clear the yaxis labels / ticks
        ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

        # 2nd Plot showing the actual clusters formed
        colors = cm.nipy_spectral(cluster_labels.astype(float) / n_clusters)
        ax2.scatter(
            X[:, 0], X[:, 1], marker=".", s=30, lw=0, alpha=0.7, c=colors, edgecolor="k"
        )

        # Labeling the clusters
        centers = clusterer.cluster_centers_
        # Draw white circles at cluster centers
        ax2.scatter(
            centers[:, 0],
            centers[:, 1],
            marker="o",
            c="white",
            alpha=1,
            s=200,
            edgecolor="k",
        )

        for i, c in enumerate(centers):
            ax2.scatter(c[0], c[1], marker="$%d$" % i, alpha=1, s=50, edgecolor="k")

        ax2.set_title("The visualization of the clustered data.")
        ax2.set_xlabel("Feature space for the 1st feature")
        ax2.set_ylabel("Feature space for the 2nd feature")

        plt.suptitle(
            "Silhouette analysis for KMeans clustering on sample data with n_clusters = %d"
            % n_clusters,
            fontsize=14,
            fontweight="bold",
        )

    plt.show()