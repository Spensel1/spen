#Модули

#import time
#print(time.asctime())

#import sys
#while True:
#    ans=input('Что-то пошло не так?\n')
#    if ans=='да':
#        print('окей придётся прервать работу программы')
#        sys.exit()
#    print('всё хорошою, продолжаем')

##import math
#from math import sqrt
#a=int(input('Введите коэффицент квадратного уравнения A:'))
#b=int(input('Введите коэффицент квадратного уравнения B:'))
#c=int(input('Введите коэффицент квадратного уравнения C:'))
#d=b**2-4*a*c
#if d<0:
#    print("уравнение с такими коэффицентами не имеет корней")
#if d==0:
#    x=-b/2*a
#    print(f'уравнение имеет один корень x={x}')
#if d>0:
#    x1=(-b+math.sqrt(d))/(2*a)
#    x2=(-b-math.sqrt(d))/(2*a)
#    print('уравнение имеет два корня')
#    print('x1=',x1)
#    print('x2=',x2)

#from math import *
#import sys
#def kvadr_ur (a,b,c):
#    d=b**2-4*a*c
#    if d<0:
#        print("уравнение с такими коэффицентами не имеет корней")
#    if d==0:
#        x=-b/2*a
#        print(f'уравнение имеет один корень x={x}')
#    if d>0:
#        x1=(-b+sqrt(d))/(2*a)
#        x2=(-b-sqrt(d))/(2*a)
#        print('уравнение имеет два корня')
#        print('x1=',x1)
#        print('x2=',x2)
#while True:        
#    a=int(input('Введите коэффицент квадратного уравнения A:'))
#    b=int(input('Введите коэффицент квадратного уравнения B:'))
#    c=int(input('Введите коэффицент квадратного уравнения C:'))
#    kvadr_ur (a,b,c)
#    ans=input('Решаем дальше?')
#    if ans=='нет':
#        print('окей придётся прервать работу программы')
#        sys.exit()

'''print(' работа функции float')
a='12.25'
print(float(a)+5)
print(float(a)+0.75)
print(' работа функции int')
print(int(123.12345678))
print(('1000 ')*999)
print('23423'*100)
print('10101010101010=',int('10101010101010',2))
print('1ff2a=',int('1ff2a',16))'''

m=max(123,34,456,67,79,99910)
print(m)
my_list=[123,34,456,67,79,99910]
print(min(my_list))
print(max(my_list))

       
