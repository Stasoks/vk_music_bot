from bot import connection, cursor
from config import *
from yoomoney import *
import requests

def user_exist(chatId):
    # Выполняем запрос
    cursor.execute("SELECT 1 FROM Users WHERE id = ?", (chatId,))
    result = cursor.fetchone()

    # Если результат найден — пользователь существует
    return result is not None

def check_payment(label):
    client = Client(YOOMONEY_TOKEN)
    history = client.operation_history(label=label)
    for operation in history.operations:
        if operation.status == "success":
            return True
    return False

def create_payment_link(order_id, amount=AMOUNT):
    url = 'https://platega.io/api/v1/invoice/create'
    headers = {'Authorization': f'Bearer {API_KEY}'}
    
    data = {
        'merchant_id': MERCHANT_ID,
        'amount': amount,
        'order_id': order_id,
        'description': f'Оплата заказа {order_id}',
        'success_url': 'https://t.me/VK_Music_Subscribition_bot',
        'fail_url': 'https://avatars.mds.yandex.net/i?id=48b9af7238e05e167884b66bca249050_l-5299999-images-thumbs&n=13'
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('payment_url')
    else:
        return None