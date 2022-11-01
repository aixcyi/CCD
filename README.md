<h1 align="center">Chinese Lunisolar Calendar</h1>

力求简单、稳定、高效的农历 Python 库。

## 功能

- [x] 农历日期的判等和比较
- [x] 农历日期的加减（与`datetime.time`）
- [x] 农历日期的数字化和汉字化
- [x] 公农历的互相转换
  - [x] 范围有限的快速转换
  - [x] 范围无限的计算转换
- [ ] 支持 Pickle 协议

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
# 'py_clc.base.ChineseCalendarDate(2022, 10, 3, False)'
```

## APIs

