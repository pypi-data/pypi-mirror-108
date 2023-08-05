from pymysql import connect


class Config:
    conn = None
    cs = None

    def __init__(self, host='127.0.0.1', port=3306, database='test', user='root',
                 password='123123', charset='utf8'):
        Config.conn = connect(host=host, port=port, database=database,
                              user=user, password=password, charset=charset)
        Config.cs = Config.conn.cursor()


def query(cmd):
    Config.cs.execute(cmd)
    return Config.cs.fetchall()


def commit():
    # 提交之前的操作，如果之前已经之执行过多次的execute，那么就都进行提交
    Config.conn.commit()


class Update:
    def getIPFromCMD(self):
        pass

    @classmethod
    def updateIP(cls):
        pass
