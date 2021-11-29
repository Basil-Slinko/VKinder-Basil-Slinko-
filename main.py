from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
# from vk_api import VkUpload
# from vk_api.keyboard import VkKeyboard, VkKeyboardColor


with open("user_vk_access_token.txt", "r", encoding="UTF-8") as file:
    user_access_token = file.read().strip()
session_user_vk = vk_api.VkApi(token=user_access_token)

with open("group_vk_access_token.txt", "r", encoding="UTF-8") as file:
    group_access_token = file.read().strip()
session_group = vk_api.VkApi(token=group_access_token)
lp_obj = VkLongPoll(session_group)


def write_msg(user_id, message):
    session_group.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})


def get_account_info(name_or_id_user):

    """
    :param name_or_id_user:
    :return: {'birth_year': user_age,
              'sex': user_gender,
              'city': user_city,
              'relation': user_relation}
    """

    params = {'user_ids': name_or_id_user, 'fields': 'bdate, sex, city, relation'}
    user_account_data = session_group.method("users.get", params)

    if 'bdate' not in user_account_data[0]:
        user_age = False
    else:
        user_age = user_account_data[0]['bdate'][-4:]
    if 'sex' not in user_account_data[0]:
        user_gender = False
    else:
        user_gender = user_account_data[0]['sex']
    if 'city' not in user_account_data[0]:
        user_city = False
    else:
        user_city = user_account_data[0]['city']['id']
    if 'relation' not in user_account_data[0]:
        user_relation = False
    else:
        user_relation = user_account_data[0]['relation']

    return {'birth_year': user_age,
            'sex': user_gender,
            'city': user_city,
            'relation': user_relation,
            'count': 999}


def pair_search(json_user_info):

    if json_user_info['sex'] == 1:
        json_user_info['sex'] = 2
    else:
        if json_user_info['sex'] == 2:
            json_user_info['sex'] = 1

    pair_to_user = session_user_vk.method("users.search", json_user_info)
    dict_id = {id_user['id']: f"{id_user['first_name']} {id_user['last_name']}\nhttps://vk.com/id{id_user['id']}"
               for id_user in pair_to_user['items']}

    return dict_id


def returning_data_account(dict_id):
    for data in dict_id.items():
        del dict_id[data[0]]
        yield data


# def returning_photo_account(tuple_account):
#     url_photo_account = vk_client.get_photos(tuple_account[0])
#     return url_photo_account


def main():
    for event in lp_obj.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                if request == "Начать":
                    write_msg(event.user_id, "Отправьте, пожалуйста, имя пользователя или\n"
                                             "его id в ВК (для которого мы ищем пару).")
                    for answer in lp_obj.listen():
                        if answer.type == VkEventType.MESSAGE_NEW:
                            if answer.to_me:
                                pair_seeker_id = answer.text
                                user_account_info = get_account_info(pair_seeker_id)

                                if not user_account_info['birth_year']:
                                    write_msg(event.user_id, "Отправьте, пожалуйста, год рождения пользователя "
                                                             "(например: 2000)")
                                    for answer_age in lp_obj.listen():
                                        if answer_age.type == VkEventType.MESSAGE_NEW:
                                            if answer_age.to_me:
                                                user_account_info['birth_year'] = answer_age.text
                                                break

                                if not user_account_info['sex']:
                                    write_msg(event.user_id, "Отправьте, пожалуйста, пол пользователя\n"
                                                             "(если женский, отправьте: 1,\n"
                                                             "если мужской, отправьте: 2)")
                                    for answer_sex in lp_obj.listen():
                                        if answer_sex.type == VkEventType.MESSAGE_NEW:
                                            if answer_sex.to_me:
                                                user_account_info['sex'] = answer_sex.text
                                                break

                                if not user_account_info['city']:
                                    write_msg(event.user_id, "Отправьте, пожалуйста, название города пользователя")
                                    for answer_city in lp_obj.listen():
                                        if answer_city.type == VkEventType.MESSAGE_NEW:
                                            if answer_city.to_me:
                                                user_account_info['city'] = answer_city.text
                                                break

                                if not user_account_info['relation']:
                                    write_msg(event.user_id, "Отправьте, пожалуйста, семейное положение пользователя\n"
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
                                
                                dict_id = pair_search(user_account_info)
                                tuple_data_account = returning_data_account(dict_id).__next__()

                                # photo = returning_photo_account(tuple_data_account)
                                # vk_api.upload.VkUpload.photo_messages(photos=photo, peer_id=event.user_id)

                                write_msg(event.user_id, tuple_data_account[1])
                                write_msg(event.user_id, f'\nОтправьте, пожалуйста, слово "Next"'
                                                         f'для просмотра следующего аккаунта')
                                for message_next_account in lp_obj.listen():
                                    if message_next_account.type == VkEventType.MESSAGE_NEW:
                                        if message_next_account.to_me:
                                            request = message_next_account.text
                                            if request == "Next" or "next" or "NEXT":
                                                write_msg(event.user_id, returning_data_account(dict_id).__next__()[1])

                else:
                    write_msg(event.user_id, 'Нажмите, пожалуйста, кнопку "Начать"\n'
                                             '(или отправьте: Начать).')
                    continue


if __name__ == "__main__":
    main()
