#!/usr/bin/env python3
from concurrent import futures
import time
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

TSURUGI_TYPES_FIELDS = [
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
    def _format_scalar_value(value):
        return repr(value)

    @classmethod
    def _print_field_block(cls, title, rows):
        print(f"[server] {title}:", flush=True)
        for name, status, detail in rows:
            if detail:
                print(f"[server]   {name:<18} : {status:<4} {detail}", flush=True)
            else:
                print(f"[server]   {name:<18} : {status}", flush=True)

    @classmethod
    def _print_tsurugi_scalar_optional_request(cls, request):
        rows = []
        for name, _ in FIELD_SPECS:
            has_value = request.HasField(name)
            if has_value:
                value = getattr(request, name)
                rows.append((name, "SET", f"value={cls._format_scalar_value(value)}"))
            else:
                rows.append((name, "NULL", ""))
        cls._print_field_block("tsurugi_scalar_optional fields", rows)

    @classmethod
    def _collect_missing_fields(cls, request, fields):
        rows = []
        missing = []
        for name in fields:
            has_value = request.HasField(name)
            if has_value:
                rows.append((name, "SET", ""))
            else:
                rows.append((name, "NULL", ""))
                missing.append(name)
        cls._print_field_block("tsurugi_types_optional field presence", rows)
        return missing

    @classmethod
    def _print_tsurugi_types_optional_request(cls, request):
        rows = []
        if request.HasField("decimal_value"):
            rows.append(
                (
                    "decimal_value",
                    "SET",
                    f"unscaled_value={request.decimal_value.unscaled_value!r}, exponent={request.decimal_value.exponent}",
                )
            )
        else:
            rows.append(("decimal_value", "NULL", ""))

        if request.HasField("date_value"):
            rows.append(("date_value", "SET", f"days={request.date_value.days}"))
        else:
            rows.append(("date_value", "NULL", ""))

        if request.HasField("localtime_value"):
            rows.append(
                ("localtime_value", "SET", f"nanos={request.localtime_value.nanos}")
            )
        else:
            rows.append(("localtime_value", "NULL", ""))

        if request.HasField("localdatetime_value"):
            rows.append(
                (
                    "localdatetime_value",
                    "SET",
                    f"offset_seconds={request.localdatetime_value.offset_seconds}, nano_adjustment={request.localdatetime_value.nano_adjustment}",
                )
            )
        else:
            rows.append(("localdatetime_value", "NULL", ""))

        if request.HasField("offsetdatatime_value"):
            rows.append(
                (
                    "offsetdatatime_value",
                    "SET",
                    f"offset_seconds={request.offsetdatatime_value.offset_seconds}, nano_adjustment={request.offsetdatatime_value.nano_adjustment}, time_zone_offset={request.offsetdatatime_value.time_zone_offset}",
                )
            )
        else:
            rows.append(("offsetdatatime_value", "NULL", ""))

        if request.HasField("blob_value"):
            rows.append(
                (
                    "blob_value",
                    "SET",
                    f"storage_id={request.blob_value.storage_id}, object_id={request.blob_value.object_id}, tag={request.blob_value.tag}, provisioned={request.blob_value.provisioned}",
                )
            )
        else:
            rows.append(("blob_value", "NULL", ""))

        if request.HasField("clob_value"):
            rows.append(
                (
                    "clob_value",
                    "SET",
                    f"storage_id={request.clob_value.storage_id}, object_id={request.clob_value.object_id}, tag={request.clob_value.tag}, provisioned={request.clob_value.provisioned}",
                )
            )
        else:
            rows.append(("clob_value", "NULL", ""))

        cls._print_field_block("tsurugi_types_optional payload", rows)

    @classmethod
    def _print_tsurugi_types_optional_response(
        cls, response, prefix="tsurugi_types_optional response"
    ):
        rows = []
        if response.HasField("decimal_value"):
            rows.append(
                (
                    "decimal_value",
                    "SET",
                    f"unscaled_value={response.decimal_value.unscaled_value!r}, exponent={response.decimal_value.exponent}",
                )
            )
        else:
            rows.append(("decimal_value", "NULL", ""))

        if response.HasField("date_value"):
            rows.append(("date_value", "SET", f"days={response.date_value.days}"))
        else:
            rows.append(("date_value", "NULL", ""))

        if response.HasField("localtime_value"):
            rows.append(
                ("localtime_value", "SET", f"nanos={response.localtime_value.nanos}")
            )
        else:
            rows.append(("localtime_value", "NULL", ""))

        if response.HasField("localdatetime_value"):
            rows.append(
                (
                    "localdatetime_value",
                    "SET",
                    f"offset_seconds={response.localdatetime_value.offset_seconds}, nano_adjustment={response.localdatetime_value.nano_adjustment}",
                )
            )
        else:
            rows.append(("localdatetime_value", "NULL", ""))

        if response.HasField("offsetdatatime_value"):
            rows.append(
                (
                    "offsetdatatime_value",
                    "SET",
                    f"offset_seconds={response.offsetdatatime_value.offset_seconds}, nano_adjustment={response.offsetdatatime_value.nano_adjustment}, time_zone_offset={response.offsetdatatime_value.time_zone_offset}",
                )
            )
        else:
            rows.append(("offsetdatatime_value", "NULL", ""))

        if response.HasField("blob_value"):
            rows.append(
                (
                    "blob_value",
                    "SET",
                    f"storage_id={response.blob_value.storage_id}, object_id={response.blob_value.object_id}, tag={response.blob_value.tag}, provisioned={response.blob_value.provisioned}",
                )
            )
        else:
            rows.append(("blob_value", "NULL", ""))

        if response.HasField("clob_value"):
            rows.append(
                (
                    "clob_value",
                    "SET",
                    f"storage_id={response.clob_value.storage_id}, object_id={response.clob_value.object_id}, tag={response.clob_value.tag}, provisioned={response.clob_value.provisioned}",
                )
            )
        else:
            rows.append(("clob_value", "NULL", ""))

        cls._print_field_block(prefix, rows)

    def tsurugi_scalar_optional(self, request, context):
        response = scalar_optional_pb2.OptionalScalarResponse()
        print("[server] received tsurugi_scalar_optional request", flush=True)
        self._print_tsurugi_scalar_optional_request(request)

        missing = [name for name, _ in FIELD_SPECS if not request.HasField(name)]
        if missing:
            print(f"[server] result=NULL (missing: {', '.join(missing)})", flush=True)
            return response

        total = sum(getattr(request, name) for name in NUMERIC_FIELDS)
        response.result = float(total)
        print(f"[server] result={response.result}", flush=True)
        return response

    def tsurugi_types_optional(self, request, context):
        response = scalar_optional_pb2.OptionalDecimal()
        print("[server] received tsurugi_types_optional request", flush=True)
        missing = self._collect_missing_fields(request, TSURUGI_TYPES_FIELDS)
        self._print_tsurugi_types_optional_request(request)

        if missing:
            print(f"[server] result=NULL (missing: {', '.join(missing)})", flush=True)
            return response

        response.CopyFrom(request)
        self._print_tsurugi_types_optional_response(response)
        return response

    def tsurugi_scalar_optional_stream(self, request, context):
        print("[server] received tsurugi_scalar_optional_stream request", flush=True)
        self._print_tsurugi_scalar_optional_request(request)

        missing = [name for name, _ in FIELD_SPECS if not request.HasField(name)]
        if missing:
            print(
                f"[server] stream terminated (missing: {', '.join(missing)})",
                flush=True,
            )
            return

        base = float(sum(getattr(request, name) for name in NUMERIC_FIELDS))
        for i in range(5):
            response = scalar_optional_pb2.OptionalScalarResponse(result=base + i)
            print(f"[server] stream[{i}] result={response.result}", flush=True)
            yield response
            time.sleep(0.05)

    def tsurugi_types_optional_stream(self, request, context):
        print("[server] received tsurugi_types_optional_stream request", flush=True)
        missing = self._collect_missing_fields(request, TSURUGI_TYPES_FIELDS)
        self._print_tsurugi_types_optional_request(request)

        if missing:
            print(
                f"[server] stream terminated (missing: {', '.join(missing)})",
                flush=True,
            )
            return

        for i in range(3):
            response = scalar_optional_pb2.OptionalDecimal()
            response.CopyFrom(request)
            response.decimal_value.exponent += i
            response.date_value.days += i
            response.localtime_value.nanos += i
            response.localdatetime_value.offset_seconds += i
            response.localdatetime_value.nano_adjustment += i
            response.offsetdatatime_value.offset_seconds += i
            response.offsetdatatime_value.nano_adjustment += i
            response.offsetdatatime_value.time_zone_offset += i
            self._print_tsurugi_types_optional_response(
                response, prefix=f"tsurugi_types_optional_stream[{i}]"
            )
            yield response
            time.sleep(0.05)

    def _print_all_tsurugi_request(self, request):
        rows = [
            (
                "decimal_value",
                "SET",
                f"unscaled_value={request.decimal_value.unscaled_value!r}, exponent={request.decimal_value.exponent}",
            ),
            ("date_value", "SET", f"days={request.date_value.days}"),
            ("localtime_value", "SET", f"nanos={request.localtime_value.nanos}"),
            (
                "localdatetime_value",
                "SET",
                f"offset_seconds={request.localdatetime_value.offset_seconds}, "
                f"nano_adjustment={request.localdatetime_value.nano_adjustment}",
            ),
            (
                "offsetdatatime_value",
                "SET",
                f"offset_seconds={request.offsetdatatime_value.offset_seconds}, "
                f"nano_adjustment={request.offsetdatatime_value.nano_adjustment}, "
                f"time_zone_offset={request.offsetdatatime_value.time_zone_offset}",
            ),
            (
                "blob_value",
                "SET",
                f"storage_id={request.blob_value.storage_id}, "
                f"object_id={request.blob_value.object_id}, "
                f"tag={request.blob_value.tag}, "
                f"provisioned={request.blob_value.provisioned}",
            ),
            (
                "clob_value",
                "SET",
                f"storage_id={request.clob_value.storage_id}, "
                f"object_id={request.clob_value.object_id}, "
                f"tag={request.clob_value.tag}, "
                f"provisioned={request.clob_value.provisioned}",
            ),
        ]
        self._print_field_block("all_tsurugi payload", rows)

    def tsurugi_scalar_no_optional_stream(self, request, context):
        print("[server] received tsurugi_scalar_no_optional_stream request", flush=True)
        print(f"[server]   double_value : {request.double_value}", flush=True)
        print(f"[server]   float_value  : {request.float_value}", flush=True)
        print(f"[server]   int32_value  : {request.int32_value}", flush=True)
        print(f"[server]   int64_value  : {request.int64_value}", flush=True)
        print(f"[server]   uint32_value : {request.uint32_value}", flush=True)
        print(f"[server]   uint64_value : {request.uint64_value}", flush=True)
        print(f"[server]   sint32_value : {request.sint32_value}", flush=True)
        print(f"[server]   sint64_value : {request.sint64_value}", flush=True)
        print(f"[server]   fixed32_value: {request.fixed32_value}", flush=True)
        print(f"[server]   fixed64_value: {request.fixed64_value}", flush=True)
        print(f"[server]   sfixed32_value: {request.sfixed32_value}", flush=True)
        print(f"[server]   sfixed64_value: {request.sfixed64_value}", flush=True)
        print(f"[server]   string_value : {request.string_value!r}", flush=True)
        print(f"[server]   bytes_value  : {request.bytes_value!r}", flush=True)

        base = float(
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

        for i in range(5):
            response = scalar_optional_pb2.ScalarResponse(result=base + i)
            print(f"[server] stream[{i}] result={response.result}", flush=True)
            yield response
            time.sleep(0.05)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    scalar_optional_pb2_grpc.add_ScalarOptionalTestServicer_to_server(
        ScalarOptionalTestServicer(), server
    )
    server.add_insecure_port("127.0.0.1:50051")
    server.start()
    print("[server] listening on 127.0.0.1:50051", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
