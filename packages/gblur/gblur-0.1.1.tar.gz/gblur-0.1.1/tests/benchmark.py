import gblur
import time

runs = 6
average = 0.0
for i in range(runs):
    start = time.time()
    f = open("tests/cballs.png", 'rb')
    img = f.read()
    out = gblur.blur(img, radius=1)
    with open("tests/cballs_blurred.png", 'wb') as f:
        f.write(bytearray(out))
    average += (time.time() - start)

average = average / runs
print("Average runtime: %s seconds" % str(average))
