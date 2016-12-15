from __future__ import division

class Neighbor(object):
	def __init__(self, addr, ssid, channel, signal, quality):
		self.addr = addr
		self.ssid = ssid
		self.id = id
		self.channel = int(channel)
		self.signal = int(signal)
		self.qualityStr = quality
		self.quality = eval(quality)

	def getAddr(self):
		return self.addr

	def getSsid(self):
		return self.ssid

	def getId(self):
		return self.id

	def getChannel(self):
		return self.channel

	def getSignal(self):
		return self.signal

	def getQuality(self):
		return self.quality

	def __hash__(self):
		r = 0
		for c in self.addr:
			r += ord(c)
		return r

	def __eq__(self, other):
		return self.__hash__() == other.__hash__()


class Neighbors(object):
	def __init__(self, n, wtp):
		self.neighbors = n
		self.wtp = wtp

	def to_dict(self):
		return { }