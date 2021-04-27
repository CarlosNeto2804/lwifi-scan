import subprocess

__TARGET_FIELDS = ['ESSID', 'Quality', 'Frequency']

# wlp2s0
def __execute_bash_command_to_list_wifis(network_interface):
    command = "iwlist {interface} scan |grep -e ESSID -e Quality -e Frequency".format(interface=network_interface)
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    return process.stdout


def __filter_stdout_data(stdout):
    return len(list(filter(lambda x: x in stdout, __TARGET_FIELDS))) > 0


def __parse_stdout_text_to_list(stdout_list):
    return list(filter(__filter_stdout_data, list(map(str.strip, str(stdout_list).splitlines()))))


def __group_wifi_props(raw_data):
    collection_wifi_props = []
    for i in range(0, len(raw_data), 3):
        wf = raw_data[i:i + 3]
        freq, qual, ssid = wf
        collection_wifi_props.append((ssid, qual, freq))
    return collection_wifi_props


def __normalize_ssid(ssid_str):
    """"parse 'ESSID:"NAME" ' -> NAME"""
    return str(ssid_str).split(':')[1].replace('"', '').strip()


def __normalize_quality(quality_str):
    """"parse 'Quality=VALUE_X/70  Signal level=VALOR_Y dBm' -> VALUE_X"""
    return str(quality_str).split(" ")[0].split('=')[1].split('/')[0]


def __normalize_frequency(freq_str):
    """"parse 'Frequency:FREQUENCY_VALUE GHz (Channel 4)' -> FREQUENCY_VALUE"""
    return str(freq_str).split(" ")[0].split(':')[1]


def __parse_wifi_tuple_to_dict(wifi_tuple):
    return {
        "ssid": __normalize_ssid(wifi_tuple[0]),
        "quality": __normalize_quality(wifi_tuple[1]),
        "frequency": __normalize_frequency(wifi_tuple[2])
    }


def __normalize_data(grouped_wifi_props):
    return list(map(__parse_wifi_tuple_to_dict, grouped_wifi_props))


def get_available_wifis(network_interface='wlp2s0'):
    stdout = __execute_bash_command_to_list_wifis(network_interface)
    raw_data = __parse_stdout_text_to_list(stdout)
    grouped_wifi_props = __group_wifi_props(raw_data)
    return __normalize_data(grouped_wifi_props)
