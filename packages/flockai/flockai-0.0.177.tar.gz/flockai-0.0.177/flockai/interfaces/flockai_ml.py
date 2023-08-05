import abc


class FlockAIClassifier(abc.ABC):
    def __init__(self):
        self.model = None

    @abc.abstractmethod
    def load_model(self):
        raise NotImplementedError

    @abc.abstractmethod
    def predict(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_model_input(self):
        raise NotImplementedError
