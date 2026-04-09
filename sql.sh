#!/bin/bash
# shfmt -w
set -eu

echo '=== setup ==='
tgsql -c ipc:tsurugi --script sql/setup.sql

echo '=== optional_decimal ==='
for f in sql/optional_decimal/[1-2][0-9]_insert_*.sql; do
	echo "=== RUN: $f ==="
	tgsql -c ipc:tsurugi --script "$f"
	tgsql -c ipc:tsurugi --script sql/optional_decimal/00_select.sql
done

echo '=== optional_all ==='
for f in sql/optional_all/[1-2][0-9]_insert_*.sql; do
	echo "=== RUN: $f ==="
	tgsql -c ipc:tsurugi --script "$f"
	tgsql -c ipc:tsurugi --script sql/optional_all/00_select.sql
done
