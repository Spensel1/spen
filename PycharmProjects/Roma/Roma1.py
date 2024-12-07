def game(n,s):
    if n==2 and s>=129:
        return n==2

    if n%2==0:
      return all (game(n+1,s+1), game(n+1,s*2))
    return any (game(n+1,s+1), game(n+1,s*2))

    for i in range(1,128):
        if game(0,i):
            print(i)
            break


def game(n,s):
 if n==3 and s>=129:
        return n==3
       if n%2!=0:
      return game (game(n+1,s+1), game(n+1,s*2))
    return game (game(n+1,s+1) or game(n+1,s*2))

 for i in range(1,128):
        if game(0,i):
            print(i)