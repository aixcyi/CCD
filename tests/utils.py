import sys
from datetime import timedelta, datetime
from functools import wraps


def delta2hms(delta: timedelta) -> tuple:
    h = delta.seconds // 3600
    m = delta.seconds % 3600 // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return h, m, s


def delta2ms(delta: timedelta) -> tuple:
    m = delta.seconds // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return m, s


class BearTimer(object):
    def __init__(self, title: str = None):
        self._mark = None
        self._point = None
        self._title = title if title else sys._getframe().f_back.f_code.co_name

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.stop()

    def _print(self, note=''):
        now = datetime.now()
        head = now.strftime('%H:%M:%S.%f')
        if self._point:
            m, s = delta2ms(now - self._point)
        else:
            m, s = 0, 0
        print(f'{head}, {m:d}:{s:f}, {self._title} | {note}')

    def start(self):
        if self._point is not None:
            raise RuntimeError('计时还未结束。')
        self._print('Starting...')
        self._point = datetime.now()
        return self

    def step(self, note=''):
        if self._point is None:
            raise RuntimeError('计时尚未开始。')
        if self._mark is None:
            self._mark = self._point
        m, s = delta2ms(datetime.now() - self._mark)
        self._print(note if note else f'(+{m:d}:{s:f})')
        self._mark = datetime.now()

    def stop(self, note=''):
        if self._point is None:
            raise RuntimeError('计时尚未开始。')
        self._print(note if note else 'Stopped.')
        self._point = None

    @classmethod
    def timing(cls, title: str = ''):
        def decorator(func):
            @wraps(func)
            def inner(*args, **kwargs):
                self = cls(title).start()
                returns = func(*args, **kwargs)
                self.stop()
                return returns

            return inner

        return decorator
