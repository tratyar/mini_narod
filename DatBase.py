from regions import regions, narod, reg_db
from data.regions import Regions
from data.narods import Narods
from data import db_session
db_session.global_init("db/narod.db")


data = {'💡 Информация': 'info', '🎞️ История': "histori", '👺 Традиции': 'traditions', '🥞 Фирменные блюда': "kooking"}


class Db_work():
    def __init__(self):
        self.narod = Narods()
        self.reg = Regions()
        self.db_sess = db_session.create_session()

    def ret_regions(self, cnt):
        print(cnt)
        for reg in self.db_sess.query(self.reg).filter((self.reg.id == int(cnt)), self.reg.data[cnt]):
            print(reg)
            return reg

    def ret_nar(self, cnt):
        for nar in self.db_sess.query(self.narod).filter((self.narod.id == int(reg_db[regions[cnt]])), self.narod.data[cnt]):
            print(nar)
            return nar