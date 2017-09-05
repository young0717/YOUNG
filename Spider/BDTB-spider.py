# -*- coding: UTF-8 -*-

import urllib
import urllib2
import re
import os


#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:
	
	def __init__(self, base_url, see_lz, floor_tag):
		#URL基础地址
		self.base_url = base_url
		#只看楼主标志
		self.see_lz = ''.join(['?see_lz=', str(see_lz)])
		#调用替换工具
		self.tool = Tool()
		#结果保存为文件
		self.file = None
		#楼层变量
		self.floor = 1
		#文件标题
		self.defaultTitle = u'百度贴吧'
		#是否显示楼层标志
		self.floor_tag = floor_tag
		
	def getPage(self, page_num):
		pn = '&pn=' + str(page_num)
		try:
			url = ''.join([self.base_url, self.see_lz, pn])
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			#print response.read().decode('utf-8')
			return response.read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print u'连接百度贴吧失败，错误原因', e.reason
				
	def getTitle(self, page):
		pattern = re.compile(r'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
		result = re.search(pattern, page)
		if result:
			#print result.group(1)
			return result.group(1).strip()
			
	def getPageNum(self, page):
		pattern = re.compile(r'<li class="l_reply_num.*?</span>.*?red">(.*?)</span>', re.S)
		result = re.search(pattern, page)
		if result:
			#print result.group(1)
			return result.group(1).strip()
			
	def getContent(self, page):
		pattern = re.compile(r'<div id="post_content_.*?>(.*?)</div>', re.S)
		items = re.findall(pattern, page)
		contents = []
		for item in items:
			content = ''.join(['\n', self.tool.replace(item), '\n'])
			contents.append(content.encode('utf-8'))
		return contents
		
	def setFileTitle(self, title):
		if title is not None:
			self.file = open(title + '.txt', 'w+')
		else:
			self.file = open(self.defaultTitle + '.txt', 'w+')
			
	def writeData(self, contents):
		for item in contents:
			if self.floor_tag:
				floorLine = ''.join(['\n第', str(self.floor), '楼----------\n'])
				self.file.write(floorLine)
			self.file.write(item)
			self.floor += 1
		
	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print u'URL已失效，请重试'
		try:
			print u'该帖子共有'+str(pageNum)+u'页'
			for i in range(1, int(pageNum)+1):
				print u'正在写入第'+str(i)+u'页数据'
				page = self.getPage(i)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError, e:
			print u'写入异常，原因' + e.message
		finally:
			self.file.close()
			print u'写入完成'
			

print u'请输入帖子地址：'
base_url = str(raw_input())
print u'是否只获取楼主发言，是输入1，否输入0'
see_lz = raw_input()
print u'是否写入楼层信息，是输入1，否输入0'
floor_tag = raw_input()
bdtb = BDTB(base_url, see_lz, floor_tag)
print u'文件保存在' + os.getcwd() #获取当前工作目录
bdtb.start()