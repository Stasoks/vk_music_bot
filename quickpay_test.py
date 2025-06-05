from yoomoney import Client
from yoomoney import Quickpay

client = Client("4100119173374580.B3AD0D89901C879FD6A254DDBC3EE13C7470408AEE492164ABFFDBFA41EF0E37E2F14535F7282A6A11C5EE868DC4296966A339857B3692A3ED21E080B01200F3866ABB68C032D566DBBA7CDE3D7C4CABE8DE2B641B2399F35E00DA47A56D52079A10D4A8360E5E60A3B0A672FDDC8F3CAE59DAF01DC3CE40E9D7E1BE980BE25A")

payment = Quickpay(receiver='4100119173374580', 
                   quickpay_form='shop',
                   targets='АГУША РАСТИШКА КУПИ КУПИ КУПИ', 
                   paymentType='SB', 
                   sum = 2, 
                   label = '89218420090')

print(payment.base_url, payment.redirected_url, sep='\n')


