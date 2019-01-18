
class Main(object):

	def __init__(self,extensions=[]):
		self.reports = Reports(self)
		self._data = [i for i in range(1,101)]
		self._extensions = extensions
		self._result_data_ext_fn = []
		self.inject()

	@property
	def injectables(self):
		return {'result_fn':self._result_data_ext_fn }

	def inject(self):
		for e in self._extensions:
			e.inject(self.injectables)

	def result_data(self):
		data_dic = {'main_data':self._data}
		for fn in self.injectables['result_fn']:
			data_dic = fn(data_dic)
		return data_dic

class Reports(object):
	def __init__(self,parent):
		self.p = parent

	def print_fiss_buzz_ans(self):
		data_dic = self.p.result_data()
		for num, fiss, buzz in zip(data_dic['main_data'],data_dic['fiss'],data_dic['Buzz']):
			print(num if fiss + buzz == '' else fiss + buzz)

class ext(object):
	def inject(self,injectables):
		raise NotImplementedError()

class Fiss(ext):
	def inject(self,injectables):
		def add_fiss(data_dic):
			data_dic['fiss'] = ['fiss' if i%3 == 0 else '' for i in data_dic['main_data']]
			return data_dic
		injectables['result_fn'].append(add_fiss)

class Buzz(ext):
	def inject(self,injectables):
		def add_buzz(data_dic):
			data_dic['Buzz'] = ['Buzz' if i%5 == 0 else '' for i in data_dic['main_data']]
			return data_dic
		injectables['result_fn'].append(add_buzz)


M = Main(extensions=[Fiss(),Buzz()])

M.reports.print_fiss_buzz_ans()
