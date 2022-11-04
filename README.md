<h1 align="center">Chinese Lunisolar Calendar</h1>

力求简单、稳定、高效的农历 Python 库。

## 功能

- [x] 农历日期的判等和比较
- [x] 农历日期的加减（与`datetime.timedelta`）
- [x] 农历日期的数字化和汉字化
- [x] 公农历的互相转换
  - [x] 范围有限的快速转换（`FastCCD`）
  - [x] 范围无限的计算转换（`EphemCCD`）
- [ ] 支持 Pickle 协议

## 使用须知

目前仅支持使用 Python 3.10 及以上版本运行，因为不想背负历史包袱。
如果希望支持旧版本，请提出 [Issue](https://github.com/aixcyi/PyCLC/issues) 并注明希望支持的最低版本，或对 Issue
点赞表态，也欢迎参与翻译。

## 快速上手

#### 安装

```shell
pip install py_clc
```

#### 导入

农历日期类主要有以下几个：

- `py_clc.ChineseCalendarDate`，无论何时都可用。
- `py_clc.FastCCD`，无论何时都可用。
- `py_clc.EphemCCD`，需要安装 [PyEphem](https://pypi.org/project/ephem/) 库后才可用，否则导入时会报错。

区别在于，其它类任何时候都是自身，而 `py_clc.ChineseCalendarDate` 默认情况下等同于 `FastCCD`
，安装对应所需的库后等同于 `EphemCCD` 。

不应该使用其它路径来导入农历日期类。

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

