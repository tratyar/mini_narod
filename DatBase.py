from regions_dicts import narod, info, data
from data.regions import Regions
from data.narods import Narods
from data import db_session
db_session.global_init("db/narod.db")


class Db_work():
    def __init__(self):
        self.narod = Narods
        self.reg = Regions
        self.db_sess = db_session.create_session()
        self.reg_num = 0
        self.reg_nar = []

    def reg_number(self, count):
        self.reg_num = count
        self.reg_nar = []

    def ret_reg_nar(self, num):
        reg_nar = self.db_sess.query(self.narod).all()
        for i in range(13):
            if str(num) in reg_nar[i].region:
                self.reg_nar.append(reg_nar[i].name)
        return self.reg_nar

    def ret_regions(self, text):
        reg = self.db_sess.query(self.reg).all()
        if info[text] == "development":
            return reg[self.reg_num].development
        if info[text] == "mine":
            return reg[self.reg_num].mine
        if info[text] == "history":
            return reg[self.reg_num].history
        if info[text] == "now_time":
            return reg[self.reg_num].now_time
        if info[text] == "traditions":
            return reg[self.reg_num].traditions
        if info[text] == "future_time":
            return reg[self.reg_num].future_time

    def ret_nar(self, inf):
        nar = self.db_sess.query(self.narod).all()
        if data[inf[1]] == "info":
            return nar[narod[inf[0]] - 1].info
        if data[inf[1]] == "histori":
            return nar[narod[inf[0]] - 1].history
        if data[inf[1]] == "traditions":
            return nar[narod[inf[0]] - 1].traditions
        if data[inf[1]] == "kitchen":
            return nar[narod[inf[0]] - 1].kitchen