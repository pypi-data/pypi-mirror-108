
class xesapp():
	
	def __init__(self, pid):
		
		self.pid = pid.split("&pid=")[1].split("&")[0]
		self.updata()
		self.like = self.data["likes"]
		self.unlike = self.data["unlikes"]
		self.last_comments=self.data["comments"]
	def updata(self):
		
		import requests
		url = "http://code.xueersi.com/api/compilers/" + self.pid + "?id=" + self.pid
		headers = {'Content-Type': 'application/json'}
		a = requests.get(url=url, headers=headers)
		a = self._nice(a.text).replace("false", "False").replace("true", "True").replace("null", "None")
		z = eval(a)
		# self._nice()
		self.data = z["data"]
	def get_modified(self):
		return self.data["modified_at"]
	def get_published(self):
		return self.data["published_at"]
	def get_view(self):
		
		return self.data["views"]
	def get_cover(self):
		
		return self.data["thumbnail"]
	def load_cover(self, savaname):
		

		def load(url, name):
			import requests as req
			response = req.get(url)
			try:
				a = open(name, "wb")
				a.write(response.content)
				a.close()
			except:
				a = open(name, "w")
				a.write(response.text)
				a.close()

		load(self.data["thumbnail"], savaname)
	def get_hot(self):
		
		return self.data["popular_score"]
	def is_like(self):
		
		self.updata()
		like = self.data["likes"]
		unlike = self.data["unlikes"]
		if int(self.like) < int(like):
			return True
		elif int(self.unlike) < int(unlike):
			return False
		else:
			return None
	def get_like(self, updata=False):
		
		if updata:
			self.updata()
		return self.data["likes"]
	def get_unlike(self, updata=False):
		
		if updata:
			self.updata()
		return self.data["unlikes"]
	def run_app(self):
		
		self.load_file()
		exec(self.get_code())
	def _nice(self, emoji_str):
		import struct
		return ''.join(
			c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in
			emoji_str)
	def get_code(self):
		
		return self._nice(self.data["xml"])
	def load_file(self, cache=""):
		

		def load(url, name):
			import requests as req
			response = req.get(url)
			try:
				a = open(name, "wb")
				a.write(response.content)
				a.close()
			except:
				a = open(name, "w")
				a.write(response.text)
				a.close()

		k = self.data["assets"]["assets"]
		for x in k:
			load(("https://livefile.xesimg.com/programme/python_assets/" + x["md5ext"]), cache + x["name"])
	def is_hidden_code(self):
		if self.data["hidden_code"]==2:
			return True
		else:
			return False
	def get_description(self):
		return self.data["description"]
	def get_comments(self):
		return self.data["comments"]
	def is_comments(self):
		if self.data["comments"]>self.last_comments:
			return True
		else:
			return False


class cmt:
	def __init__(self,pid):
		self.pid = pid.split("&pid=")[1].split("&")[0]
		self.updata()
		self.dta_dic=self._in_dta(self.data)
	def _nice(self, emoji_str):
		import struct
		return ''.join(
			c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in
			emoji_str)
	def updata(self):
		
		import requests
		s = requests.Session()
		url = "http://code.xueersi.com/api/comments?appid=1001108&topic_id=CP_{pid}&parent_id=0&order_type=&page=1&per_page=15".replace("{pid}",self.pid)
		a = s.get(url=url, headers={'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate',
			  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
			  'Cookie': 'xesId=b524835904a4a420cba3dde34890bade; user-select=scratch;  xes_run_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIuY29kZS54dWVlcnNpLmNvbSIsImF1ZCI6Ii5jb2RlLnh1ZWVyc2kuY29tIiwiaWF0IjoxNjAxODA5NDcxLCJuYmYiOjE2MDE4MDk0NzEsImV4cCI6MTYwMTgyMzg3MSwidXNlcl9pZCI6bnVsbCwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvODUuMC40MTgzLjEyMSBTYWZhcmlcLzUzNy4zNiBFZGdcLzg1LjAuNTY0LjY4IiwiaXAiOiIxMTIuNDkuNzIuMTc1In0.9bXcb813GhSPhoUJkezZpV8O50ynm0hhYvszNyczznQ; prelogid=ef8f6d12febabf75bf9599744b73c6f5; xes-code-id=87f66376f1afd34f70339baeca61b7a1.8dbd833da9122d69a17f91054066dbb3; X-Request-Id=82f1c3968c8ff01ee151a0413f56aa84; Hm_lpvt_a8a78faf5b3e92f32fe42a94751a74f1=1601809487',
			  'Host': 'code.xueersi.com', 'Proxy-Connection': 'keep-alive',
			  'Referer': 'http://code.xueersi.com/space/11909587',
			  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.68'})
		a = self._nice(a.text).replace("false", "False").replace("true", "True").replace("null", "None")
		z = eval(a)
		print(z)
		# self._nice()
		self.data = z["data"]["data"]
	def _in_dta(self,data):
		dta_dic = []
		for x in data:
			kk={}
			kk["user_id"] = x["user_id"]
			kk["content"] = x["content"]
			kk["created_at"] = x["created_at"]
			kk["data"]=kk["created_at"]
			kk["username"]=x["username"]
			kk["reply_username"] = x["reply_username"]
			kk["likes"]=x["likes"]
			z=x["reply_list"]["data"]
			z_list=[]
			for n in z:
				k = {}
				k["user_id"] = n["user_id"]
				k["content"] = n["content"]
				k["created_at"] = n["created_at"]
				k["reply_username"] = n["reply_username"]
				k["username"] = n["username"]
				z_list.append(k)

			kk["reply_list"]=z_list

			dta_dic.append(kk)
		return dta_dic
	def sorted(self,sort_by="likes",reverse=True):
		if sort_by=="likes":
			def sort(z):
				return z["likes"]
		elif sort_by=="data":
			def sort(z):
				return z["data"]
		self.dta_dic=sorted(self.dta_dic,key=sort,reverse=reverse)
		return self.dta_dic
	def fmt(self):
		str=""
		for x in self.dta_dic:
			str+="["+x["created_at"]+"]\n\t"+x["username"]+"回复"+x["reply_username"]+":"+x["content"].replace("\n","\n\t")+"\n"

			for y in x["reply_list"]:
				str += "\t[" + y["created_at"] + "]\n\t\t" + y["username"] + "回复" + y["reply_username"] + ":" + y[
					"content"].replace("\n","\n\t\t") + "\n"
			str += "\n"
		return str
