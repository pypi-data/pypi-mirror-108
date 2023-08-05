from typing import Iterable, List, Optional
from collections.abc import Iterator


class IteratorAccelerator(Iterator):
  def __init__(
    self,
    iterable: Iterable,
    buffer_size: int
  ) -> None:
    self._iterator: Optional[Iterator[bytes]] = iter(iterable)
    self._buffer_size = buffer_size

  def __iter__(self) -> Iterator[bytes]:
    return self

  def __next__(self) -> bytes:
    if self._iterator is None:
      raise StopIteration
    buffer: List[bytes] = []
    buffer_size = 0
    while buffer_size < self._buffer_size:
      block = next(self._iterator, None)
      if block is None:
        self._iterator = None
        if len(buffer) == 0:
          raise StopIteration
        break
      buffer.append(block)
      buffer_size += len(block)

    return b''.join(buffer)