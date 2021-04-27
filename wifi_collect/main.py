import pickle
import os
import time
import user_interface
from scan import get_available_wifis
from functools import reduce


def __not_exists_dataset_in_current_folder(dataset_name):
    return bool(dataset_name not in os.listdir('.'))


def __build_dump_file(data, dataset_name):
    with open(dataset_name, 'wb') as p_dump:
        pickle.dump(data, p_dump, pickle.HIGHEST_PROTOCOL)


def __create_default_dataset_if_not_exists(dataset, default_key, dataset_name):
    if __not_exists_dataset_in_current_folder(dataset_name):
        dataset[default_key] = []
        __build_dump_file(dataset, dataset_name)


def __get_available_wifis(network_interface):
    return get_available_wifis(network_interface)


def __add_wifi_on_existing_ssid(current_wifi, dataset):
    ssid = current_wifi['ssid']
    quality = current_wifi['quality']
    dataset[ssid].append(quality)


def __add_new_ssid(current_wifi, dataset):
    ssid = current_wifi['ssid']
    quality = current_wifi['quality']
    dataset[ssid] = [quality]


def __add_register_on_dataset(avaliable_wifis, dataset):
    print('[INFO] ADICIONANDO NO DATASET')
    for current_wifi in avaliable_wifis:
        if current_wifi['ssid'] in dataset:
            __add_wifi_on_existing_ssid(current_wifi, dataset)
        else:
            __add_new_ssid(current_wifi, dataset)


def __collect_data_per_cicle(dataset, cicles, network_interface, sleep_time):
    for i in range(cicles):
        print(i + 1)
        print('[INFO] BUSCANDO WIFIS DISPONIVEIS')
        avaliable_wifis = __get_available_wifis(network_interface)
        if bool(avaliable_wifis):
            print('[INFO] {total_wifis} WIFIS ENCONTRADOS'.format(total_wifis=len(avaliable_wifis)))
            __add_register_on_dataset(avaliable_wifis, dataset)
        time.sleep(sleep_time)
        print()
    print("[SUCCESS] DADOS ADICIONADOS AO DATASET")


def __normalize_dataset_headers(dataset, protected_key, target_room, limit):
    empty_positions = limit - len(dataset[protected_key])
    list_with_missing_headers = [target_room] * empty_positions
    dataset[protected_key] = [*dataset[protected_key], *list_with_missing_headers]


def all_numbers_are_zero(list_of_numbers):
    if bool(list_of_numbers):
        return len(list(filter(lambda x: x == 0, list_of_numbers))) == len(list_of_numbers)
    else:
        return False


def __normalize_dataset_to_left(dataset, protected_key):
    for key, wifi_items in dataset.items():
        if key != protected_key:
            head, *tail = wifi_items
            if all_numbers_are_zero(tail):
                print('NORMALIZANDO A ESQUERDA')
                dataset[key] = [*tail, head]


def __normalize_dataset_to_right(dataset, limit, protected_key, default_quality):
    for key, wifi_items in dataset.items():
        if key != protected_key:
            missing_numbers = limit - len(wifi_items)
            list_with_zeros_to_complete = [0] * missing_numbers
            dataset[key] = [*wifi_items, *list_with_zeros_to_complete]


def __get_max_num_items_of_ssids(database, protected_key):
    return max(reduce(lambda acc, ssid: [*acc, len(database[ssid]) if ssid != protected_key else 0], database, []))


def main_flow():
    __WIFI_DICT = {}
    __ENABLED_ROOMS = ['quarto1', 'quarto2', 'quarto3', 'varanda', 'sala', 'cozinha', 'banheiro']
    __DEFAULT_WIFI_QUALITY = 0
    __PROTECTED_KEY = 'COMODO'
    __DATASET_NAME = user_interface.get_dataset_name() + '.pkl'
    __DEFAULT_NETWORK_INTERFACE = user_interface.get_network_interface()
    __DATA_COLLECT_PER_CICLE = user_interface.get_data_collect_per_cicle()
    __SLEEP_TIME = user_interface.get_sleep_time_between_cicle()
    __TARGET_ROOM = user_interface.get_target_room(__ENABLED_ROOMS)
    __create_default_dataset_if_not_exists(__WIFI_DICT, __PROTECTED_KEY, __DATASET_NAME)
    with open(__DATASET_NAME, 'rb') as f:
        __WIFI_DICT = pickle.load(f)
        __collect_data_per_cicle(__WIFI_DICT, __DATA_COLLECT_PER_CICLE, __DEFAULT_NETWORK_INTERFACE, __SLEEP_TIME)
        print('[INFO] NORMALIZANDO DADOS A DIREITA')
        length_max = __get_max_num_items_of_ssids(__WIFI_DICT, __PROTECTED_KEY)
        __normalize_dataset_to_right(__WIFI_DICT, length_max, __PROTECTED_KEY, __DEFAULT_WIFI_QUALITY)
        __normalize_dataset_headers(__WIFI_DICT, __PROTECTED_KEY, __TARGET_ROOM, length_max)
        __normalize_dataset_to_left(__WIFI_DICT, __PROTECTED_KEY)
        __build_dump_file(__WIFI_DICT, __DATASET_NAME)


if __name__ == "__main__":
    main_flow()