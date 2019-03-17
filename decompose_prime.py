import time

time_start = time.time()
i = 2
while True:
#if 32416187567 % i == 0:
#    if 1299721 % i == 0:
#    if 15485867 % i == 0:
    if 179424691 % i == 0:
        print(i)
        break
    else:
        i = i + 1

print(time.time()-time_start)
