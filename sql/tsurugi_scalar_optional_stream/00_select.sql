select * from t;
SELECT R.value
FROM t
CROSS APPLY tsurugi_scalar_optional_stream(
  t.double_value,
  t.float_value,
  t.int32_value,
  t.int64_value,
  t.uint32_value,
  t.uint64_value,
  t.sint32_value,
  t.sint64_value,
  t.fixed32_value,
  t.fixed64_value,
  t.sfixed32_value,
  t.sfixed64_value,
  t.string_value,
  t.bytes_value
)AS R(value);