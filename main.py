import requests
import os
import time
import database
import json

TOKEN = os.environ.get('TOKEN')
URL = f'https://api.telegram.org/bot{TOKEN}/'


def getUpdates():
    url = URL + 'getUpdates'
    return requests.get(url).json()['result'][-1]

def start(chat_id):
    # print(chat_id)
    url = URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text' : 'Assalomu alaykum, iltimos tugmalardan birini bosing',
        'reply_markup': {
            'inline_keyboard' : [
                [{'text': 'Like', 'callback_data': 'like'}, {"text": 'Dislike', 'callback_data': 'dislike'}]
            ],
            'resize_keyboard': True,
        },
    }
    requests.get(url, json=payload)

## inline keyboard
# def start(chat_id):
#     print(chat_id)
#     url = URL + 'sendMessage'
#     payload = {
#         'chat_id': chat_id,
#         'text' : 'Assalomu alaykum, iltimos tugmalardan birini bosing',
#         'reply_markup': {
#             'inline_keyboard' : [
#                 [{'text': 'Like', 'callback_data': 'Like'}, {"text": 'Dislike', 'callback_data': 'Dislike'}], 
#             ],
#             'resize_keyboard': True
#         },
#     }
#     requests.get(url, json=payload)

def like(chat_id):
    url = URL + 'sendMessage'
    database.update_data('like')
    data = database.get_data()
    payload = {
        'chat_id': chat_id,
        'text': f"Likes: {data['like']}\nDislikes: {data['dislike']}",
        'reply_markup': {
            'inline_keyboard' : [
                [{'text': 'Like', 'callback_data': 'like'}, {"text": 'Dislike', 'callback_data': 'dislike'}]
            ],
            'resize_keyboard': True,
        },
    }
    requests.post(url, json=payload)

def dislike(chat_id):
    url = URL + 'sendMessage'
    database.update_data('dislike')
    data = database.get_data()
    payload = {
        'chat_id': chat_id,
        'text': f"Likes: {data['like']}\nDislikes: {data['dislike']}",
        'reply_markup': {
            'inline_keyboard' : [
                [{'text': 'Like', 'callback_data': 'like'}, {"text": 'Dislike', 'callback_data': 'dislike'}]
            ],
            'resize_keyboard': True,
        },
    }
    requests.post(url, json=payload)

def other():
    pass

def main():
    last_update_id = None
    while True:
        last_upd = getUpdates()
        curr_update_id = last_upd['update_id']
        if curr_update_id != last_update_id:
            last_update_id = curr_update_id
            if 'message' in last_upd and last_upd['message']['text'] == '/start':
                start(last_upd['message']['chat']['id'])
            elif 'callback_query' in last_upd and last_upd['callback_query']['data'] == 'like':
                like(last_upd['callback_query']['from']['id'])
            elif 'callback_query' in last_upd and last_upd['callback_query']['data'] == 'dislike':
                dislike(last_upd['callback_query']['from']['id'])
            else:
                other()
            # print(last_upd)
        time.sleep(2)


if __name__ == '__main__':
    main()