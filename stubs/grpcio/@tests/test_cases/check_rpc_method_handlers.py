from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
from typing_extensions import assert_type

import grpc


def sync_unary(request: str, context: grpc.ServicerContext) -> str:
    return request


async def async_unary(request: str, context: grpc.aio.ServicerContext[str, str]) -> str:
    return request


async def async_unary_stream(request: str, context: grpc.aio.ServicerContext[str, str]) -> AsyncIterator[str]:
    yield request


async def async_stream_unary(requests: AsyncIterator[str], context: grpc.aio.ServicerContext[str, str]) -> str:
    return await anext(requests)


async def async_stream_stream(requests: AsyncIterator[str], context: grpc.aio.ServicerContext[str, str]) -> AsyncIterator[str]:
    async for request in requests:
        yield request


async def async_write(request: str, context: grpc.aio.ServicerContext[str, str]) -> None:
    await context.write(request)


async def async_stream_write(requests: AsyncIterator[str], context: grpc.aio.ServicerContext[str, str]) -> None:
    async for request in requests:
        await context.write(request)


def sync_stream(requests: Iterator[str], context: grpc.ServicerContext) -> Iterator[str]:
    return requests


assert_type(grpc.unary_unary_rpc_method_handler(sync_unary, bytes.decode, str.encode), grpc.RpcMethodHandler[str, str])
assert_type(grpc.stream_stream_rpc_method_handler(sync_stream, bytes.decode, str.encode), grpc.RpcMethodHandler[str, str])
assert_type(grpc.unary_unary_rpc_method_handler(async_unary), grpc.aio._AsyncRpcMethodHandler[str, str])
assert_type(grpc.unary_stream_rpc_method_handler(async_unary_stream), grpc.aio._AsyncRpcMethodHandler[str, str])
assert_type(grpc.stream_unary_rpc_method_handler(async_stream_unary), grpc.aio._AsyncRpcMethodHandler[str, str])
assert_type(grpc.stream_stream_rpc_method_handler(async_stream_stream), grpc.aio._AsyncRpcMethodHandler[str, str])
assert_type(grpc.unary_stream_rpc_method_handler(async_write), grpc.aio._AsyncRpcMethodHandler[str, str])
assert_type(grpc.stream_stream_rpc_method_handler(async_stream_write), grpc.aio._AsyncRpcMethodHandler[str, str])

sync_handlers = {"Check": grpc.unary_unary_rpc_method_handler(sync_unary, bytes.decode, str.encode)}
grpc.method_handlers_generic_handler("test.Sync", sync_handlers)
async_handlers = {"Check": grpc.unary_unary_rpc_method_handler(async_unary)}
grpc.method_handlers_generic_handler("test.Async", async_handlers)


# The synchronous fallback must still accept the callback-based streaming API.
def nonblocking_watch(request: str, context: grpc.ServicerContext, send_response_callback: object) -> None:
    pass


assert_type(grpc.unary_stream_rpc_method_handler(nonblocking_watch, bytes.decode, str.encode), grpc.RpcMethodHandler[str, str])
