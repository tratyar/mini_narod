from regions import regions, narod, reg_db
from data.regions import Regions
from data.narods import Narods



data = {'💡 Информация': 'info', '🎞️ История': "histori", '👺 Традиции': 'traditions', '🥞 Фирменные блюда': "kooking"}


class Db_work():
    def __init__(self):
        from data import db_session
        self.narod = Narods()
        self.reg = Regions()
        self.db_sess = db_session.create_session()

    def ret_regions(self, cnt):
        for reg in self.db_sess.query(self.reg).filter((self.reg.id == int(reg_db[regions[cnt]])), self.reg.data[cnt]):
            return reg

    def ret_nar(self, cnt):
        for nar in self.db_sess.query(self.narod).filter((self.narod.id == int(reg_db[regions[cnt]])), self.narod.data[cnt]):
            return nar