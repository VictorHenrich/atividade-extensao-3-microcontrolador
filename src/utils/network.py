import network
from core.settings import NETWORK_NAME, NETWORK_PASSWORD, NETWORK_IDENTITY


class Network:
    __wlan_instance = None

    @classmethod
    def connect_wifi(
        cls,
        network_name=NETWORK_NAME,
        network_password=NETWORK_PASSWORD,
        network_identity=NETWORK_IDENTITY,
    ):
        cls.__wlan_instance = network.WLAN(network.STA_IF)

        cls.__wlan_instance.active(True)

        other_params = {}

        if network_identity:
            other_params["eap"] = network.WLAN.EAP_PEAP

            other_params["identity"] = network_identity

        cls.__wlan_instance.connect(network_name, network_password, **other_params)

    @classmethod
    def disconnect_wifi(cls):
        if not cls.__wlan_instance:
            return

        cls.__wlan_instance.close()

        cls.__wlan_instance = None

    @classmethod
    def wifi_connected(cls):
        if not cls.__wlan_instance:
            return False

        return cls.__wlan_instance.isconnected()

    @classmethod
    def get_config(cls):
        if cls.__wlan_instance is None:
            return

        ip, subnet_mask, gateway, dns_server = cls.__wlan_instance.ifconfig()

        return {
            "ip": ip,
            "subnet_mask": subnet_mask,
            "gateway": gateway,
            "dns_server": dns_server,
        }

    @classmethod
    def scan_wifi(cls):
        if cls.__wlan_instance is None:
            return

        networks = cls.__wlan_instance.scan()

        wifi_list = []

        for ssid, bssid, channel, rssi, auth, hidden in networks:
            wifi_list.append(
                {
                    "ssid": ssid,
                    "bssid": bssid,
                    "rssi": rssi,
                    "channel": channel,
                    "auth": auth,
                    "hidden": hidden,
                    "mac_address": ":".join(f"{b:02x}" for b in bssid),
                    "signal_strength": rssi,
                }
            )

        return wifi_list
