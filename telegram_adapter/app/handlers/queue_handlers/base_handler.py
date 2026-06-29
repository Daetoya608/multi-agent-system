from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T_DTO = TypeVar('T_DTO')

class BaseQueueHandler(ABC, Generic[T_DTO]):
    @abstractmethod
    async def handle(self, dto: T_DTO) -> None:
        """Каждая команда из очереди должна реализовать этот метод"""
        pass
