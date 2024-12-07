s=input('введите строку: ')
ss=input('какой символ искать:')
print ('символ',ss,'встречается',s.count(ss),'раз')
for i in range(len(s)):
    if s[i]==ss:
        kol.append(i)
print("на следующих местах",kol)
