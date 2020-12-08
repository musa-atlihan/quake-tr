# create tables

create_quake_tr_table = """
CREATE TABLE IF NOT EXISTS quake_tr
(
    quake_id SERIAL PRIMARY KEY,
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
    location VARCHAR
);
"""


# insert queries

insert_quake_tr_table = """
INSERT INTO quake_tr
(
    quake_id, quake_code, quake_time,
    lat, lon, depth,
    xm, md, ml, 
    mw, ms, mb, 
    quake_type, location
)
VALUES
(
    DEFAULT, %s, %s,
    %s, %s, %s,
    %s, %s, %s,
    %s, %s, %s,
    %s, %s
)
"""
