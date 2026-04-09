#!/bin/bash
# shfmt -w
(
	cd proto
	rm scalar_optional_pb2_grpc.py scalar_optional_pb2.py
)
TSURUGI_PROTO=${HOME}/git/tsurugi-udf/proto
BASE_DIR="${HOME}/grpc"
python3 -m grpc_tools.protoc \
	-I. -I ${TSURUGI_PROTO} \
	--python_out=. \
	--grpc_python_out=. \
	proto/scalar_optional.proto
udf-plugin-builder --proto proto/scalar_optional.proto \
	-I . -I ${TSURUGI_PROTO} \
	--clean --debug --output-dir "${BASE_DIR}"
# rm -r tmp
