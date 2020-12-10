# select

select_tr_quakes_to_cluster = """
SELECT *
FROM quake_tr
WHERE 
    lat >= '30.0' AND lat <= '47.0'
    AND lon >= '21.0' AND lon <= '50.0'
    AND ml >= '3.5'
ORDER BY quake_time DESC;
"""


# create

create_clustering_table = """
CREATE TABLE IF NOT EXISTS geospatial_clustering
(
    quake_id INT PRIMARY KEY,
    quake_code VARCHAR,
    quake_time TIMESTAMP,
    lat FLOAT,
    lon FLOAT,
    depth FLOAT,
    xm FLOAT,
    md FLOAT,
    ml FLOAT,
    mw FLOAT,
    ms FLOAT,
    mb FLOAT,
    quake_type VARCHAR,
    location VARCHAR,
    cluster_label INT
);
"""
