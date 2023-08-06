from greyai_sdk.dataset import DatasetType
from pydantic import BaseModel
from abc import ABC, abstractmethod
from tensorflow import data


class Model(ABC):
    def __init__(self, strategy=None, weights_file=None):
        self.model = None
        self.weights_file = weights_file
        self.strategy = strategy

    @abstractmethod
    def predict(self, dataset: data.Dataset) -> BaseModel:
        pass

    @abstractmethod
    def train(self, dataset: data.Dataset) -> str:
        pass

    @abstractmethod
    def customizable(self) -> bool:
        pass

    @abstractmethod
    def accepts_input(self) -> DatasetType:
        pass

