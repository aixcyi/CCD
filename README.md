<h1 align="center">Chinese Lunisolar Calendar</h1>

力求简单、稳定、高效的农历 Python 库。

## 功能

- 农历文本与数字的互相转换。
- 公农历的互相转换。
- 农历日期对象的存储、判等、比较、加减。

## 快速上手

#### 安装

```shell
pip install py_clc
```

#### 使用

```python
from py_clc import ChineseCalendarDate

today = ChineseCalendarDate.today()
print(str(today))
# '农历2022年八月廿一'
print(repr(today))
# 'py_clc.limited.ChineseCalendarDate(2022, 10, 3, False)'
```

