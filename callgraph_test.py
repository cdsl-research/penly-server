def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def heavy_loop(n = 500000000):
    for i in range(n):
        calc()

    print("executed %d loop" % n)

def calc():
    1 + 2

def hello_world():
    print("Hello World!!")

def task(fib_num, heavy_loop_num):
    print("fib(%d) = %d" % (fib_num,fib(fib_num)))
    heavy_loop(heavy_loop_num)
    hello_world()

task(35, 10000000)