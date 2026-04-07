drop table if exists t;
CREATE TABLE t (id INT,va INT);
INSERT INTO t (id,va) VALUES (1,2);
select optional_add(id,va) from t;
