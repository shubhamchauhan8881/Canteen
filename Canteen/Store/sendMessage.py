from django.conf import settings
import requests
import asyncio

BASE_URL = "https://api.telegram.org/bot"



MESSAGE_TEMPLATE ="""

__New Order Recieved__

*\Order Details*
Order id: *\%s*

Items:
%s

*\Customer details*
Name: %s
Phone: %s
Address: %s

"""
async def _make_request(url,data):
    requests.post(
        url, 
        data=data,
        timeout=5000,
    )
    # print(re.content)


def send(data, to):
    try:
        action = "sendMessage"
        # url = "https://api.telegram.org/bot<token>/sendMessage"
        url = BASE_URL + settings.TELEGRAM_BOT_KEY + "/" + action
        data = {
            "text": MESSAGE_TEMPLATE%data,
            "parse_mode": "MarkdownV2",
            }

        if len(to) > 1:
            for i in to:
                data["chat_id"] = i
                asyncio.run(_make_request(url, data))
        else:
            data["chat_id"] = to[0]
            asyncio.run(_make_request(url, data))
    except Exception as e:
        print(e)
