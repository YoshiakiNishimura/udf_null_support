#!/bin/bash
# shfmt -w
BASE_DIR="${HOME}/grpc"
python3 -m grpc_tools.protoc \
	-I. \
	--python_out=. \
	--grpc_python_out=. \
	proto/scalar_optional.proto
udf-plugin-builder --proto proto/scalar_optional.proto --clean --debug --output-dir "${BASE_DIR}"
# rm -r tmp
