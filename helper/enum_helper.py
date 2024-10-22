from enum import Enum


class MLModelsEnum(int, Enum):
    LINEAR_REGRESSION = 1
    NEURAL_NETWORK = 2

class FillingMethodEnum(int, Enum):
    MIN = 1
    MAX = 2
    MEAN = 3
    MEDIAN = 4
    MODE = 5
    RECOMENDATION = 6