import mysql.connector as connector
import configparser
import os

from src.WikiSearch import wikipediaSearch
from src.DbModules import DbModule as db

class MyModules:

    def __init__(self):
        self.db = db()

    def save_drug_mapping_data(self, drug_name: str):
        
        table = 'drug_url_mapping_data'

        url = wikipediaSearch(drug_name)

        if not url:
            return False

        value = {
            'drug': drug_name,
            'url': url,
        }

        try:
            self.db.insert(table, value)
            return True
        except:
            raise


    def get_drug_data(self, drug_name: str):
        sql = "SELECT `id` FROM `{table_name}` WHERE drug='{drug}'".format(
            table_name = 'drug_url_mapping_data',
            drug = drug_name
        )

        try:
            result = self.db.select(sql)
        except:
            raise

        if not result:
            return False

        return result[0]['id']

    def get_user(self, user_id: int):
        table = 'users'
        sql = "SELECT * FROM `{table}` WHERE user_id = '{user_id}'".format(
            table = table,
            user_id = user_id,
        )

        try:
            result = self.db.select(sql)
        except:
            raise

        return result[0]


    def save_use_drug_history(self, user_id: int, drug_name: str, amount: int):
        drug_id = self.get_drug_data(drug_name)
        if not drug_id:
            return False
        user = self.get_user(user_id)
        value = {
            'user_id': str(user['id']),
            'drug_id': str(drug_id),
            'amount': str(amount),

        }

        try:
            self.db.insert('medication_histories', value)
            return True
        except:
            raise

    def get_drug_use_history(self, user):

        sql = "SELECT `user`, `drug_name`, `amount`, `created_at` FROM drug_use_history WHERE `user` = '{user}'".format(
            user = user,
        )

        try:
            response = self.db.select(sql)
        except Exception as e:
            print(e)
            raise

        return response

    def get_drug_use_count(self, user):
        sql = "SELECT `user`, `drug_name`, COUNT(`drug_name`) AS count, SUM(`amount`) AS amount FROM drug_use_history WHERE `user` = '{user}' GROUP BY `drug_name`".format(
            user = user,
        )

        try:
            response = self.db.select(sql)
        except Exception as e:
            print(e)
            raise

        return response

    def get_registered_drug_list(self):
        sql = "SELECT `drug` FROM `drug_url_mapping_data`"
        try:
            response = self.db.select(sql)
        except Exception as e:
            print(e)
            raise

        return response

    def get_the_last_time_of_medication(self, user: str):
        sql = "SELECT created_at FROM `drug_use_history` WHERE user = '{user}' ORDER BY id DESC LIMIT 1".format(
            user = user
        )
        try:
            response = self.db.select(sql)
        except Exception as e:
            print(e)
            raise

        return response    

    def member_register(self, member_data):

        self.db.insert('users', member_data)

    def update_user_name(self, user_id: int, after_name: str):
        sql = ""