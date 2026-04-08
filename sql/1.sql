drop table if exists t;

create table t (
    double_value double,
    float_value real,
    int32_value int,
    int64_value bigint,
    uint32_value int,
    uint64_value bigint,
    sint32_value int,
    sint64_value bigint,
    fixed32_value int,
    fixed64_value bigint,
    sfixed32_value int,
    sfixed64_value bigint
);
insert into t values (
    1.25,
    2.5,
    3,
    4,
    5,
    6,
    -7,
    -8,
    9,
    10,
    -11,
    -12
);
insert into t values (
    1.25,
    2.5,
    3,
    4,
    null,
    6,
    -7,
    -8,
    9,
    10,
    -11,
    -12
);
select optional_all(
    double_value,
    float_value,
    int32_value,
    int64_value,
    uint32_value,
    uint64_value,
    sint32_value,
    sint64_value,
    fixed32_value,
    fixed64_value,
    sfixed32_value,
    sfixed64_value
) from t;