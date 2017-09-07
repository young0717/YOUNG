# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import thread
import time

class QSBK:
	
	def __init__(self):
		'''
		初始化参数
		'''
		self.page_index = 1
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = {'User-Agent': self.user_agent }
		#存储所有段子
		self.all_stories = []
		#程序运行标志
		self.enable = False
		
	def get_page(self, page_index):
		'''
		获取段子网页
		'''
		url = 'https://www.qiushibaike.com/hot/page/' + str(page_index)
		try:
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			page = response.read().decode('utf-8')
			return page
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print e.reason
			if hasatr(e, 'code'):
				print e.code
	
	def get_stories(self, page):
		'''
		获取每页的段子列表（包含用户名，内容，点赞数）
		'''
		pattern = re.compile(r'<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<!--(.*?)stats">.*?<i class="number">(.*?)</i>', re.S)
		items = re.findall(pattern, page)
		page_stories = []
		for item in items:
			haveImg = re.search(r'img', item[2])
			if not haveImg:
				page_stories.append([item[0].strip(), item[1].strip(), item[3].strip()])
		return page_stories
		
	def load_stories(self, page_stories):
		'''
		将每页段子列表加载到总段子列表中
		'''
		if self.enable:
			if len(self.all_stories) < 2:
				self.all_stories.append(page_stories)
				self.page_index += 1
				
	def load_stories_thread(self):
		'''
		多线程加载段子列表
		'''
		while self.enable:
			if len(self.all_stories) < 2:
				page = self.get_page(self.page_index)
				page_stories = self.get_stories(page)
				self.all_stories.append(page_stories)
				self.page_index += 1
			else:
				time.sleep(1)
				
	def show_story(self, page_stories, page_index):
		'''
		显示单个段子内容
		'''
		for story in page_stories:
			input = raw_input()
			if input == 'Q' or input == 'q':
				self.enable = False
				return
			print u'第%s页\t用户名：%s\n内容：%s\n点赞数：%s' % (page_index, story[0], story[1], story[2])
			
	def start(self):
		#单线程启动
		self.enable = True
		print u'正在连接糗百，按回车键继续，按“Q/q”退出'
		while self.enable:
			if len(self.all_stories) >= 0:
				now_index = self.page_index
				page = self.get_page(now_index)
				page_stories = self.get_stories(page)
				self.load_stories(page_stories)
				self.show_story(page_stories, now_index)
				del self.all_stories[0]
				
	def start_thread(self):
		#多线程启动
		self.enable = True
		now_index = self.page_index
		print u'正在连接糗百，按回车键继续，按“Q/q”退出'
		#新建线程在后台加载段子并存储
		thread.start_new_thread(self.load_stories_thread,())
		while self.enable:
			if len(self.all_stories) > 0:
				page_stories = self.all_stories[0]
				self.show_story(page_stories, now_index)
				del self.all_stories[0]
				now_index += 1
				

				
spider = QSBK()
#spider.start()
spider.start_thread()
