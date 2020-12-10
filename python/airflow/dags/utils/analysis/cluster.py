import logging
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from airflow.hooks.postgres_hook import PostgresHook

from .queries import *


logging.basicConfig()
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


def detect_num_clusters(X_norm):
    score_max, best_n = -1, 2
    for n_clusters in range(2, 10):
        model = KMeans(n_clusters=n_clusters, max_iter=300)
        labels = model.fit_predict(X_norm)
        score = silhouette_score(X_norm, labels)
        logger.info(f"Silhouette score for {n_clusters} clusters is {score}.")
        if score > score_max:
            best_n = n_clusters
            score_max = score
    logger.info(f"Best value for number of clusters is {best_n} with max score {score_max}.")
    return best_n


def clustering_model():
    hook = PostgresHook(postgres_conn_id="postgres_quake_tr")
    df = hook.get_pandas_df(select_tr_quakes_to_cluster)
    df = df.sample(frac=1)
    scaler = StandardScaler()
    X = df[["lat", "lon"]].values
    X_norm = scaler.fit_transform(X)
    num_clusters = detect_num_clusters(X_norm)
    model = KMeans(n_clusters=num_clusters, max_iter=300)
    model.fit(X_norm)
    logger.info(f"Cluster model ready with {num_clusters} cluster centroids.")
    return model, scaler


def drop_cluster_table():
    with PostgresHook(postgres_conn_id="postgres_quake_tr").get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS geospatial_clustering")


def insert_cluster_labels():
    hook = PostgresHook(postgres_conn_id="postgres_quake_tr")
    df = hook.get_pandas_df("SELECT * FROM quake_tr ORDER BY quake_time DESC")
    model, scaler = clustering_model()
    X_norm = scaler.transform(df[["lat", "lon"]].values)
    df["cluster_label"] = model.predict(X_norm)
    params = df.values.tolist()
    hook.insert_rows("geospatial_clustering", params)
