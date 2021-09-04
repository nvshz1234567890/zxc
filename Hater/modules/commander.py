from threading import Thread

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType


class Commander(Thread):

    def __init__(self, token: str, hate_ids: list, database, config):
        Thread.__init__(self, name="commander")

        self.token = token
        self.hate_ids = hate_ids
        self.database = database
        self.config = config

        print("[COMMANDER]: инициализирован")

    def __authorization(self):

        self.config["ADMINS"].append(self.database.init_database())
        vk_session = VkApi(token=self.token)

        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()

    def __sender(self, peer_id: int, message: str):

        self.vk.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=0
        )

    def __filter_id(self, pattern):

        if "[id" in pattern:
            return int(pattern.split("|")[0].replace("[id", ""))

        elif "vk.com/" in pattern:
            domen = pattern.split("/")[-1].replace("id", "")
            return self.vk.users.get(user_ids=domen)[0]["id"]

        else:

            return None

    def __get_id(self, event, split_text):

        message = self.vk.messages.getById(message_ids=event.message_id)['items'][0]

        if len(split_text) == 2:

            user_id = self.__filter_id(split_text[1])

        elif len(split_text) == 1 and "reply_message" in message:

            user_id = message['reply_message']['from_id']

        else:

            user_id = None

        return user_id

    def __polling(self):

        try:

            for event in self.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:

                    text = event.text.split(' ')

                    if text[0] in self.config["commands"]:

                        if event.user_id in self.config["ADMINS"]:

                            if len(text) == 2 and text[1] in self.config["con"]:

                                user = event.peer_id

                            else:

                                user = self.__get_id(event, text)

                            if user is not None:

                                if text[0] in self.config["add"]:

                                    if len(text) == 2 and text[1] in self.config["con"]:

                                        self.database.add_hate(
                                            id=user
                                        )
                                        self.hate_ids.append(user)

                                        self.__sender(
                                            peer_id=event.peer_id,
                                            message=f"✅ Беседа {user} добавлена в базу"
                                        )

                                        print(f"[COMMANDER]: беседа {user} добавлена в базу")

                                    else:

                                        if self.database.check_hate(user) is False:

                                            self.database.add_hate(
                                                id=user
                                            )
                                            self.hate_ids.append(user)

                                            self.__sender(
                                                peer_id=event.peer_id,
                                                message=f"✅ Айди {user} добавлено в базу"
                                            )

                                            print(f"[COMMANDER]: айди {user} добавлено в базу")

                                        else:

                                            self.__sender(
                                                peer_id=event.peer_id,
                                                message=f"❎ Айди {user} уже имеется в базе"
                                            )

                                if text[0] in self.config["del"]:

                                    if len(text) == 2 and text[1] in self.config["con"]:

                                        if self.database.check_hate(user) is True:
                                            self.database.del_hate(
                                                id=user
                                            )
                                            self.hate_ids.remove(user)

                                            self.__sender(
                                                peer_id=event.peer_id,
                                                message=f"✅ Беседа {user} удалена из базы"
                                            )

                                            print(f"[COMMANDER]: беседа {user} удалена из базы")

                                    else:

                                        if self.database.check_hate(user) is True:

                                            self.database.del_hate(
                                                id=user
                                            )
                                            self.hate_ids.remove(user)

                                            self.__sender(
                                                peer_id=event.peer_id,
                                                message=f"✅ Айди {user} удалено из базы"
                                            )

                                            print(f"[COMMANDER]: айди {user} удалено из базы")

                                        else:

                                            self.__sender(
                                                peer_id=event.peer_id,
                                                message=f"❎ Айди {user} отсутствует в базе"
                                            )

                            else:

                                self.__sender(
                                    peer_id=event.peer_id,
                                    message=f"❎ Пользователь не указан"
                                )

        except Exception as e:
            print(f"[COMMANDER]: {repr(e)}")

    def run(self):

        try:

            self.__authorization()
            self.__polling()

        except Exception as e:
            print(f"[COMMANDER]: {repr(e)}")
