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

OPTIONAL_DECIMAL_FIELDS = [
    "decimal_value",
    "date_value",
    "localtime_value",
    "localdatetime_value",
    "offsetdatatime_value",
    "blob_value",
    "clob_value",
]


class ScalarOptionalTestServicer(scalar_optional_pb2_grpc.ScalarOptionalTestServicer):
    @staticmethod
    def _collect_missing_fields(request, fields):
        missing = []
        for name in fields:
            has_value = request.HasField(name)
            print(f"[server] {name}(has={has_value})")
            if not has_value:
                missing.append(name)
        return missing

    @staticmethod
    def _print_optional_all_request(request):
        parts = []
        for name, _ in FIELD_SPECS:
            has_value = request.HasField(name)
            value = getattr(request, name)
            parts.append(f"{name}(has={has_value}, val={value!r})")
        print("[server] " + " | ".join(parts))

    @staticmethod
    def _print_optional_decimal_request(request):
        if request.HasField("decimal_value"):
            print(
                "[server] request decimal: "
                f"unscaled_value={request.decimal_value.unscaled_value!r}, "
                f"exponent={request.decimal_value.exponent}"
            )
        if request.HasField("date_value"):
            print(f"[server] request date.days={request.date_value.days}")
        if request.HasField("localtime_value"):
            print(f"[server] request localtime.nanos={request.localtime_value.nanos}")
        if request.HasField("localdatetime_value"):
            print(
                "[server] request localdatetime: "
                f"offset_seconds={request.localdatetime_value.offset_seconds}, "
                f"nano_adjustment={request.localdatetime_value.nano_adjustment}"
            )
        if request.HasField("offsetdatatime_value"):
            print(
                "[server] request offsetdatetime: "
                f"offset_seconds={request.offsetdatatime_value.offset_seconds}, "
                f"nano_adjustment={request.offsetdatatime_value.nano_adjustment}, "
                f"time_zone_offset={request.offsetdatatime_value.time_zone_offset}"
            )
        if request.HasField("blob_value"):
            print(
                "[server] request blob: "
                f"storage_id={request.blob_value.storage_id}, "
                f"object_id={request.blob_value.object_id}, "
                f"tag={request.blob_value.tag}, "
                f"provisioned={request.blob_value.provisioned}"
            )
        if request.HasField("clob_value"):
            print(
                "[server] request clob: "
                f"storage_id={request.clob_value.storage_id}, "
                f"object_id={request.clob_value.object_id}, "
                f"tag={request.clob_value.tag}, "
                f"provisioned={request.clob_value.provisioned}"
            )

    @staticmethod
    def _print_optional_decimal_response(response):
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
        print(
            "[server] response blob: "
            f"storage_id={response.blob_value.storage_id}, "
            f"object_id={response.blob_value.object_id}, "
            f"tag={response.blob_value.tag}, "
            f"provisioned={response.blob_value.provisioned}"
        )
        print(
            "[server] response clob: "
            f"storage_id={response.clob_value.storage_id}, "
            f"object_id={response.clob_value.object_id}, "
            f"tag={response.clob_value.tag}, "
            f"provisioned={response.clob_value.provisioned}"
        )

    def optional_all(self, request, context):
        response = scalar_optional_pb2.OptionalScalarResponse()

        print("[server] received optional_all request")
        self._print_optional_all_request(request)

        missing = []
        for name, _ in FIELD_SPECS:
            if not request.HasField(name):
                missing.append(name)

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
        missing = self._collect_missing_fields(request, OPTIONAL_DECIMAL_FIELDS)
        self._print_optional_decimal_request(request)

        if missing:
            print(f"[server] NULL detected: {missing} -> result=NULL")
            return response

        response.CopyFrom(request)
        self._print_optional_decimal_response(response)
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
