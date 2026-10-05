# 学生信息管理系统

基于 **Python + SQLite** 的学生信息管理系统，实现登录校验与学生信息的增删改查，配套 **unittest** 单元测试。

## ✨ 功能

- 登录校验（用户名密码匹配、空值处理、大小写敏感）
- 学生信息增删改查（添加 / 查询 / 修改 / 删除 / 查看全部）
- 输入校验（姓名非空、年龄 0–30 岁）

## 🧪 测试

- 共 **19 条**单元测试，基于 Python 标准库 `unittest`
- 覆盖正常 / 异常 / 边界三类情况
- 用例设计方法：等价类划分 + 边界值分析

## 📁 项目结构

| 文件 | 说明 |
|---|---|
| `student_manager.py` | 核心功能实现 |
| `test_student_manager.py` | 单元测试 |
| `README.md` | 说明文档 |

## 🚀 运行

环境要求：Python 3.x（仅使用标准库，无第三方依赖）

```bash
# 功能演示
python student_manager.py

# 运行测试
python test_student_manager.py
```

> Windows 下如 `python` 命令不可用，可使用 `py`。
