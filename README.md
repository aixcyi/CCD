<h1 align="center">Chinese Calendar Date</h1>

力求简单、稳定、高效的农历日期 Python 库。

## 功能一览

- [x] 农历日期的判等和比较
- [x] 农历日期的加减（与`datetime.timedelta`）
- [x] 农历日期的数字化和汉字化
- [x] 公农历的互相转换
  - [x] 范围有限的快速转换（`FastCCD`）
  - [x] 范围无限的计算转换（`EphemCCD`）
- [ ] 支持 Pickle 协议
- [x] 中文文档注释

## 兼容性

目前仅支持使用 Python 3.11 及以上版本运行。  
如果希望支持旧版本，可以提出 [Issue](#问题反馈) 并注明希望支持的最低版本，或点赞表态，也欢迎参与翻译。

## 快速上手

#### 安装

```shell
pip install CCD
```

#### 使用

```python
from datetime import date, timedelta
from ccd import FastCCD

gcd = date.today()
print(str(gcd))  # '2020-06-20'

ccd = FastCCD.from_date(gcd)
print(str(ccd))  # '农历2020年闰四月廿九'
print(repr(ccd))  # 'ccd.base.FastCCD(2020, 4, 29, True)'

ccd += timedelta(days=1)
print(str(ccd))  # '农历2020年五月初一'
print(repr(ccd))  # 'ccd.base.FastCCD(2020, 5, 1, False)'

gcd = ccd.to_date()
print(str(gcd))  # '2020-06-21'
```

#### 说明

农历日期类有以下几个：

- `ccd.EphemCCD`，无限范围。需要安装 [PyEphem](https://pypi.org/project/ephem/) 库后才可用。
- `ccd.FastCCD`，有限范围。无论何时都可用。
- `ccd.ChineseCalendarDate`，无论何时都可用。
  - 默认情况下等同于 `FastCCD` 。
  - 安装 [PyEphem](https://pypi.org/project/ephem/) 库后等同于 `EphemCCD` 。


## 问题反馈

码云：[https://gitee.com/aixcyi/CCD/issues](https://gitee.com/aixcyi/CCD/issues)  
GitHub：[https://github.com/aixcyi/CCD/issues](https://github.com/aixcyi/CCD/issues)

