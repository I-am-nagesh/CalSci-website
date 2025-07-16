def home():
    from application_modules.home import home
    home()

def calculate():
    from application_modules.calculate import calculate
    calculate()


def graph():
    from application_modules.graph import graph_app
    graph_app()

def wifi():
    from application_modules.wifi_app import wifi_app
    wifi_app()

def wifi_connector(ssid):
    from application_modules.wifi_connector import wifi_connector
    wifi_connector(ssid)

def network_status_as():
    from application_modules.network_status import network_status
    network_status()

def chatbot():
    from application_modules.chatbot_ai import chatbot
    chatbot()

def settings():
    from application_modules.settings import settings
    settings()
    return 0

def disconnect_wifi():
    from application_modules.network_status import disconnect_network
    disconnect_network()

def backlight():
    from application_modules.backlight import toggle_backlight
    toggle_backlight()








