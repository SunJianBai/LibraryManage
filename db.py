import pymysql
import traceback
import logging

# 配置日志记录
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# host = "117.72.218.137"
host = "127.0.0.1"
# user = "ll"
user = "root"
password = "879879"
database = "ll"  # 数据库名字
port = 3306


def get_conn():
    """
    链接数据库
    :return: 连接，游标
    """
    try:
        # 创建连接
        conn = pymysql.connect(host=host,
                              user=user,
                              password=password,
                              db=database,
                              port=port)  # 添加超时设置方便诊断
        logging.debug("成功连接到数据库")
        # 创建游标
        cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        return conn, cursor
    except Exception as e:
        logging.error(f"连接数据库失败: {e}")
        return None, None


def close_conn(conn, cursor):
    """
    关闭链接
    :param conn:
    :param cursor:
    :return:
    """
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """
    封装通用查询
    :param sql:
    :param args:
    :return: 返回查询到的结果，((),(),)的形式
    """
    conn, cursor = get_conn()
    if conn is None or cursor is None:
        logging.error("数据库连接为空，无法执行查询")
        return ()
    try:
        cursor.execute(sql, args)
        res = cursor.fetchall()
        logging.debug(f"查询结果: {res}")
        return res
    except Exception as e:
        logging.error(f"执行查询失败: {e}")
        return ()
    finally:
        close_conn(conn, cursor)


def exec_(sql):
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        if conn is None or cursor is None:
            logging.error("数据库连接为空，无法执行操作")
            return
        cursor.execute(sql)
        conn.commit()  # 提交事务 update delete insert操作
        logging.debug("操作提交成功")
    except Exception as e:
        logging.error(f"执行操作失败: {e}")
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def main():
    sql = "select * from student"  # mysql查询语句
    res = query(sql)
    # print(res)