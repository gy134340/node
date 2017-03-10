
# list
list = [1, 2, 3, 4]
it = iter(list)
for x in it:
    print(x)

# 多线程
def multiRun(url):
    count = 0
    while count < 1000:
        ra = random.randint(0, 200)
        count += 2
        print("%s: %s" % (ra, time.ctime(time.time())))
try:
    _thread.start_new_thread(multiRun, ('1',))
    _thread.start_new_thread(multiRun, ('2',))
except:
    print('error thread')
while 1:
    pass