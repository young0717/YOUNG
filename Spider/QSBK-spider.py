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
		self.stories = []
		self.enable = False
		
	def getPage(self, page_index):
		'''
		获取网页
		'''
		url = 'https://www.qiushibaike.com/hot/page/' + str(page_index)
		try:
			request = urllib2.Request(url, headers=self.headers)
			response = urllib2.urlopen(request)
			content = response.read().decode('utf-8')
			return content
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u'connect failed,reason:', e.reason
	
	def getPageItems(self, page_index):
		'''
		获取每页的用户名，内容，点赞数
		'''
		content = self.getPage(page_index)
		if not content:
			print 'content error'
		pattern = re.compile(r'<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?<!--(.*?)stats">.*?<i class="number">(.*?)</i>', re.S)
		items = re.findall(pattern, content)
		pageStories = []
		for item in items:
			haveImg = re.search(r'img', item[2])
			if not haveImg:
				pageStories.append([item[0].strip(), item[1].strip(), item[3].strip()])
		return pageStories
		
	def loadPage(self):
		'''
		加载每页糗百内容
		'''
		if self.enable:
			if len(self.stories) < 2:
				pageStories = self.getPageItems(self.page_index)
				if pageStories:
					self.stories.append(pageStories)
					self.page_index += 1
					
	def getOneStory(self, pageStories, page):
		'''
		获取单个糗百内容
		'''
		for story in pageStories:
			input = raw_input()
			self.loadPage()
			if input == 'Q':
				self.enable = False
				return
			print u'第%s页\t用户名：%s\n内容：%s\n点赞数：%s' % (page, story[0], story[1], story[2])
			
	def start(self):
		print u'正在连接糗百，按回车键继续，按“Q”退出'
		self.enable = True
		self.loadPage()
		nowPage = 0
		while self.enable:
			if len(self.stories)>0:
				pageStories = self.stories[0]
				nowPage += 1
				del self.stories[0]
				self.getOneStory(pageStories, nowPage)
				
spider = QSBK()
spider.start()