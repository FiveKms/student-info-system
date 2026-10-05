# -*- coding: utf-8 -*-
"""
学生信息管理系统 —— 软件测试练手项目
=====================================

这是一个为零基础 → 软件测试实习 设计的学习项目。

它同时帮你练习两件事：
  1. 看懂 Python 基础：函数、SQLite 数据库、增删改查
  2. 把它当成"被测系统"，在 test_student_manager.py 里为它写测试用例

项目功能：
  登录校验 / 添加学生 / 查询学生 / 修改学生 / 删除学生 / 查看全部学生

怎么运行（在 VSCode 里打开这个文件，点右上角的 ▶ 运行按钮）：
  student_manager.py        跑一遍功能演示
  test_student_manager.py   跑测试用例
"""

import sqlite3

# ================= 一、登录模块 =================
# 写死一个账号密码，方便练习"登录功能"的经典测试用例
# （正确密码 / 错误密码 / 空输入 / 大小写 等）
USERNAME = "admin"
PASSWORD = "123456"


def login(username, password):
    """登录校验：成功返回 True，失败返回 False。"""
    if not username or not password:
        return False  # 用户名或密码为空 -> 失败
    return username == USERNAME and password == PASSWORD


# ================= 二、数据库 =================
DB_FILE = "students.db"


def _conn():
    """内部辅助函数：获取一个数据库连接。"""
    return sqlite3.connect(DB_FILE)


def init_db():
    """初始化：如果学生表不存在就创建它。"""
    conn = _conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            age   INTEGER,
            major TEXT,
            phone TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# ================= 三、学生增删改查 =================
def add_student(name, age, major, phone):
    """
    添加学生。
    姓名 name 不能为空，否则返回 None（表示失败）；
    成功则返回新学生的 id（整数）。
    年龄 age 在0~30之间，否则返回 None（表示失败）
    """
    if not name or not name.strip():
        return None
    if not 0 <= age <= 30:
        return None
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (name, age, major, phone) VALUES (?, ?, ?, ?)",
        (name.strip(), age, major, phone),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def search_student(name):
    """按姓名精确查询，返回学生列表（查不到返回空列表 []）。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE name = ?", (name,))
    rows = cur.fetchall()
    conn.close()
    return rows


def list_students():
    """返回所有学生。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_student(student_id, name, age, major, phone):
    """按 id 修改学生信息（全部字段），返回是否成功（True/False）。"""
    if not name or not name.strip():
        return False
    if not 0 <= age <= 30:
        return False
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=?, age=?, major=?, phone=? WHERE id=?",
        (name, age, major, phone, student_id),
    )
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated


def delete_student(student_id):
    """按 id 删除学生，返回是否真的删掉了（True/False）。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


# ================= 四、主程序（演示） =================
if __name__ == "__main__":
    init_db()

    print("=== 学生信息管理系统 演示 ===\n")

    print("登录 admin / 123456   ->", login("admin", "123456"))
    print("登录 admin / 错误密码 ->", login("admin", "000000"))
    print("登录 空用户名         ->", login("", "123456"))
    print()

    sid = add_student("张三", 20, "计算机科学与技术", "13800000000")
    print("添加 张三 -> id =", sid)
    add_student("李四", 21, "软件工程", "13900000000")
    print("添加 李四 成功\n")

    print("查询 张三  ->", search_student("张三"))
    print("查询 不存在 ->", search_student("王五"))
    print()

    print("全部学生 ->", list_students())
