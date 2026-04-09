DROP TABLE IF EXISTS t;
DROP TABLE IF EXISTS t_decimal;

CREATE TABLE t (
  double_value DOUBLE,
  float_value REAL,
  int32_value INT,
  int64_value BIGINT,
  uint32_value INT,
  uint64_value BIGINT,
  sint32_value INT,
  sint64_value BIGINT,
  fixed32_value INT,
  fixed64_value BIGINT,
  sfixed32_value INT,
  sfixed64_value INT,
  string_value VARCHAR(255),
  bytes_value VARBINARY(255)
);

CREATE TABLE t_decimal (
  decimal_value DECIMAL(15, 2),
  d DATE,
  t TIME,
  stamp1 TIMESTAMP,
  stamp2 TIMESTAMP WITH TIME ZONE,
  blob1 BLOB,
  clob1 CLOB
);
