from concurrent import futures
import grpc

from proto import scalar_optional_pb2
from proto import scalar_optional_pb2_grpc


FIELD_SPECS = [
    ("double_value", float),
    ("float_value", float),
    ("int32_value", int),
    ("int64_value", int),
    ("uint32_value", int),
    ("uint64_value", int),
    ("sint32_value", int),
    ("sint64_value", int),
    ("fixed32_value", int),
    ("fixed64_value", int),
    ("sfixed32_value", int),
    ("sfixed64_value", int),
    ("string_value", str),
    ("bytes_value", bytes),
]

NUMERIC_FIELDS = [
    "double_value",
    "float_value",
    "int32_value",
    "int64_value",
    "uint32_value",
    "uint64_value",
    "sint32_value",
    "sint64_value",
    "fixed32_value",
    "fixed64_value",
    "sfixed32_value",
    "sfixed64_value",
]


class ScalarOptionalTestServicer(scalar_optional_pb2_grpc.ScalarOptionalTestServicer):
    def optional_all(self, request, context):
        response = scalar_optional_pb2.OptionalScalarResponse()

        print("[server] received request")
        missing = []
        parts = []

        for name, _ in FIELD_SPECS:
            has_value = request.HasField(name)
            value = getattr(request, name)
            parts.append(f"{name}(has={has_value}, val={value!r})")
            if not has_value:
                missing.append(name)

        print("[server] " + " | ".join(parts))

        if missing:
            print(f"[server] NULL detected: {missing} -> result=NULL")
            return response

        total = sum(getattr(request, name) for name in NUMERIC_FIELDS)

        response.result = float(total)
        print(f"[server] result={response.result}")
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    scalar_optional_pb2_grpc.add_ScalarOptionalTestServicer_to_server(
        ScalarOptionalTestServicer(), server
    )
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("[server] listening on 127.0.0.1:50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
