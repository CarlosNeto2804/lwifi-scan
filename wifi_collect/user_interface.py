def __get_user_response_to_question(message, default_value):
    user_response = input(message)
    return user_response or default_value


def get_dataset_name():
    message_to_user = 'Informe o nome do dataset (default = wifi_dict): '
    return __get_user_response_to_question(message_to_user, 'wifi_dict')


def get_target_room(enabled_rooms=[]):
    message_to_user = 'Informe o comodo a ser coletado\nOpçoes disponiveis: {rooms}\nR: '.format(rooms=",".join(enabled_rooms))
    return __get_user_response_to_question(message_to_user, 'not_informed')


def get_network_interface():
    message_to_user = 'Informe sua interface de rede (default = wlp2s0): '
    return __get_user_response_to_question(message_to_user,'wlp2s0')


def get_data_collect_per_cicle():
    message_to_user = 'Informe o numero de ciclos (default = 5): '
    return int(__get_user_response_to_question(message_to_user, 5))


def get_sleep_time_between_cicle():
    message_to_user = 'Informe o tempo entre ciclos (default = 5): '
    return int(__get_user_response_to_question(message_to_user, 5))
