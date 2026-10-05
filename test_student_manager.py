# -*- coding: utf-8 -*-
"""
学生信息管理系统 —— 单元测试
================================

这个文件是简历上"测试经验"的核心。
用 Python 自带的 unittest 框架，为 student_manager.py 的每个功能写测试用例，
覆盖：正常情况、异常情况、边界情况。

怎么运行（在 VSCode 里打开这个文件，点右上角 ▶ 运行按钮）：
  python test_student_manager.py
结果：
  "OK"     = 全部通过
  "FAILED" = 有失败（说明测出了 bug，这本身也是"测试能力"的体现）

学到的核心概念：
  测试用例 = 输入 + 预期结果 + 断言(assert)
  常用设计方法：等价类、边界值、场景法（见下方用例注释）
"""

import unittest
import sqlite3
import student_manager as sm


def _clear_db():
    """辅助函数：清空学生表，保证每个用例互不干扰。"""
    sm.init_db()
    conn = sqlite3.connect(sm.DB_FILE)
    conn.execute("DELETE FROM students")
    conn.commit()
    conn.close()


# ---------- 登录功能测试 ----------
class TestLogin(unittest.TestCase):

    def test_正确账号密码_登录成功(self):
        # 正常情况
        self.assertTrue(sm.login("admin", "123456"))

    def test_错误密码_登录失败(self):
        # 异常情况
        self.assertFalse(sm.login("admin", "000000"))

    def test_用户名为空_登录失败(self):
        # 边界情况
        self.assertFalse(sm.login("", "123456"))

    def test_密码为空_登录失败(self):
        # 边界情况
        self.assertFalse(sm.login("admin", ""))

    def test_用户名大小写_登录失败(self):
        # 边界情况：admin 和 Admin 应区分
        self.assertFalse(sm.login("Admin", "123456"))


# ---------- 添加学生功能测试 ----------
class TestAddStudent(unittest.TestCase):

    def setUp(self):
        _clear_db()

    def test_添加成功_返回id(self):
        sid = sm.add_student("张三", 20, "计算机", "13800000000")
        self.assertIsInstance(sid, int)

    def test_姓名为空_添加失败(self):
        # 等价类：无效输入
        self.assertIsNone(sm.add_student("", 20, "计算机", "138"))
        self.assertIsNone(sm.add_student("   ", 20, "计算机", "138"))

    def test_年龄超范围_添加失败(self):
        # 边界值：超上限
        self.assertIsNone(sm.add_student("小二", 40, "计算机", "138"))
        self.assertIsNone(sm.add_student("小三", 31, "计算机", "138"))   # 边界外一格
        self.assertIsNone(sm.add_student("小四", -1, "计算机", "138"))   # 负数

    def test_年龄边界值_添加成功(self):
        # 边界值：刚好在边界上，应该成功
        self.assertIsInstance(sm.add_student("小五", 0, "计算机", "138"), int)
        self.assertIsInstance(sm.add_student("小六", 30, "计算机", "138"), int)

    def test_添加后_能查询到(self):
        sm.add_student("李四", 21, "软件工程", "139")
        self.assertEqual(len(sm.search_student("李四")), 1)


# ---------- 查询学生功能测试 ----------
class TestSearchStudent(unittest.TestCase):

    def setUp(self):
        _clear_db()
        sm.add_student("王五", 22, "计算机", "137")

    def test_查询存在的学生(self):
        self.assertGreaterEqual(len(sm.search_student("王五")), 1)

    def test_查询不存在的学生_返回空(self):
        self.assertEqual(sm.search_student("不存在"), [])


# ---------- 删除学生功能测试 ----------
class TestDeleteStudent(unittest.TestCase):

    def setUp(self):
        _clear_db()

    def test_删除存在的学生(self):
        sid = sm.add_student("赵六", 20, "计算机", "136")
        self.assertTrue(sm.delete_student(sid))

    def test_删除不存在的id(self):
        # 边界：删除一个不存在的 id
        self.assertFalse(sm.delete_student(9999))

    def test_删除后_查询不到(self):
        sid = sm.add_student("钱七", 20, "计算机", "135")
        sm.delete_student(sid)
        self.assertEqual(sm.search_student("钱七"), [])


# ---------- 修改学生功能测试 ----------
class TestUpdateStudent(unittest.TestCase):

    def setUp(self):
        _clear_db()

    def test_修改存在的学生(self):
        sid = sm.add_student("孙八", 20, "计算机", "134")
        self.assertTrue(sm.update_student(sid, "孙八改", 21, "软工", "133"))

    def test_修改不存在的id(self):
        self.assertFalse(sm.update_student(9999, "x", 1, "x", "x"))

    def test_修改年龄超范围_失败(self):
        sid = sm.add_student("孙八", 20, "计算机", "134")
        self.assertFalse(sm.update_student(sid, "孙八", 40, "软工", "133"))

    def test_修改姓名为空_失败(self):
        sid = sm.add_student("孙八", 20, "计算机", "134")
        self.assertFalse(sm.update_student(sid, "", 21, "软工", "133"))


if __name__ == "__main__":
    unittest.main()
