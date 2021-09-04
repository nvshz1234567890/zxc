from time import sleep
from random import shuffle
from threading import Thread

from vk_api import VkApi


class Hater(Thread):

    def __init__(self, token: str, cooldown: int, hate_ids: list, variants: list):
        Thread.__init__(self, name="hater")

        self.token = token
        self.cooldown = cooldown
        self.hate_ids = hate_ids
        self.variants = variants

        print("[HATER]: инициализирован")

    def __authorization(self):

        vk_session = VkApi(token=self.token)
        self.vk = vk_session.get_api()

    def __sender(self, peer_id: int, message: str):

        self.vk.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=0
        )

    def __worker(self):

        index = 0

        while True:

            if index < len(self.variants):

                for id in self.hate_ids:

                    try:

                        self.__sender(
                            peer_id=id,
                            message=self.variants[index]
                        )

                        print(f"[HATER]: сообщение айди {id} отправлено")

                    except:

                        print(f"[HATER]: не удалось отправить сообщение айди {id}")

                index += 1

            else:

                index = 0
                shuffle(self.variants)

                for id in self.hate_ids:

                    try:

                        self.__sender(
                            peer_id=id,
                            message=self.variants[index]
                        )

                        print(f"[HATER]: сообщение айди {id} отправлено")

                    except:

                        print(f"[HATER]: не удалось отправить сообщение айди {id}")

                index += 1

            sleep(self.cooldown)

    def run(self):

        try:

            self.__authorization()
            self.__worker()

        except Exception as e:
            print(f"[HATER]: {repr(e)}")
