#!/bin/bash
# shfmt -w
set -eu

echo '=== setup ==='
tgsql -c ipc:tsurugi --script sql/setup.sql

tsurugi_scalar_no_optional_stream() {
	echo "=== tsurugi_scalar_no_optional_stream ==="
	tgsql -c ipc:tsurugi --script sql/tsurugi_scalar_no_optional_stream/10_insert_ok.sql
	tgsql -c ipc:tsurugi --script sql/tsurugi_scalar_no_optional_stream/00_select.sql
}
#tsurugi_scalar_no_optional_stream
tsurugi_scalar_optional_stream() {
	echo "=== tsurugi_scalar_optional_stream ==="
	for f in sql/tsurugi_scalar_optional_stream/[1-2][0-9]_insert_*.sql; do
		tgsql -c ipc:tsurugi --script "$f"
		tgsql -c ipc:tsurugi --script sql/tsurugi_scalar_optional_stream/00_select.sql
	done
}
#tsurugi_scalar_optional_stream
tsurugi_scalar_optional() {
	echo "=== tsurugi_scalar_optional ==="
	for f in sql/tsurugi_scalar_optional/[1-2][0-9]_insert_*.sql; do
		tgsql -c ipc:tsurugi --script "$f"
		tgsql -c ipc:tsurugi --script sql/tsurugi_scalar_optional/00_select.sql
	done
}
#tsurugi_scalar_optional
tsurugi_types_optional() {
	echo "=== tsurugi_types_optional ==="
	for f in sql/tsurugi_types_optional/[1-2][0-9]_insert_*.sql; do
		tgsql -c ipc:tsurugi --script "$f"
		tgsql -c ipc:tsurugi --script sql/tsurugi_types_optional/00_select.sql
	done
}
#tsurugi_types_optional
tsurugi_types_optional_stream() {
	echo "=== tsurugi_types_optional_stream ==="
	for f in sql/tsurugi_types_optional_stream/[1-2][0-9]_insert_*.sql; do
		tgsql -c ipc:tsurugi --script "$f"
		tgsql -c ipc:tsurugi --script sql/tsurugi_types_optional_stream/00_select.sql
	done
}
tsurugi_types_optional_stream
#echo '=== optional_decimal ==='
#for f in sql/optional_decimal/[1-2][0-9]_insert_*.sql; do
#	echo "=== RUN: $f ==="
#	tgsql -c ipc:tsurugi --script "$f"
#	tgsql -c ipc:tsurugi --script sql/optional_decimal/00_select.sql
#done
echo '=== optional_decimal_stream ==='
#for f in sql/optional_decimal_stream/[1-2][0-9]_insert_*.sql; do
#	echo "=== RUN: $f ==="
#	tgsql -c ipc:tsurugi --script "$f"
#	tgsql -c ipc:tsurugi --script sql/optional_decimal_stream/00_select.sql
#done

echo '=== optional_all ==='
#cat sql/optional_all/27_insert_multi_null_3.sql
#for f in sql/optional_all/27_insert_multi_null_3.sql; do
#	echo "=== RUN: $f ==="
#	tgsql -c ipc:tsurugi --script "$f"
#	tgsql -c ipc:tsurugi --script sql/optional_all/00_select.sql
#done
