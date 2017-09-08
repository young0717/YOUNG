# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os
import requests
from bs4 import BeautifulSoup
import lxml

class Spider():

	def __init__(self, page_index):
		self.base_url = 'https://3344pu.com/tupianqu/zipai/'
		self.page_index = page_index
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = {'User-Agent': self.user_agent} #headers数据
		
	def get_page(self):
		url = self.base_url + str(self.page_index) + '.html'
		print u'正在连接' + url
		try:
			
			response = requests.get(url, headers=self.headers)
			response.encoding = 'utf-8'
			page = response.text
			#print page
			return page
		except requests.RequestException:
			print 'Error'

	def get_title(self, page):
		soup = BeautifulSoup(page, 'lxml')
		title = soup.h1.string
		print title
		return title

	def get_imgs(self, page):
		soup = BeautifulSoup(page, 'lxml')
		div = soup.find('div', class_='news')
		imgs = []
		for i in div:
			if i.name == 'img':
				src = i['src']
				imgs.append(src)
		#print imgs
		return imgs	

	def save_img(self, img_url, img_name):
		try:
			if not os.path.exists(img_name):
				img = requests.get(img_url, headers=self.headers)
				data = img.content #获取图片的bytes信息
				#print data
				f_img = open(img_name, 'wb') #写入图片二进制信息
				f_img.write(data)
				f_img.close()
				'''
				with open(img_name, 'wb') as f_img:
					f_img.write(data)
				'''
		except requests.RequestException:
			print 'Error'
		
	def save_imgs(self, imgs, path_name):
		number = 1
		print u'共有 %s 张需要下载，请稍等...' % len(imgs)
		for img_url in imgs:
			img_name = path_name + '/' + str(number) + '.jpg'
			print u'正在保存第%s张图片' %number
			self.save_img(img_url, img_name)
			number += 1
		
	def mk_dir(self, path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False
			
	def start(self, page_num):
		if not os.path.exists('F:\\Data\Spider'):
			os.makedirs('F:\\Data\Spider')
		os.chdir('F:\\Data\Spider') #更改工作目录
		for i in range(0, page_num):
			print u'共要下载%s组图片，当前下载第%s组...' %(page_num, i+1)
			page = self.get_page()
			title = self.get_title(page)
			imgs = self.get_imgs(page)
			self.mk_dir(title)
			self.save_imgs(imgs, title)
			self.page_index -= 1
		print u'全部图片抓取完成，请查看。'
		
spider = Spider(257395) #初始网址257403
spider.start(10)
