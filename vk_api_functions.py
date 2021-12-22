# from pprint import pprint
from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll
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
    session_group.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})


def write_msg_with_photos(user_id, account_details):
    # pprint(account_details)
    """
    :param account_details: кортеж, где сначала идёт id найденного аккаунта, а вторым -- текст сообщения для отправки
    :param user_id: id пользователя кому отправляются данные
    # Ecли на входе нет всех трёх необходимых фотографий, необходимо как-то сделать так, чтобы не было ошибки и
    # код продолжал дальше работать
    :return: list с 3-мя фотографиями именно аккаунта (а не из других альбомов пользователя)
    """
    list_with_three_pictures = returning_photos_account(account_details[0])
    # print(list_with_three_pictures)

    if len(list_with_three_pictures) == 0:
        write_msg(user_id, account_details[1])
    else:

        write_msg(user_id, account_details[1])

        for id_photo in list_with_three_pictures:
            # pprint(id_photo)
            session_group.method('messages.send', {'user_id': user_id,
                                                   'random_id': randrange(10 ** 7),
                                                   'attachment': f"photo{account_details[0]}_{id_photo}"})

    # session_group.method('messages.send', {'user_id': user_id,
    #                                        'message': account_details[1],
    #                                        'random_id': randrange(10 ** 7),
    #                                        'attachment': f"photo{account_details[0]}_{list_with_three_pictures[0]}"})
    # session_group.method('messages.send', {'user_id': user_id,
    #                                        'random_id': randrange(10 ** 7),
    #                                        'attachment': f"photo{account_details[0]}_{list_with_three_pictures[1]}"})
    # session_group.method('messages.send', {'user_id': user_id,
    #                                        'random_id': randrange(10 ** 7),
    #                                        'attachment': f"photo{account_details[0]}_{list_with_three_pictures[2]}"})


def get_account_info(name_or_id_user):
    """
    :param: name_or_id_user:
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


def returning_photos_account(vk_id_account):

    def get_photos_three_max_popular_photo(dict_photo_id_and_count_reactions):
        # pprint(dict_photo_id_and_count_reactions)
        list_three_ids_photo = list()

        if len(dict_photo_id_and_count_reactions) <= 3:
            list_three_ids_photo = dict_photo_id_and_count_reactions.keys()
        else:
            popularity_values_list = list(dict_photo_id_and_count_reactions.values())
            id_photo = list(dict_photo_id_and_count_reactions.keys())
            id_most_popular_photo = id_photo[popularity_values_list.index(max(popularity_values_list))]
            list_three_ids_photo.append(id_most_popular_photo)
            del dict_photo_id_and_count_reactions[id_most_popular_photo]

            popularity_values_list = list(dict_photo_id_and_count_reactions.values())
            id_photo = list(dict_photo_id_and_count_reactions.keys())
            id_most_popular_photo = id_photo[popularity_values_list.index(max(popularity_values_list))]
            list_three_ids_photo.append(id_most_popular_photo)
            del dict_photo_id_and_count_reactions[id_most_popular_photo]

            popularity_values_list = list(dict_photo_id_and_count_reactions.values())
            id_photo = list(dict_photo_id_and_count_reactions.keys())
            id_most_popular_photo = id_photo[popularity_values_list.index(max(popularity_values_list))]
            list_three_ids_photo.append(id_most_popular_photo)
            dict_photo_id_and_count_reactions.clear()

        return list_three_ids_photo

    params_vk = {
        'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
        'v': '5.131',
    }
    photos_get_url = 'https://api.vk.com/method/' + 'photos.get'
    photos_get_params = {
        'owner_id': vk_id_account,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
    }
    response = requests.get(photos_get_url, params={**params_vk, **photos_get_params})
    if response.status_code != 200:
        print("ERROR")
        return

    dict_photo_info = response.json()
    # pprint(dict_photo_info)

    dict_popularity_values_and_ids_photo = dict()
    for photo_info in dict_photo_info['response']['items']:
        photo_id = photo_info['id']
        popularity_values = photo_info['comments']['count'] + photo_info['likes']['count']
        dict_popularity_values_and_ids_photo[photo_id] = popularity_values

    list_1 = get_photos_three_max_popular_photo(dict_popularity_values_and_ids_photo)
    # pprint(list_1)
    return list_1
