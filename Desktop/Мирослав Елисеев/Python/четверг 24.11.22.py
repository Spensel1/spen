###работа с кортежами

#num=(1,2,3,4)
#num[0]=5
#print(num[0])

#пабота со словарями
#словарь={'ключ':'значение','ключ1':'значение1'}

#books={'У лукоморья дуб зелёный':'А.С.Пушкин',
#       'Маленький Принц':'Антуан де Сент-Экзюпери',
#       'Пикник у обочины':'А.Н.Стругацкий, Б.Н.Стругацкий'}
#print(books['Пикник у обочины'])
#del books['У лукоморья дуб зелёный']
#print(books)

###Условный Оператор

##age=13
#age=int (input())
#print(type(age))
#if age>20:
#    print('вы уже совсем взрослый')
#else:
#    print('ты школьник')
#print(age>20)

#name=input('как тебя зовут?')
#age=int (input(f'Солько тебе лет {name}?'))
#if age>20:
#    print('ема дед')
#else:
#    print('ема ты спиногрыз')

###Задача: 3 имени 3 возраста-кто старший?
#name1=input('Как зовут первого? ')
#ame2=input('Как зовут второго? ')
#name3=input('Как зовут третьего? ')
#age1=int (input(f'сколько лет {name1}? '))
#age2=int (input(f'сколько лет {name2}? '))
#age3=int (input(f'сколько лет {name3}? '))
#if age1>age2 and age1>age3:
#    print(name1, ' - самый старый')
#if age2>age1 and age2>age3:
#    print(name2, ' - самый старый')
#if age3>age1 and age3>age2:
#    print(name3, ' - самый старый')
#if age1==age2 and age1==age3:
#    print('все ровесники')
#if age1==age2 and age1>age3:
#    print(name1, 'и' ,name2, ' - одного возраста')
#if age3==age2 and age2>age1:
#    print(name1, 'и' ,name3, ' - одного возраста')
#if age1==age2 and age1>age3:
#    print(name2, 'и' ,name3, ' - одного возраста')


#python=input()
#if python=='python':
#    print('ДА')
#else:
#    print('НЕТ')

zarp=int (input())
if zarp<20000:
    print(zarp)
else:
    print(zarp-(zarp*13)/100)
