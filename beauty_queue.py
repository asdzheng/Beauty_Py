#coding=utf-8
import requests
import urllib
import urllib2
import random
import simplejson as json
from time import sleep

from PIL import Image
from multiprocessing import Pool

import gevent
from gevent.queue import Queue, Empty

def main():

    global next
    global baseUrl
    global i
    while i < 400:
        i+=1
        print "i = ", i

        url = baseUrl + next
        content=requests.get(url, timeout=100)
        jsonText = content.text
        jsonDict = json.loads(jsonText)
        # print 'code = ',jsonDict['code'],'jsonDict',jsonDict

        if jsonDict['code'] == 0 :
            data = jsonDict['data']
            next = data['next']
            print 'next = ', next

            # imgs = []
            results = data['results']
            #得到目标图片url
            for r in results :
                sex = r['user']['sex']
                # print 'sex = ' , sex
                if sex != 1 :
                    img = r['photo']
                    if img != '':
                        tasks.put(img)
                        # print "tasks sieze = ", tasks.qsize
                    # imgs.append(img)

            # for index in xrange(len(imgs)) :
            #     queue.put(imgs[index])

            # threads = []
            # for i in xrange(worker_num) :
            #     thread = MyThread(downloadImg)
            #     thread.start()  #线程开始处理任务
            #     print("第%s个线程开始工作") % i
            #     threads.append(thread)
            # for thread in threads :
            #     thread.join()
            # queue.join()
        print "gevent sleep "
        gevent.sleep(random.uniform(0.5,1))

def downloadImg() :
        try:
            print "current = ", id(gevent.getcurrent())
            gevent.sleep(0.001)
            global img_num

            global tasks
            while True:
                img = tasks.get(timeout=1)
                print "img = " + img
                path='g:\\spider\\same_beauty\\'+str(img_num)+'.jpg'
                #声明存储地址及图片名称
                urllib.urlretrieve(img,path)
                # image=urllib2.urlopen(img).read()
                # file = open(path,'wb')
                # file.write(image)
                # file.close()
                #下载图片
                print '下载了第'+str(img_num)+'张图片'
                img_num += 1
                # tasks.
        except Empty:
            print '没有数据啦~~~~'
        except Exception as e:
            print (e)

            global miss_num
            miss_num += 1
            print '抓漏', miss_num,'张'



if __name__ == '__main__':
    tasks = Queue()  #构造一个不限制大小的的队列

    i = 200
    img_num = 5612
    miss_num = 0

    baseUrl = 'https://v2.same.com'
    # next = '/channel/1015326/senses' 这是第一页
    next = '/channel/1015326/senses?offset=43882779' #这是第200页

    threads = []
    threads.append(gevent.spawn(main))
    for index in xrange(20) :
        threads.append(gevent.spawn(downloadImg))
    gevent.joinall(threads)
