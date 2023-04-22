# This Python file uses the following encoding: utf-8
import sys
import queue
import random
import math
from pathlib			import Path
from PySide6.QtCore		import QTimer, QObject, Slot, Signal, Property
from PySide6.QtGui		import QGuiApplication
from PySide6.QtQml		import QQmlApplicationEngine, QmlElement
from PySide6.QtQuick	import QQuickImageProvider
from PIL				import Image, ImageQt


_sneakyResetFunction = None

def sneakyResetFunction():
	_sneakyResetFunction()

QML_IMPORT_NAME = "nl.jorisgoosen.Segregation"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Bridge(QObject):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._intolerance = 0.5
		self._similarity = 0.333333
		self._maxMigration = 0
		self._maxKids = 0.5

	@Property('float')
	def intolerance(self):
		return self._intolerance


	@Property('float')
	def similarity(self):
		return self._similarity

	@Property('float')
	def maxMigration(self):
		return self._maxMigration

	@Property('float')
	def maxKids(self):
		return self._maxKids

	@intolerance.setter
	def intolerance(self, intolerance):
		self._intolerance = intolerance

	@similarity.setter
	def similarity(self, similarity):
		self._similarity = similarity

	@maxMigration.setter
	def maxMigration(self, maxMigration):
		self._maxMigration = maxMigration

	@maxKids.setter
	def maxKids(self, maxKids):
		self._maxKids = maxKids

	@Slot()
	def resetClass(self):
		sneakyResetFunction()

brug		= Bridge()
classroom	= Image.new("RGBA", (128, 128), (0, 0, 0, 0))
prio		= queue.Queue()


def getColor(pos):
	col = classroom.getpixel(pos)
	if col[3] == 0:
		#print("pos " + str(pos) + " is empty alright, col is: " + str(col))
		return None
	return (col[0], col[1], col[2])

def placeAgent(pos, col):
	if len(col) == 3:
		col = (col[0], col[1], col[2], 255)

	whatsThere = getColor(pos)
	if whatsThere is not None:
		return False

	classroom.putpixel(pos, col)
	prio.put(pos)
	return True

def removeAgent(pos):
	classroom.putpixel(pos, (0,0,0,0))

def posIsOk(pos):
	return len(pos) == 2 and pos[0] >= 0 and pos[0] < classroom.width and pos[1] >= 0 and pos[1] < classroom.height

def randomPos():
	return (random.randint(0, classroom.width-1), random.randint(0, classroom.height-1))

def randomPosAtMaxDist(posDist, distance=3):
	while True:
		pos = (random.randint(0, classroom.width-1), random.randint(0, classroom.height-1))
		if math.dist(posDist, pos) < distance:
			return pos

def initClassroom():
	global classroom
	global prio
	classroom = Image.new("RGBA", (classroom.width, classroom.height), (0, 0, 0, 0))
	prio = queue.Queue()
	maxKids = (classroom.width * classroom.height) * brug._maxKids
	print(maxKids)
	kiddos  = set()
	while len(kiddos) < maxKids:
		newKid = randomPos()
		if newKid not in kiddos:
			kiddos |= set([(newKid[0], newKid[1])])
			col = (0, 0, 0, 0)
			while col[0] == 0 and col[1] == 0 and col[2] == 0:
				col = (random.randint(0,255), random.randint(0,255), random.randint(0,255), 255) #(random.random(), random.random(), random.random(), 1.0)
			placeAgent(newKid, col)

_sneakyResetFunction = initClassroom

def countNeighboursIsItAGoodPlace(pos, posCol):
	neighbours	= []
	for relX in range(-1, 2):
		for relY in range(-1, 2):
			absX = pos[0] + relX
			absY = pos[1] + relY
			if absX >= 0 and absY >= 0 and absX < classroom.width and absY < classroom.height and not (relX == 0 and relY == 0):
				neighbourColor = getColor((absX,absY))
				if neighbourColor is not None:
					neighbours.append(neighbourColor)

	similarNeighbours = []
	avgSimil = 0
	for neighbour in neighbours:
		if neighbour is None:
			print("Neighbour is None...")
			exit()

		colDist = math.dist(neighbour, posCol) / 441.6729559300637
		avgSimil += colDist

		if math.dist(neighbour, posCol) / 441.6729559300637 < brug._similarity:
			similarNeighbours.append(neighbour)

	ratio = 0
	if len(neighbours) > 0:
		ratio = len(similarNeighbours) / len(neighbours)
		avgSimil /= len(neighbours)

	#return avgSimil < brug._similarity
	return ratio > brug._intolerance and len(neighbours) > 2 #Maybe they want to have neighbours?or len(neighbours) == 0

def checkForPotentialMover():
	potMover	= prio.get()
	potMoverCol = getColor(potMover)
	if potMoverCol is None:
		app.exit()

	if not countNeighboursIsItAGoodPlace(potMover, potMoverCol):
		#so this agent has decided to move!
		tries = 0
		maxTries = 100
		placedIt = False

		while tries < maxTries and not placedIt:
			if brug.maxMigration <= 1.0:
				pos = randomPos()
			else:
				pos = randomPosAtMaxDist(potMover, brug.maxMigration)

			placedIt = False
			if countNeighboursIsItAGoodPlace(pos, potMoverCol) or tries > maxTries / 2:
				placedIt = placeAgent(pos, potMoverCol)

			if not placedIt:
				tries += 1

		if not placedIt:
			prio.put(potMover)
		else:
			removeAgent(potMover)
	else:
		#Agent seems to be fine here so it aint moving!
		prio.put(potMover)

	#print("updateClassRoom done, prio has length")
	#print(prio.qsize())


def updateClassroom():
	for a in range(10):
		checkForPotentialMover();


class ImgProvider(QQuickImageProvider):
	def __init__(self):
		super().__init__(QQuickImageProvider.Image)

	def requestImage(self, id, size, requestedSize):
		classCopy = classroom.copy()
		if requestedSize is tuple and len(tuple) == 2 and requestedSize.x > 0 and requestedSize.y > 0:
			classCopy.resize(requestedSize)
		return ImageQt.ImageQt(classCopy)

revision = 0

if __name__ == "__main__":
	app			= QGuiApplication(sys.argv)
	engine		= QQmlApplicationEngine()
	qml_file	= Path(__file__).resolve().parent / "main.qml"

	initClassroom()
	print(prio)

	imgProvider = ImgProvider()
	engine.addImageProvider("img", imgProvider)



	def updateRevisionAndClassroom():
		global revision
		updateClassroom()
		revision += 1
		engine.rootContext().setContextProperty("revision", revision)

	timer = QTimer()
	timer.timeout.connect(updateRevisionAndClassroom)
	timer.interval = 0
	timer.start()

	engine.rootContext().setContextProperty("revision", revision)
	engine.rootContext().setContextProperty("brug",		brug)

	engine.load(qml_file)

	if not engine.rootObjects():
		sys.exit(-1)

	sys.exit(app.exec())
