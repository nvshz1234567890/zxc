from json import load
from random import shuffle

from modules.hater import Hater
from modules.commander import Commander
from modules.database import Database


class Core:

    def __init__(self):

        self.config = self.__get_config()
        self.hate_ids = []
        self.variants_path = "variants/variants.txt"
        self.variants = self.__get_variants()
        self.database = Database("database/database.db")

    def __get_config(self):

        with open('config.json', "r", encoding="utf-8") as file:
            return load(file)

    def __get_variants(self):

        with open(self.variants_path, "r", encoding="utf-8") as f:
            return f.readlines()

    def __get_users(self):

        users = self.database.get_all_users()

        for user in users:
            self.hate_ids.append(user[0])

    def run(self):

        self.__get_config()
        self.__get_variants()
        self.__get_users()

        shuffle(self.variants)

        Hater(token=self.config["BOT_TOKEN"], cooldown=self.config["COOLDOWN"], hate_ids=self.hate_ids, variants=self.variants).start()
        Commander(token=self.config["BOT_TOKEN"], hate_ids=self.hate_ids, database=self.database, config=self.config).start()

        print("\n[BOT]: успешно запущен\n")


if __name__ == '__main__':
    Core().run()
