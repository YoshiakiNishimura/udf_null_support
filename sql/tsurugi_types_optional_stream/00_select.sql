SELECT R.value1, R.value2, R.value3, R.value4, R.value5, R.value6, R.value7
FROM t_decimal
CROSS APPLY tsurugi_types_optional_stream(
t_decimal.decimal_value, t_decimal.d, t_decimal.t, t_decimal.stamp1, t_decimal.stamp2, t_decimal.blob1, t_decimal.clob1
)AS R(value1, value2, value3, value4, value5, value6, value7);