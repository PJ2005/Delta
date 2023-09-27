# To create a tic-tac-toe grid
def grid(n):

    for i in range(1,n): #Row
        for j in range(n-1): #Column
            print("__|",end='')
        for k in range(1):
            print("__",end='')
        print()
    for i in range(1):
        for j in range(n-1):
            print("  |",end='')
        for k in range(1):
            print('  ',end='')


n = int(input("enter the square matrix order:"))
grid(n)