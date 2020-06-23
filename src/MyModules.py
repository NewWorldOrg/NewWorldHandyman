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

    def __insert(self, sql: str):
        cnx = self.__db_connect()
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
            return True
        except:
            cnx.rollback()
            return False

    def __select(self, sql: str):
       cnx = self.__db_connect()
       cur = cnx.cursor(dictionary=True)
       try:
           cur.execute(sql)
           return cur.fetchall()
       except:
           raise

    def save_drug_mapping_data(self, drug_name: str):

        url = wikipediaSearch(drug_name)

        if not url:
            return False

        sql = "INSERT INTO `{table}` (drug, url) VALUES ('{drug}', '{url}')".format(
            table = 'drug_url_mapping_data',
            drug = drug_name,
            url = url,
        )

        try:
            self.__insert(sql)
            return True
        except:
            cnx.rollback()
            raise


    def  get_drug_data(self, drug_name: str):
        sql = "SELECT `url` FROM `{table_name}` WHERE drug='{drug}'".format(table_name='drug_url_mapping_data', drug=drug_name)

        try:
            result = self.__select(sql)
        except:
            raise

        if not result:
            return False

        return result[0]['url']

    def save_use_drug_history(self, user: str, drug_name: str, amount: int):
        url = self.get_drug_data(drug_name)
        if not url:
            return False

        sql = "INSERT INTO `{table}` (user, drug_name, amount, url) VALUES ('{user}', '{drug}', {amount}, '{url}')".format(
            table = 'drug_use_history',
            user = user,
            drug = drug_name,
            amount = amount,
            url = url,
        )

        try:
            self.__insert(sql)
            return True
        except:
            cnx.rollback()
            return False

    def get_drug_use_history(self, user):

        sql = "SELECT `user`, `drug_name`, `amount`, `created_at` FROM drug_use_history WHERE `user` = '{user}'".format(
            user = user,
        )

        try:
            response = self.__select(sql)
        except Exception as e:
            print(e)
            raise

        return response

    def get_drug_use_count(self, user):
        sql = "SELECT `user`, `drug_name`, COUNT(`drug_name`) AS count, SUM(`amount`) AS amount FROM drug_use_history WHERE `user` = '{user}' GROUP BY `drug_name`".format(
            user = user,
        )

        try:
            response = self.__select(sql)
        except Exception as e:
            print(e)
            raise

        return response
