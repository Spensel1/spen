#x=0
#y=0
#
#while x<999999999999999999999999999999 and y<999999999999999999999999999999:
#    x=x+10
#    y=y+10
#    print(x, y)

#day=0
#x=int(input('сколько пробежал? '))
#y=int(input('скок хочешь? '))
#while x<y:
#    x=x+(x*10)/100
#    day=day+1
#    print('дней:', day, 'Километров:', x)

#import math
#a=int(input('От скольки:  '))
#b=int(input('До скольки:  '))
#for i in range(a,b+1):
#    if math.sqrt(i)==int(math.sqrt(i)):
#        print(i, '-точный квадрат')

#ves=int(input('Какой твой вес? '))
#or year in range(2021,2036):
#    print(year, 'Ваш вес на луне- ',ves*0.165)
#    ves+=1


import random
def draw_dors(n):
    if n==0:
        print('  [1]          [2]           [3]')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('||||||*||   |||||||*||   |||||||*||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
        print('|||||||||   ||||||||||   ||||||||||')
    elif n==1:
        print('  [1]          [2]           [3]')
        print(' ****       ||||||||||   ||||||||||')
        print('*******     ||||||||||   ||||||||||')
        print('*{}*{}*     ||||||||||   ||||||||||')
        print('*******     ||||||||||   ||||||||||')
        print('*******     |||||||*||   |||||||*||')
        print('*******     ||||||||||   ||||||||||')
        print('*******     ||||||||||   ||||||||||')
        print('*******     ||||||||||   ||||||||||')
        print('*******     ||||||||||   ||||||||||')
    elif n==2:
        print('   [1]          [2]          [3]')
        print('||||||||||     ****       ||||||||||')
        print('||||||||||    *******     ||||||||||')
        print('||||||||||    *{}*{}*     ||||||||||')
        print('||||||||||    *******     ||||||||||')
        print('|||||||*||    *******     |||||||*||')
        print('||||||||||    *******     ||||||||||')
        print('||||||||||    *******     ||||||||||')
        print('||||||||||    *******     ||||||||||')
        print('||||||||||    *******     ||||||||||')
    elif n==3:
        print('   [1]             [2]        [3]')
        print('||||||||||     ||||||||||    ****')
        print('||||||||||     ||||||||||   *******')
        print('||||||||||     ||||||||||   *{}*{}*')
        print('||||||||||     ||||||||||   *******')
        print('|||||||*||     |||||||*||   *******')
        print('||||||||||     ||||||||||   *******')
        print('||||||||||     ||||||||||   *******')
        print('||||||||||     ||||||||||   *******')
        print('||||||||||     ||||||||||   *******')
    
print(f'Вы играете в дом с приведениями!')
brave=True
score=0
while brave==True:
    ghost=random.randint(1,3)
    print(f'Пред вами три трухлявые гниющие двери, в одной из этих трухлявых и гниющих дверей находится призрак сериного убийцы который убил 1 милиард человек. В какую войдёш?')
    draw_dors(0)
    user=int(input())
    if not (user==1 or user==2 or user==3):
        brave=False
        print(f'Так как ты дебил и хотел нас обмануть мы тебя зарезали =-)')
        print(f'Вы прошли {score} дверей')
        break
    if user==ghost:
        brave=False
        draw_dors(ghost)
        print(f'Поздравляем вы вошли в неправельную трухлявую гниющую дверь и наткнулись на призрака серийного убийцы который убил 1 миллиард человек и вы здохли! ')
        
        print(f'Вы прошли {score} дверей')
    else:
        score+=1
        print(f'Вы прошли через одну из трёх трухлявых и гнилых дверей и не наткнулись на призрака серийного убийцы который убил 1 миллиард людей но так как вы прогляты навсегда в этом доме перед вами снова три трухлявых и гниющих дверей. В какую водёш?')
