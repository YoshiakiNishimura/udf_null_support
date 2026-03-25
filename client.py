import grpc


from proto import null_pb2
from proto import null_pb2_grpc


def call_add(
    stub, a_set: bool, b_set: bool, a_value: int = 0, b_value: int = 0
) -> None:
    req = null_pb2.AddRequest()

    if a_set:
        req.a = a_value
    if b_set:
        req.b = b_value

    print("----")
    print(
        f"[client] send:"
        f" has_a={req.HasField('a')}"
        f" has_b={req.HasField('b')}"
        f" a={req.a if req.HasField('a') else 'NULL'}"
        f" b={req.b if req.HasField('b') else 'NULL'}"
    )

    res = stub.Add(req)

    if res.HasField("result"):
        print(f"[client] result={res.result}")
    else:
        print("[client] result=NULL")


def main() -> None:
    with grpc.insecure_channel("127.0.0.1:50051") as channel:
        stub = null_pb2_grpc.CalculatorStub(channel)

        call_add(stub, a_set=True, b_set=True, a_value=10, b_value=20)
        call_add(stub, a_set=False, b_set=True, b_value=20)
        call_add(stub, a_set=True, b_set=False, a_value=10)
        call_add(stub, a_set=False, b_set=False)
        call_add(stub, a_set=True, b_set=True, a_value=0, b_value=5)


if __name__ == "__main__":
    main()
