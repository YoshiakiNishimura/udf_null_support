from concurrent import futures
import grpc

from proto import scalar_optional_pb2
from proto import scalar_optional_pb2_grpc


FIELDS = [
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
    "sfixed64_value"
]


class ScalarOptionalTestServicer(scalar_optional_pb2_grpc.ScalarOptionalTestServicer):
    def optional_all(self, request, context):
        response = scalar_optional_pb2.OptionalScalarResponse()

        print("[server] received request")
        missing = []

        for name in FIELDS:
            has_value = request.HasField(name)
            value = getattr(request, name)
            print(f"[server] {name}: has={has_value}, value={value}")
            if not has_value:
                missing.append(name)

        if missing:
            print(f"[server] NULL detected: {missing} -> result=NULL")
            return response

        # 全部セットされている場合は動作確認用に適当に合計
        total = (
            request.double_value
            + request.float_value
            + request.int32_value
            + request.int64_value
            + request.uint32_value
            + request.uint64_value
            + request.sint32_value
            + request.sint64_value
            + request.fixed32_value
            + request.fixed64_value
            + request.sfixed32_value
            + request.sfixed64_value
        )

        response.result = float(total)
        print(f"[server] result={response.result}")
        return response


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    scalar_optional_pb2_grpc.add_ScalarOptionalTestServicer_to_server(
        ScalarOptionalTestServicer(), server
    )

    listen_addr = "127.0.0.1:50051"
    server.add_insecure_port(listen_addr)
    server.start()

    print(f"[server] listening on {listen_addr}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()