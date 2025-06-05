from yoomoney import Authorize

Authorize(client_id='5511A5F3CD6D40B86D88BCBBACFF46F2E198F338454A302C853F023146676F36',
          redirect_uri='https://t.me/VK_Music_Subscribition_bot',
          client_secret='D2B905D2A3E565A4C1691813D10DFE43CEEE580FA4E4016A220114ED99115CB7E611A49A2512A64FFF023E365A8DC9E1596C3158E0EC1719855B8570EE46B141',
          scope=['account-info',
                 'operation-history',
                 'operation-details',
                 'incoming-transfers',
                 'payment-p2p',
                 'payment-shop'])