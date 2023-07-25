import requests
import socket
from urllib.parse import urlparse
import sys


class ApiClient:

    def __init__(self, base_url, login, password):
        self.base_url = base_url
        self.login = login
        self.password = password

    def _check_base_url(self):
        url = urlparse(self.base_url)
        host = url.netloc
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((host, url.port if url.port else 80))

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, auth=(self.login, self.password))
            response.raise_for_status()
        except requests.RequestException as err:
            print(f"Ошибка при GET запросе: {err}")
            sys.exit(1)

        return response.json()

    def set(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, auth=(self.login, self.password))
            response.raise_for_status()
        except requests.RequestException as err:
            print(f"Ошибка при SET запросе: {err}")
            sys.exit(1)

        return response.json()


class RFIDConfig(ApiClient):

    def get_params(self):
        return self.get("rfidconfig")

    def set_continuous_scanning(self, value):
        return self.set("rfidconfig", {"infiniteinventory": str(value).lower()})

    def set_power_antenna(self, value, ch):
        return self.set("rfidconfig", {f"pwrant{ch}": value})

    def set_enable_antenna(self, value, ch):
        return self.set("rfidconfig", {f"enant{ch}": str(value).lower()})

    def set_enable_trigger(self, value, ch):
        return self.set("rfidconfig", {f"entrig{ch}": str(value).lower()})

    ####????????
    def set_trigger_state(self, value, ch):
        return self.set("rfidconfig", {f"triggered{ch}": value})

    def set_antenna_dependency(self, value):
        return self.set("rfidconfig", {"rf_session": value})

    def set_repeattime(self, value):
        return self.set("rfidconfig", {"repeattime": value})

    def set_min_hold_ms(self, value):
        return self.set("rfidconfig", {"min_hold_ms": value})


class PeripheryConfig(ApiClient):

    def get_params(self):
        return self.get("peripheryconfig")

    def set_relay_unit_enable(self, value):
        return self.set("peripheryconfig", {"smartboard_enable": str(value).lower()})

    def set_relay_enable(self, value, ch):
        response = self.set("peripheryconfig", {f"smartboard_port{ch}_enable": str(value).lower()})
        data = response
        smartboard_data = data['smartboard']
        if ch == 1:
            if value != smartboard_data['port_enable'][0]:
                return (f"Not Good: {value} != {smartboard_data['port_enable'][0]} for ch = {ch}")
        if ch == 2:
            if value != smartboard_data['port_enable'][1]:
                return (f"Not Good: {value} != {smartboard_data['port_enable'][1]} for ch = {ch}")
        return "Good"

    def set_relay_enable_ant(self, value, ch):
        response = self.set("peripheryconfig", {f"smartboard_port{ch}_ants": str(value).lower()})
        data = response
        smartboard_data = data['smartboard']
        if value not in smartboard_data['port_depends']:
            return f"Not Good: {value} not in {smartboard_data['port_depends']}"
        if ch not in smartboard_data['port_depends']:
            return f"Not Good: {ch} not in {smartboard_data['port_depends']}"
        return "Good"

    def set_relay_timer(self, value, ch):
        return self.set("peripheryconfig", {f"smartboard_port{ch}_timer": str(value).lower()})

    def set_wiegand_enable(self, value, ch):
        return self.set("peripheryconfig", {f"wiegand{ch}_enable": str(value).lower()})

    def set_wiegand_type(self, value):
        return self.set("peripheryconfig", {"wiegand1_type": value})

    def set_wiegand_shift_bytes(self, value):
        return self.set("peripheryconfig", {"wiegand1_shift_bytes": value})

    def set_wiegand_source(self, value):
        return self.set("peripheryconfig", {"wiegand1_source": value})

    def set_beep_on_start(self, value):
        return self.set("peripheryconfig", {"beep_on_start": str(value).lower()})

    def set_timeout_logical(self, value):
        return self.set("peripheryconfig", {"timeout_logical_0": value})

    def set_timeout_next_bit(self, value):
        return self.set("peripheryconfig", {"timeout_next_bit": value})


class TagIdentity(ApiClient):

    def get_params(self):
        return self.get("tagidentity")

    def get_tag_list(self):
        return self.get("tagidentity?taglist=true")

    def set_valid_time_ms(self, value):
        return self.set("tagidentity", {"validtime_ms": value})

    ###????
    def set_hold_time_ms(self, value):
        return self.set("tagidentity", {"hold_time_ms": value})

    def set_rssi_filter_value(self, value):
        return self.set("tagidentity", {"rssi_filter_value": -value})

    def set_rssi_filter_enable(self, value):
        return self.set("tagidentity", {"rssi_filter_enable": str(value).lower()})

    def set_epc_access_password(self, value):
        return self.set("tagidentity", {"epc_access_password": value})

    def set_epc_filter_value(self, value, filter):
        return self.set("tagidentity", {f"epc_filter_value{filter}": str(value).lower()})

    def set_epc_filter_enable(self, value, filter):
        return self.set("tagidentity", {f"epc_filter_enable{filter}": str(value).lower()})

    def set_beep_on_tag(self, value):
        return self.set("tagidentity", {"beep_on_tag": str(value).lower()})

    # def set_extra_mem_read(self, value):
    #     url = f"{self.base_url}/tagidentity?extra_mem_read=bool"
    #     data = {"extra_mem_read": value}
    #     response = requests.get(url, data=data)
    #     return response
    #
    # def set_extra_mem_bank(self, value):
    #     url = f"{self.base_url}/tagidentity?extra_mem_bank=value"
    #     data = {"extra_mem_bank": value}
    #     response = requests.get(url, data=data)
    #     return response
    #
    # def set_data_start_words(self, value):
    #     url = f"{self.base_url}/tagidentity?data_start_words=value"
    #     data = {"data_start_words": value}
    #     response = requests.get(url, data=data)
    #     return response
    #
    # def set_data_len_words(self, value):
    #     url = f"{self.base_url}/tagidentity?data_len_words=value"
    #     data = {"data_len_words": value}
    #     response = requests.get(url, data=data)
    #     return response

    def set_notify_uart(self, value):
        return self.set("tagidentity", {"notify_uart": str(value).lower()})

    def set_notify_uart_json(self, value):
        return self.set("tagidentity", {"notify_uart_json": value})

    def set_add_prefix(self, value):
        return self.set("tagidentity", {"add_prefix": value})

    def set_add_epcl(self, value):
        return self.set("tagidentity", {"add_epcl": str(value).lower()})

    def set_add_epc(self, value):
        return self.set("tagidentity", {"add_epc": str(value).lower()})

    def set_add_tidl(self, value):
        return self.set("tagidentity", {"add_tidl": str(value).lower()})

    def set_add_tid(self, value):
        return self.set("tagidentity", {"add_tid": str(value).lower()})

    # def set_add_suffix(self, value):
    #     return self.set("tagidentity", {"add_suffix": value})

    def set_add_crlf(self, value):
        return self.set("tagidentity", {"add_crlf": str(value).lower()})

    def set_add_ant(self, value):
        return self.set("tagidentity", {"add_ant": str(value).lower()})

    def set_add_rssi(self, value):
        return self.set("tagidentity", {"add_rssi": str(value).lower()})

    def set_notify_uart_alive(self, value):
        return self.set("tagidentity", {"notify_uart_alive": str(value).lower()})

    def set_notify_uart_speed(self, value):
        return self.set("tagidentity", {"notify_uart_speed": value})

    def set_notify_ip(self, value):
        return self.set("tagidentity", {"notify_ip": value})

    def set_notify_port(self, value):
        return self.set("tagidentity", {"notify_port": value})

    def set_notify_time_lim_ms(self, value):
        return self.set("tagidentity", {"notify_time_lim_ms": value})

    def set_notify_enable(self, value):
        return self.set("tagidentity", {"notify_enable": str(value).lower()})


class NetworkConfig(ApiClient):

    def get_netinfo(self):
        return self.get("netinfo")

    def set_sta_enable(self, value):
        return self.set("netinfo", {"sta_enable": str(value).lower()})

    def set_ap_enable(self, value):
        return self.set("netinfo", {"ap_enable": str(value).lower()})

    def set_wificonnect(self, ssid, password, safe):
        return self.set("wificonnect", {"ssid": ssid, "pass": password, "safe": safe})

    def scan_wifi(self):
        return self.get("scan")


class SystemCommands(ApiClient):
    def logout(self):
        return self.get("logout")

    def get_messagelog(self):
        return self.get("messagelog")

    def get_version(self):
        return self.get("version")

    def reboot(self):
        return self.get("reboot")

    def beep_device(self):
        return self.get("beepdevice")

    def inventory_once(self):
        return self.get("inventory_once")

    def saving_settings(self):
        return self.get("makedump")

    def set_relay(self):
        return self.get("relay1")
