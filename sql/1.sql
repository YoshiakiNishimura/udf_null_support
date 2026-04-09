-- sqlformat -r -k upper  sql/1.sql
DROP TABLE IF EXISTS t;
CREATE TABLE t (double_value DOUBLE,
                             float_value real, int32_value int,
                             int64_value bigint, uint32_value int,
                             uint64_value bigint, sint32_value int,
                             sint64_value bigint, fixed32_value int,
                             fixed64_value bigint, sfixed32_value int,
                             sfixed64_value bigint, string_value varchar(255),
                             bytes_value varbinary(255));
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (NULL, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,NULL,NULL);
INSERT INTO t
VALUES (NULL, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, NULL, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, NULL, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, NULL, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, NULL, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, NULL, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, NULL, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, NULL, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, NULL, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, NULL, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, NULL, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, NULL,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,NULL,x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',NULL);
INSERT INTO t
VALUES (NULL, NULL, 3, 4, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, NULL, NULL, 5, 6, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, NULL, NULL, -7, -8, 9, 10, -11, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, NULL, NULL, 9, 10, NULL, NULL,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, NULL, NULL, NULL, NULL,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (NULL, 2.5, NULL, 4, NULL, 6, NULL, -8, NULL, 10, NULL, -12,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (NULL, NULL, 3, 4, 5, 6, NULL, NULL, 9, 10, NULL, NULL,'hello',x'68656c6c6f');
INSERT INTO t
VALUES (1.25, 2.5, 3, 4, 5, 6, -7, -8, 9, 10,-11, -12, NULL, NULL);

SELECT optional_all(double_value, float_value, int32_value, int64_value, uint32_value, uint64_value, sint32_value, sint64_value, fixed32_value, fixed64_value, sfixed32_value, sfixed64_value,string_value,bytes_value)
FROM t;
-- select double_value, float_value, int32_value, int64_value, uint32_value, uint64_value, sint32_value, sint64_value, fixed32_value, fixed64_value, sfixed32_value, sfixed64_value,string_value,bytes_value from t;
