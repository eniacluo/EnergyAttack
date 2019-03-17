import random
import time

time_start = time.time()
for i in range(10000):
    with open('write_file.tmp', 'w+') as f:
        f.write(str([random.random()]*100))

print(time.time()-time_start)
