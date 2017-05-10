# This is here to be a base class, such that subclasses can specify which
#    fields should be included when serialized to JSON
class CustomJSON:
	_jsonattrs = []

	def get_dict(this):
		this_dict = {}
		for attr in this._jsonattrs:
			try:
				(attr, value) = this.get_attr(attr)
				this_dict[attr] = value
			except NoValue:
				pass

		return this_dict

	def get_attr(this, attr):
		if(',' in attr):
			(attr, options) = attr.split(',', 1)
			options = options.split(',')
		else:
			options = []
		(attr, value) = this.get_raw_attr(attr)
		return (attr, this.process_options(value, options))

	def get_raw_attr(this, attr):
		obj = None
		if(':' in attr):
			(attr, func) = attr.split(':', 1)
			obj = getattr(this, attr)
			if(hasattr(obj, func)):
				member = getattr(obj, func)
				if(callable(member)):
					obj = member()
				else:
					obj = member
		else:
			obj = getattr(this, attr)

		if(hasattr(obj, 'get_dict')):
			return (attr, obj.get_dict())
		elif(type(obj) == list):
			return (attr, [o.get_dict() if hasattr(o, 'get_dict') else o for o in obj])
		elif(type(obj) == dict):
			return (attr, {k : v.get_dict() if hasattr(v, 'get_dict') else v for k, v in obj.items()})
		return (attr, getattr(this, attr))

	def process_options(this, value, options):
		if('omitempty' in options):
			if(type(value) == int):
				if(value == 0):
					raise NoValue()
			elif(type(value) == float):
				if(value == 0.0):
					raise NoValue()
			elif(type(value) == str):
				if(value == ''):
					raise NoValue()
			elif(type(value) == list):
				if(len(value) == 0):
					raise NoValue()
			elif(type(vlaue) == dict):
				if(len(value) == 0):
					raise NoValue()
		return value

class NoValue(Exception):
	pass
