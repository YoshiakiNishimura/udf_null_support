from concurrent import futures
import grpc

from proto import null_pb2
from proto import null_pb2_grpc


class CalculatorServicer(null_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        response = null_pb2.AddResponse()

        has_a = request.HasField("a")
        has_b = request.HasField("b")

        print(f"[server] has_a={has_a}, has_b={has_b}")

        if not has_a or not has_b:
            print("[server] one or more args are NULL -> result=NULL")
            return response

        value = request.a + request.b
        response.result = value
        print(f"[server] result={value}")
        return response


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    null_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)

    listen_addr = "127.0.0.1:50051"
    server.add_insecure_port(listen_addr)
    server.start()

    print(f"[server] listening on {listen_addr}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
