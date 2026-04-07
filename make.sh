#!/bin/bash
# shfmt -w
python3 -m grpc_tools.protoc \
	-I. \
	--python_out=. \
	--grpc_python_out=. \
	proto/null.proto

#udf-plugin-builder  --proto proto/null.proto --clean
