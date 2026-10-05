# -*- coding: utf-8 -*-
"""
学生信息管理系统

基于 Python + SQLite 实现，提供登录校验与学生信息的增删改查功能。
配套单元测试见 test_student_manager.py。
"""

import sqlite3

# ================= 登录模块 =================
USERNAME = "admin"
PASSWORD = "123456"


def login(username, password):
    """登录校验：用户名与密码均匹配时返回 True，否则返回 False。"""
    if not username or not password:
        return False
    return username == USERNAME and password == PASSWORD


# ================= 数据库 =================
DB_FILE = "students.db"


def _conn():
    """获取数据库连接。"""
    return sqlite3.connect(DB_FILE)


def init_db():
    """初始化数据库：students 表不存在时自动创建。"""
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


# ================= 学生增删改查 =================
def add_student(name, age, major, phone):
    """添加学生：姓名非空、年龄 0-30 合法；成功返回新 id，失败返回 None。"""
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
    """按姓名精确查询，返回学生列表（未找到返回空列表）。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE name = ?", (name,))
    rows = cur.fetchall()
    conn.close()
    return rows


def list_students():
    """返回全部学生。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_student(student_id, name, age, major, phone):
    """按 id 修改学生信息；姓名非空、年龄 0-30 合法，返回是否成功。"""
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
    """按 id 删除学生，返回是否删除成功。"""
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted


# ================= 主程序 =================
if __name__ == "__main__":
    init_db()

    print("=== 学生信息管理系统 ===\n")

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
