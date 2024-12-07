print('''Подсказки:
камень-1
ножницы-2
бумага-3
''')
from random import *
main_list=['Камень','Ножницы','Бумага']
restart_game=True
wins_comp=wins_user=0
comp_change=choice(main_list)
while restart_game:
    comp_change=choice(main_list)
    ask=input('Ваш выбор: ')
    if ask=='1':
        user_change=main_list[0]
    elif ask=='2':
        user_change=main_list[1]
    elif ask=='3':
        user_change=main_list[2]
    else:
        print('Неправильно, попрой ещё раз!')
        continue
    print('Компьютер:',comp_change)
    if user_change==comp_change:
        print('Никто не выйграл.')
    
    if user_change==main_list[0] and comp_change==main_list[1]:
        print('Вы выйграли!.')
        wins_user+=1
    if user_change==main_list[1] and comp_change==main_list[0]:
        print('Компьютер выйграл!.')
        wins_comp+=1
    if user_change==main_list[1] and comp_change==main_list[2]:
        print('Вы выйграли!.')
        wins_user+=1
    if user_change==main_list[2] and comp_change==main_list[1]:
        print('Компьютер выйграл!.')  
        wins_comp+=1
    if user_change==main_list[2] and comp_change==main_list[0]:
        print('Вы выйграли!.')
        wins_user+=1
    if user_change==main_list[0] and comp_change==main_list[2]:
        print('Компьютер выйграл!.')
        wins_comp+=1
    print('''
Ваши победы-''',wins_user)
    print('Победы компьютера-',wins_comp)
    print('''
Хотите продолжить? (да/нет)''')
    yes_no=input()
    if yes_no=='нет':
        restart_game=False
