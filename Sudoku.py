import math
import time 

class Sudoku:
	sn = []
	d = []
	missingList = []

	def __init__(self, sn, boxHeight = False, boxWidth = False):
		self.sn = sn
		self.missingList = self.getMissingList()

		self.d = dict()
		if boxWidth == False:
			self.d['boxWidth'] = int(math.ceil(math.sqrt(self.rowNumber())))
		else:
			self.d['boxWidth'] = boxWidth
		if boxHeight == False:
			self.d['boxHeight'] = int(math.floor(math.sqrt(self.colNumber())))
		else:
			self.d['boxHeight'] = boxHeight

		self.d['sepRow'] = range(self.d['boxHeight'] - 1, self.rowNumber() - self.d['boxHeight'],
		 				   self.d['boxHeight']) #[2,5]
		self.d['sepCol'] = range(self.d['boxWidth'] - 1, self.colNumber(), self.d['boxWidth']) #[2,5,8]
		self.d['numbers'] = self.d['boxWidth'] * self.d['boxHeight']

	def __str__(self):
		return self.nicePrint()

	def rowNumber(self):
		return len(self.sn)

	def colNumber(self):
		return len(self.sn[0])

	def getCompletion(self):
		totalPlaces = 0
		missingPlaces = 0
		for i in range (0, self.rowNumber()):
			for j in range(0, self.colNumber()):
				totalPlaces += 1
				if self.sn[i][j] == 0:
					missingPlaces += 1

		return (missingPlaces, totalPlaces)

	def nicePrint(self):
		ss = '\n'
		sepRow = self.d['sepRow']
		sepCol = self.d['sepCol']
		for i in range (0, self.rowNumber()):
			for j in range(0, self.colNumber()):
				ss = ss + str(self.sn[i][j]) + ' '
				if j in sepCol:
					ss = ss + '   '
			ss = ss + '\n'
			if i in sepRow:
				ss = ss + '\n'
		(missingPlaces, totalPlaces) = self.getCompletion()
		ss += '\n' + 'Completion: ' + str(totalPlaces - missingPlaces) + ' / ' + str(totalPlaces)
		return ss

	def validRow(self, row):
		nList = [0] * self.colNumber()
		for i in range(0, self.colNumber()):
			el = self.sn[row][i]
			if el != 0:
				nList[el - 1] += 1
				if nList[el - 1] > 1:
					return False
		return True

	def validCol(self, col):
		nList = [0] * self.rowNumber()
		for i in range(0, self.rowNumber()):
			el = self.sn[i][col]
			if el != 0:
				nList[el - 1] += 1
				if nList[el - 1] > 1:
					return False
		return True

	def validBox(self, row, col):
		numbers = self.d['numbers']
		boxWidth = self.d['boxWidth']
		boxHeight = self.d['boxHeight']

		minHeight = int(math.floor(row/boxHeight)) * boxHeight
		maxHeight = (int(math.floor(row/boxHeight)) + 1) * boxHeight
		minWidth = int(math.floor(col/boxWidth)) * boxWidth
		maxWidth = (int(math.floor(col/boxWidth)) + 1) * boxWidth

		nList = [0] * numbers
		for i in range(minHeight, maxHeight):
			for j in range (minWidth, maxWidth):
				el = self.sn[i][j]
				if el != 0:
					nList[el - 1] += 1
					if nList[el - 1] > 1:
						return False
		return True

	def fillKnownSingle(self):
		numbers = self.d['numbers']
		for i in range (0, self.rowNumber()):
			for j in range(0, self.colNumber()):
				if self.sn[i][j] == 0:
					lastNumber = 0
					validNumbers = 0
					for k in range (1, numbers + 1):
						self.sn[i][j] = k
						if self.validRow(i) and self.validCol(j) and self.validBox(i,j):
							lastNumber = k
							validNumbers += 1
							if validNumbers > 1:
								break
					if validNumbers > 1:
						self.sn[i][j] = 0
					else:
						self.sn[i][j] = lastNumber

	def fillKnown(self):
		oldMissingPlaces = -1
		missingPlaces = self.getCompletion()

		while oldMissingPlaces != missingPlaces:
			self.fillKnownSingle()
			oldMissingPlaces = missingPlaces
			missingPlaces = self.getCompletion()

		self.missingList = self.getMissingList()

	class MissingNumber():
		i = 0
		j = 0
		t = 1
		def __init__(self, i, j):
			self.i = i
			self.j = j
		def __str__(self):
			return '[' + str(self.i) + ',' + str(self.j) + ']: ' + str(self.t)

	def getMissingList(self):
		missingList = []
		for i in range (0, self.rowNumber()):
			for j in range(0, self.colNumber()):
				if self.sn[i][j] == 0:
					mn = self.MissingNumber(i,j)
					missingList.append(mn)
		return missingList

	def clearMissing(self):
		missingList = self.missingList
		for mn in missingList:
			self.sn[mn.i][mn.j] = 0

	def solveIterative(self):
		missingList = self.missingList
		numbers = self.d['numbers']
		i = 0
		while i < len(missingList):
			if i < 0:
				return False
			mn = missingList[i]
			if mn.t == numbers + 1:
				self.sn[mn.i][mn.j] = 0
				mn.t = 1
				i -= 1
				continue
			for j in range(mn.t, numbers + 1):
				self.sn[mn.i][mn.j] = j
				mn.t = j + 1
				if self.validRow(mn.i) and self.validCol(mn.j) and self.validBox(mn.i,mn.j):
					i += 1
					break
				elif j == numbers:
					self.sn[mn.i][mn.j] = 0
					mn.t = 1
					i -= 1
		return True

	def solve(self):
		self.fillKnown()
		return self.solveIterative()

	def analyze(self):
		print 'Original sudoku'
		print '================='
		print self
		print '\nSolved sudoku'
		print '================='
		t = time.time()
		solved = self.solve()
		elapsed = time.time() - t
		if solved:
			print self
		else:
			print 'ERROR: Sudoku cannot be solved'
		print 'Time: ' + str(elapsed)

		countSolutions = False
		nSolutions = 1
		while True:
			self.clearMissing()
			solved = self.solveIterative()
			if solved:
				nSolutions += 1
				if countSolutions == False:
					print 'ERROR: Sudoku has multiple solutions'
					break
				else:
					print self
			else:
				break
		if nSolutions > 1 and countSolutions == True:
			print 'ERROR: Sudoku has ' + str(nSolutions) + ' solutions'

if __name__ == '__main__':
	import time

	#Multiple
	si = [[0,0,0, 0,0,0, 0,0,0],
		  [0,0,0, 0,0,0, 0,0,0],
		  [8,0,0, 0,0,0, 0,0,0],

		  [0,0,0, 0,0,0, 0,0,0],
		  [0,0,0, 0,0,0, 0,0,0],
		  [0,0,0, 0,0,0, 0,0,0],

		  [0,0,0, 0,0,0, 0,0,0],
		  [0,0,0, 0,0,0, 0,0,0],
		  [0,0,0, 0,0,0, 0,0,0]]

	#Diagonal	  
	sd = [[5,0,0, 0,0,0, 0,0,0],
		  [0,5,0, 0,0,0, 0,0,0],
		  [0,0,5, 0,0,0, 0,0,0],

		  [0,0,0, 5,0,0, 0,0,0],
		  [0,0,0, 0,5,0, 0,0,0],
		  [0,0,0, 0,0,5, 0,0,0],

		  [0,0,0, 0,0,0, 5,0,0],
		  [0,0,0, 0,0,0, 0,5,0],
		  [0,0,0, 0,0,0, 0,0,5]]

	#Easy
	se = [[7,9,0, 0,0,0, 3,0,0],
		  [0,0,0, 0,0,6, 9,0,0],
		  [8,0,0, 0,3,0, 0,7,6],

		  [0,0,0, 0,0,5, 0,0,2],
		  [0,0,5, 4,1,8, 7,0,0],
		  [4,0,0, 7,0,0, 0,0,0],

		  [6,1,0, 0,9,0, 0,0,8],
		  [0,0,2, 3,0,0, 0,0,0],
		  [0,0,9, 0,0,0, 0,5,4]]

  	#Hard
	sh = [[1,0,0, 0,7,0, 0,3,0],
		  [8,3,0, 6,0,0, 0,0,0],
		  [0,0,2, 9,0,0, 6,0,8],

		  [6,0,0, 0,0,4, 9,0,7],
		  [0,9,0, 0,0,0, 0,5,0],
		  [3,0,7, 5,0,0, 0,0,4],

		  [2,0,3, 0,0,9, 1,0,0],
		  [0,0,0, 0,0,2, 0,4,3],
		  [0,4,0, 0,8,0, 0,0,9]]

	#Extreme
	sm = [[6,0,0, 0,0,0, 0,4,0],
		  [0,0,5, 0,0,2, 0,0,7],
		  [7,2,9, 0,0,0, 0,0,3],

		  [0,9,0, 0,4,0, 0,0,1],
		  [0,0,0, 0,6,0, 0,0,0],
		  [4,0,0, 0,8,0, 0,7,0],

		  [3,0,0, 0,0,0, 1,6,5],
		  [2,0,0, 4,0,0, 8,0,0],
		  [0,5,0, 0,0,0, 0,0,4]]  

	#Telegraph
	st = [[8,0,0, 0,0,0, 0,0,0],
		  [0,0,3, 6,0,0, 0,0,0],
		  [0,7,0, 0,9,0, 2,0,0],

		  [0,5,0, 0,0,7, 0,0,0],
		  [0,0,0, 0,4,5, 7,0,0],
		  [0,0,0, 1,0,0, 0,3,0],

		  [0,0,1, 0,0,0, 0,6,8],
		  [0,0,8, 5,0,0, 0,1,0],
		  [0,9,0, 0,0,0, 4,0,0]]  

	#Irregular
	si = [[0,0,3, 0,5,0],
		  [2,4,5, 0,3,0],

		  [0,0,0, 0,6,2],
		  [1,2,0, 0,0,0],

		  [0,5,0, 3,1,6],
		  [0,6,0, 4,0,0]]  

	s = Sudoku(se)
	s.analyze()