from typing import Generic, TypeVar

InputData = TypeVar("InputData")
OutputData = TypeVar("OutputData")


class Interactor(Generic[InputData, OutputData]):
    def __call__(self, data: InputData) -> OutputData:
        raise NotADirectoryError