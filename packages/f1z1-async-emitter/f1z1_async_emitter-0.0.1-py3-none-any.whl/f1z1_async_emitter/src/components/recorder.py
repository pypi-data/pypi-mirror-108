# @Time     : 2021/6/4
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from itertools import chain

from .base import IEmitRecorder


class EmitRecorder(IEmitRecorder):

    def __init__(self):
        self._results = []

    @property
    def length(self):
        return len(self._results)

    def empty(self):
        return not self.length

    def save(self, result):
        self._results.append(result)

    def __iter__(self):
        if not self.empty():
            for _, result in enumerate(self._results):
                yield result


class EmitRecorderChain(IEmitRecorder):

    def __init__(self):
        self._results = EmitRecorder()

    def save(self, result: IEmitRecorder):
        if not self._is_recoder(result):
            return
        self._results.save(result)

    def __iter__(self):
        return chain(*self._results)

    def _is_recoder(self, value):
        return isinstance(value, IEmitRecorder)
