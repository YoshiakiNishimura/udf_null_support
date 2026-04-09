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

    def optional_decimal(self, request, context):
        response = scalar_optional_pb2.OptionalDecimal()

        print("[server] received optional_decimal request")

        fields = [
            "decimal_value",
            "date_value",
            "localtime_value",
            "localdatetime_value",
            "offsetdatatime_value",
        ]

        missing = []
        for name in fields:
            has_value = request.HasField(name)
            print(f"[server] {name}(has={has_value})")
            if not has_value:
                missing.append(name)

        if missing:
            print(f"[server] NULL detected: {missing} -> result=NULL")
            return response

        dec = request.decimal_value
        print(
            "[server] decimal: "
            f"unscaled_value={dec.unscaled_value!r}, exponent={dec.exponent}"
        )

        response.decimal_value.unscaled_value = dec.unscaled_value
        response.decimal_value.exponent = dec.exponent

        response.date_value.days = request.date_value.days

        response.localtime_value.nanos = request.localtime_value.nanos

        response.localdatetime_value.offset_seconds = (
            request.localdatetime_value.offset_seconds
        )
        response.localdatetime_value.nano_adjustment = (
            request.localdatetime_value.nano_adjustment
        )

        response.offsetdatatime_value.offset_seconds = (
            request.offsetdatatime_value.offset_seconds
        )
        response.offsetdatatime_value.nano_adjustment = (
            request.offsetdatatime_value.nano_adjustment
        )
        response.offsetdatatime_value.time_zone_offset = (
            request.offsetdatatime_value.time_zone_offset
        )

        print(
            "[server] response decimal: "
            f"unscaled_value={response.decimal_value.unscaled_value!r}, "
            f"exponent={response.decimal_value.exponent}"
        )
        print(f"[server] response date.days={response.date_value.days}")
        print(f"[server] response localtime.nanos={response.localtime_value.nanos}")
        print(
            "[server] response localdatetime: "
            f"offset_seconds={response.localdatetime_value.offset_seconds}, "
            f"nano_adjustment={response.localdatetime_value.nano_adjustment}"
        )
        print(
            "[server] response offsetdatetime: "
            f"offset_seconds={response.offsetdatatime_value.offset_seconds}, "
            f"nano_adjustment={response.offsetdatatime_value.nano_adjustment}, "
            f"time_zone_offset={response.offsetdatatime_value.time_zone_offset}"
        )

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
