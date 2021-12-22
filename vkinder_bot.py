# from random import randrange
# import vk_api
# from vk_api import VkUpload
# from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api_functions import lp_obj, write_msg, get_account_info, pair_search, write_msg_with_photos
from vk_api.longpoll import VkEventType
# import psycopg2


def returning_data_account(dict_id):
    for data in dict_id.items():
        del dict_id[data[0]]
        yield data


def get_user_data(event):
    for answer in lp_obj.listen():
        if answer.type == VkEventType.MESSAGE_NEW:
            if answer.to_me:
                pair_seeker_id = answer.text
                user_account_info = get_account_info(pair_seeker_id)

                if not user_account_info['birth_year']:
                    write_msg(event, "Отправьте, пожалуйста, год рождения пользователя "
                                     "(например: 2000)")
                    for answer_age in lp_obj.listen():
                        if answer_age.type == VkEventType.MESSAGE_NEW:
                            if answer_age.to_me:
                                user_account_info['birth_year'] = answer_age.text
                                break

                if not user_account_info['sex']:
                    write_msg(event, "Отправьте, пожалуйста, пол пользователя\n"
                                     "(если женский, отправьте: 1,\n"
                                     "если мужской, отправьте: 2)")
                    for answer_sex in lp_obj.listen():
                        if answer_sex.type == VkEventType.MESSAGE_NEW:
                            if answer_sex.to_me:
                                user_account_info['sex'] = answer_sex.text
                                break

                if not user_account_info['city']:
                    write_msg(event, "Отправьте, пожалуйста, название города пользователя")
                    for answer_city in lp_obj.listen():
                        if answer_city.type == VkEventType.MESSAGE_NEW:
                            if answer_city.to_me:
                                user_account_info['city'] = answer_city.text
                                break

                if not user_account_info['relation']:
                    write_msg(event, "Отправьте, пожалуйста, семейное положение пользователя\n"
                                     "(1 — не женат/не замужем;\n"
                                     "2 — есть друг/есть подруга;\n"
                                     "3 — помолвлен/помолвлена;\n"
                                     "4 — женат/замужем;\n"
                                     "5 — всё сложно;\n"
                                     "6 — в активном поиске;\n"
                                     "7 — влюблён/влюблена;\n"
                                     "8 — в гражданском браке.)")
                    for answer_relation in lp_obj.listen():
                        if answer_relation.type == VkEventType.MESSAGE_NEW:
                            if answer_relation.to_me:
                                user_account_info['relation'] = answer_relation.text
                                break

                    return user_account_info


def main():
    for event in lp_obj.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "Начать":
                    write_msg(event.user_id, "Отправьте, пожалуйста, имя пользователя или\n"
                                             "его id в ВК (для которого мы ищем пару).")

                    user_account_info = get_user_data(event.user_id)
                    dict_id = pair_search(user_account_info)
                    tuple_data_account = returning_data_account(dict_id).__next__()

                    write_msg_with_photos(event.user_id, tuple_data_account)

                    write_msg(event.user_id, f'\nОтправьте, пожалуйста, слово "Next"'
                                             f'для просмотра следующего аккаунта')
                    for message_next_account in lp_obj.listen():
                        if message_next_account.type == VkEventType.MESSAGE_NEW:
                            if message_next_account.to_me:
                                request = message_next_account.text
                                if request == "Next" or "next" or "NEXT":
                                    next_account_details = returning_data_account(dict_id).__next__()
                                    write_msg_with_photos(event.user_id, next_account_details)
                else:
                    write_msg(event.user_id, 'Нажмите, пожалуйста, кнопку "Начать"\n'
                                             '(или отправьте: Начать).')
                    continue

# ОШИБКА №1. При вводе боту названия города:
# vk_api.exceptions.ApiError: [100] One of the parameters specified was missing or invalid: city not integer
