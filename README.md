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
from datetime import date, timedelta
from py_clc import ChineseCalendarDate

gcd = date.today()
print(str(gcd))
# '2020-06-20'

ccd = ChineseCalendarDate.from_date(gcd)
print(str(ccd))
# '农历2020年闰四月廿九'
print(repr(ccd))
# 'py_clc.base.ChineseCalendarDate(2020, 4, 29, True)'

ccd += timedelta(days=1)
print(str(ccd))
# '农历2020年五月初一'
print(repr(ccd))
# 'py_clc.base.ChineseCalendarDate(2020, 5, 1, False)'

gcd = ccd.to_date()
print(str(gcd))
# '2020-06-21'
```

## APIs

