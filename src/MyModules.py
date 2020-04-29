import mysql.connector as connector
import configparser
import os

from src.WikiSearch import wikipediaSearch

class MyModules:

    def __db_connect(self):
        base = os.path.dirname(os.path.abspath(__file__))
        conf_path = os.path.normpath(os.path.join(base, '../'))
        conf = configparser.ConfigParser()
        conf.read(conf_path+'/config.ini', encoding='utf-8')
        try:
            db = connector.connect(
                user = conf['DB']['USER'],
                passwd = conf['DB']['PASSWD'],
                host = conf['DB']['HOST'],
                db = conf['DB']['DATABASE'],
            )
            return db
        except Exception as e:
            print(e)
            raise

    def __create_drug_mapping_data(self, drug_name: str):

        url = wikipediaSearch(drug_name)

        if not url:
            return False

        sql = "INSERT INTO `{table}` (drug, url) VALUES ('{drug}', '{url}')".format(
            table = 'drug_url_mapping_data',
            drug = drug_name,
            url = url,
        )
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
        except:
            cnx.rollback()
            raise

        return url

    def  __get_drug_mapping_data(self, drug_name: str):
        sql = "SELECT `url` FROM `{table_name}` WHERE drug='{drug}'".format(table_name='drug_url_mapping_data', drug=drug_name)
        cnx = self.__db_connect()
        cur = cnx.cursor(dictionary=True)
        try:
            cur.execute(sql)
            result = cur.fetchall()
            cur.close()
        except:
            raise

        if not result:
            result = self.__create_drug_mapping_data(drug_name)
            if not result:
                return False
            return result

        return result[0]['url']

    def save_use_drug_history(self, user, drug_name):
        url = self.__get_drug_mapping_data(drug_name)
        if not url:
            return False

        sql = "INSERT INTO `{table}` (user, drug_name, url) VALUES ('{user}', '{drug}', '{url}')".format(
            table = 'drug_use_history',
            user = user,
            drug = drug_name,
            url = url,
        )
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
            return True
        except:
            cnx.rollback()
            return False
