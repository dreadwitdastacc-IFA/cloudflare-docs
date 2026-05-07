from dataclasses import dataclass
from typing import Any, Callable, Dict, List


@dataclass
class AMFEvent:
    source: str
    topic: str
    payload: Dict[str, Any]


class AMFRouter:
    """Simple Application Messaging Framework for Sentinel Apex."""

    def __init__(self):
        self.handlers: Dict[str, List[Callable[[AMFEvent], Any]]] = {}

    def subscribe(self, topic: str, handler: Callable[[AMFEvent], Any]) -> None:
        if topic not in self.handlers:
            self.handlers[topic] = []
        self.handlers[topic].append(handler)

    def publish(self, event: AMFEvent) -> None:
        handlers = self.handlers.get(event.topic, [])
        for handler in handlers:
            handler(event)

    def clear(self) -> None:
        self.handlers.clear()


class SentinelMessage:
    def __init__(self, event: AMFEvent):
        self.event = event

    def route(self) -> str:
        return f"sentinel.{self.event.topic}"


class GatewayMessage:
    def __init__(self, event: AMFEvent):
        self.event = event

    def route(self) -> str:
        return f"gateway.{self.event.topic}"


class BitcoinMessage:
    def __init__(self, event: AMFEvent):
        self.event = event

    def route(self) -> str:
        return f"bitcoin.{self.event.topic}"
