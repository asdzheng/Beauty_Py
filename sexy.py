#coding=utf-8
import requests
import urllib
import urllib2
import re
import random
import simplejson as json
from time import sleep
import grequests
import gevent

from PIL import Image
from multiprocessing import Pool

import threading, Queue

lock = threading.Lock()
queue = Queue.Queue()  #构造一个不限制大小的的队列
worker_num = 10  #设置线程的个数

i=200
img_num = 5612
miss_num = 0

class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.func = func  #传入线程函数逻辑

    def run(self) :
        self.func()

def main():

    baseUrl = 'https://v2.same.com'
    # next = '/channel/1015326/senses' 这是第一页
    next = '/channel/1015326/senses?offset=43882779' #这是第200页
    global i
    while  i < 205:
        i+=1
        url = baseUrl + next
        content=requests.get(url, timeout=10)
        jsonText = content.text
        jsonDict = json.loads(jsonText)
        # print 'code = ',jsonDict['code'],'jsonDict',jsonDict

        if jsonDict['code'] == 0 :
            data = jsonDict['data']
            next = data['next']
            print 'next = ', next

            imgs = []
            results = data['results']
            #得到目标图片url
            for r in results :
                sex = r['user']['sex']
                # print 'sex = ' , sex
                if sex != 1 :
                    img = r['photo']
                    if img != '':
                        imgs.append(img)

            for index in xrange(len(imgs)) :
                queue.put(imgs[index])

            threads = []
            for i in xrange(worker_num) :
                thread = MyThread(downloadImg)
                thread.start()  #线程开始处理任务
                print("第%s个线程开始工作") % i
                threads.append(thread)
            for thread in threads :
                thread.join()
            queue.join()

            #
            # for index in xrange(len(imgs)):
            #     threads.append(gevent.spawn(downloadImg, imgs[index]))
            # gevent.joinall(threads)

                # try:
                #     print "img = " + img
                #     path='g:\\spider\\same_beauty\\'+str(img_num)+'.jpg'
                #     #声明存储地址及图片名称
                #     urllib.urlretrieve(img,path)
                #     #下载图片
                #     print '下载了第'+str(img_num)+'张图片'
                #     img_num += 1
                #     #睡眠函数用于防止爬取过快被封IP
                # except:
                #     miss_num += 1
                #     print '抓漏',miss_num,'张'
        sleep(random.uniform(0.1,0.5))

def downloadImg() :
        try:
            global img_num

            global queue
            while not queue.empty():
                img = queue.get()
                print "img = " + img
                path='g:\\spider\\test\\'+str(img_num)+'.jpg'
                #声明存储地址及图片名称
                urllib.urlretrieve(img,path)
                # image=urllib2.urlopen(img).read()
                # file = open(path,'wb')
                # file.write(image)
                # file.close()
                #下载图片
                print '下载了第'+str(img_num)+'张图片'
                img_num += 1
                queue.task_done()
            #睡眠函数用于防止爬取过快被封IP
        except Exception as e:
            print (e)

            global miss_num

            miss_num += 1
            print '抓漏', miss_num,'张'

    #感觉这个话题下面美女多
    # headers={省略}
    # i=1
    # for x in xrange(20,3600,20):
    #     data={'start':'0',
    #     'offset':str(x),
    #     '_xsrf':'a128464ef225a69348cef94c38f4e428'}
    #     #知乎用offset控制加载的个数，每次响应加载20
    #     content=requests.post(url,headers=headers,data=data,timeout=10).text
    #     #用post提交form data
    #     imgs=re.findall('<img src=\\\\\"(.*?)_m.jpg',content)
    #     #在爬下来的json上用正则提取图片地址，去掉_m为大图
    #     for img in imgs:
    #         try:
    #             img=img.replace('\\','')
    #             #去掉\字符这个干扰成分
    #             pic=img+'.jpg'
    #             path='d:\\bs4\\zhihu\\jpg\\'+str(i)+'.jpg'
    #             #声明存储地址及图片名称
    #             urllib.urlretrieve(pic,path)
    #             urllib.
    #             #下载图片
    #             print u'下载了第'+str(i)+u'张图片'
    #             i+=1
    #             sleep(random.uniform(0.5,1))
    #             #睡眠函数用于防止爬取过快被封IP
    #         except:
    #             print u'抓漏1张'
    #         pass
    #     sleep(random.uniform(0.5,1))

if __name__=='__main__':
    main()
