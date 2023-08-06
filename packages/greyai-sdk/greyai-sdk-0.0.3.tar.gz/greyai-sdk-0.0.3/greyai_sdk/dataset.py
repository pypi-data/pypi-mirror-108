from enum import Enum


class DatasetBuilder:
    def __init__(self):
        pass


class DatasetType:
    def __init__(self, value, orred_type=None):
        self.child_type = type(self)
        self._value = value
        self.orred_type = orred_type

    def __and__(self, other):
        if isinstance(other, DatasetType):
            if self.child_type != DatasetType and isinstance(other, self.child_type):
                return DatasetType(self.value | other.value, self.child_type)
            elif isinstance(other, self.orred_type):
                return DatasetType(self._value | other.value, self.orred_type)
        if self.child_type == DatasetType:
            raise Exception(f'{other} isn\'t {self.orred_type.__name__}')
        else:
            raise Exception(f'{other} isn\'t {self.child_type.__name__}')

    @staticmethod
    def _set_k_bit(n, k):
        return (1 << k) | n

    def split(self):
        values = []
        if self.child_type != DatasetType:
            # pure type, not orred
            values.append(self.child_type(self._value))
        else:
            mtype = self.orred_type
            count = 0
            value = self._value
            bit = 0
            while value:
                if value & 1:
                    values.append(mtype(self._set_k_bit(0, bit)))
                value >>= 1
                bit += 1
        return values


class DatasetTypeImage(DatasetType, Enum):
    # do not change the values or reorder
    # values are exponential to perform and op
    # new values will be added, values will never be deleted even after
    # deprecation, model creator shows deprecation of datatypes in such cases
    IMAGE_WITH_LABELS = 1
    IMAGE_WITH_LABELED_BBS = 2
    IMAGE_WITH_BBS = 4
    IMAGE_WITH_SUMMARY = 8


class DatasetTypeAudio(DatasetType, Enum):
    # do not change the values or reorder
    # values are exponential to perform and op
    # new values will be added, values will never be deleted even after
    # deprecation, model creator shows deprecation of datatypes in such cases
    AUDIO_WITH_TRANSCRIPTION = 1
    AUDIO_WITH_LABELS = 2
    AUDIO_WITH_TIME_SPANNED_LABELS = 4


class DatasetTypeText(DatasetType, Enum):
    # do not change the values or reorder
    # values are exponential to perform and op
    # new values will be added, values will never be deleted even after
    # deprecation, model creator shows deprecation of datatypes in such cases
    TEXT_RAW = 1
    TEXT_WITH_NE = 2
    TEXT_WITH_LABELS = 4


class DatasetTypeTranslation(DatasetType, Enum):
    # do not change the values or reorder
    # values are exponential to perform and op
    # new values will be added, values will never be deleted even after
    # deprecation, model creator shows deprecation of datatypes in such cases
    TRANSLATION_TEXT = 1
    TRANSLATION_AUDIO = 2

