#for i in range(1,101):
#   print(i,"Hello world!",end=", ")
'''
a=int(input("Введите первое число: "))
b=int(input("Введите второе число: "))
print('Выберите операцию: \n 1 -"+", 2 - "-", 3 - "*", 4 - "/" ')
operation=input()
if operation=='1':
    print(a,'+',b,'=',a+b)
elif operation == '2':
    print(a, '-', b, '=', a - b)
elif operation=='3':
    print(a,'*',b,'=',a * b)
elif operation == '4':
    if b!=0:
        print(a, '/', b, '=', a/b)
    else:
        print('На ноль делить нельзя')
else:
    print('неверный ввод')
'''

#n=int(input())
#for i in range(n):
#    a=int(input())
#    if a%3==0:
#        if a<maxx:
#            maxx=a
#print (maxx)

import telebot
bot=telebot.TeleBot('6516242122:AAESZYHFVDUUbBapYWEpUDLXxp5tMol_QGk')
greetings =["Привет", "Здравствуй", "Добрый день"]
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Здравствуй человек")
bot.infinity_polling()