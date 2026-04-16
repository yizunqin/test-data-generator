# 测试数据生成工具

[English](README_en.md) | 简体中文

一个基于 PyQt5 的桌面应用，用于生成各类测试数据，支持导出文件。

![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15.10-orange)
![License](https://img.shields.io/badge/license-GPL--3.0-yellow)
[![Legal](https://img.shields.io/badge/Legal-For%20Testing%20Only-orange)](DISCLAIMER.md)
[![Warning](https://img.shields.io/badge/Warning-Read%20Disclaimer-red)](DISCLAIMER.md)

## 功能特性

| 功能 | 说明 |
|------|------|
| 随机身份证号 | 支持按区划、生日、性别筛选，校验码自动计算 |
| 统一社会信用代码 | 支持按区划、登记管理部门、机构类别筛选，含校验位 |
| 随机数据 | 支持生成电子邮件、地址 |
| 随机手机号码 | 生成符合中国规范的11位手机号 |
| 随机姓名 | 支持按性别筛选（男/女） |
| 自增数据 | 支持数字/字母序列，可自定义标志位和总位数 |
| 随机密码 | 可配置长度、是否包含大小写字母/数字/特殊字符 |
| 合并文件 | 支持多文件按行合并，自动检测文件编码 |

## 界面预览

左侧为导航栏，右侧为功能面板，统一提供：生成、导出、重置 三个操作按钮。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行项目

```bash
python main.py
```

## 打包为 EXE

项目使用 PyInstaller 打包：

```bash
pip install pyinstaller
pyinstaller YourAppName.spec
```

打包后的文件位于 `dist/` 目录。

## 项目结构

```
.
├── main.py                        # 主窗口 + 导航栏
├── pages/                         # 各功能页面
│   ├── welcome_page.py            # 欢迎页（含功能说明、规则、注意事项）
│   ├── id_card_page.py            # 身份证号生成
│   ├── credit_code_page.py        # 统一社会信用代码生成
│   ├── random_data_page.py        # 随机数据（邮件、地址）
│   ├── phone_number_page.py       # 手机号码生成
│   ├── name_page.py               # 姓名生成
│   ├── increment_page.py          # 自增数据生成
│   ├── pass_word_generation_page.py  # 密码生成
│   └── merge_files_page.py        # 文件合并
├── utils/                         # 工具模块
│   ├── random_data_generator.py   # Faker 封装 + 导出函数 + 基类
│   ├── social_credit_code_generator.py  # 统一社会信用代码生成器
│   └── data.py                    # 区划数据、登记管理部门等静态数据
├── resources/                     # 图标和样式
│   ├── style.qss                  # QSS 样式表
│   └── *.png / *.ico               # 按钮图标、应用图标
├── build/                         # PyInstaller 打包临时文件
├── dist/                          # PyInstaller 打包输出目录
├── YourAppName.spec               # PyInstaller 配置文件
├── requirements.txt              # Python 依赖
└── start.py                       # 启动脚本
```

## 数据规则说明

- **区划选择**：非必填，不选择时随机分配全国区划
- **生日**：格式 `YYYY.MM.DD`，支持日历选择，非必填
- **性别**：男/女，非必填，不填时随机
- **自增数据位数**：字母类型时受组合数限制（1位最多26条，2位最多702条，以此类推）
- **密码**：至少选择一种字符类型

## 技术栈

- **GUI 框架**: PyQt5 5.15.10
- **数据生成**: Faker 16.8.1
- **打包工具**: PyInstaller
- **Python 版本**: 3.7+

## License

本项目基于 **GNU General Public License v3.0** 开源，详见 [LICENSE.md](LICENSE.md)。

## 法律与合规警告

- 本工具仅供**合法的软件测试与开发**使用。生成的身份证号、统一社会信用代码、姓名、邮箱、地址均为**虚拟测试数据- 仅用于测试目的**，严禁用于伪造证件、冒充身份、批量注册虚假账户、诈骗等任何违法活动。  
- **使用者需自行承担违法违规使用的一切法律责任。** 详细免责条款请阅读 [DISCLAIMER.md](DISCLAIMER.md)。


