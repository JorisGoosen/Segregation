# This Python file uses the following encoding: utf-8
import sys
import queue
import random
from pathlib			import Path
from PySide6.QtCore		import QTimer
from PySide6.QtGui		import QGuiApplication
from PySide6.QtQml		import QQmlApplicationEngine
from PySide6.QtQuick	import QQuickImageProvider
from PIL				import Image, ImageQt


classroom	= Image.new("RGBA", (200, 200), (0, 0, 0, 0))
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

def initClassroom():
	maxKids = (classroom.width * classroom.height) / 3
	print(maxKids)
	kiddos  = set()
	while len(kiddos) < maxKids:
		newKid = randomPos()
		if newKid not in kiddos:
			kiddos |= set([(newKid[0], newKid[1])])
			col = (0, 0, 0, 0)
			while col[0] == 0 and col[1] == 0 and col[2] == 0:
				col = (random.randint(0,1)*255, random.randint(0,1)*255, random.randint(0,1)*255, 255) #(random.random(), random.random(), random.random(), 1.0)
			placeAgent(newKid, col)

intolerance = 0.5

def updateClassroom():
	potMover	= prio.get()
	potMoverCol = getColor(potMover)
	if potMoverCol is None:
		app.exit()

	similars	= []
	for relX in range(-1, 2):
		for relY in range(-1, 2):
			absX = potMover[0] + relX
			absY = potMover[1] + relY
			if absX >= 0 and absY >= 0 and not (relX == 0 and relY == 0) and absX < classroom.width and absY < classroom.height:
				neighbourColor = getColor((absX,absY))
				if neighbourColor is not None:
					similars.append(neighbourColor)

	similarNeighbours = 0
	for similar in similars:
		if similar == potMoverCol:
			similarNeighbours += 1

	ratio = similarNeighbours / max(1, len(similars))

	if ratio < intolerance:
		#so this agent has decided to move!
		safety = 0

		while not placeAgent(randomPos(), potMoverCol) and safety < 1000:
			safety += 1

		if safety > 1000:
			print("WTF")
			exit(123)

		removeAgent(potMover)
	else:
		#Agent seems to be fine here so it aint moving!
		prio.put(potMover)

	#print("updateClassRoom done, prio has length")
	#print(prio.qsize())





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

	engine.load(qml_file)

	if not engine.rootObjects():
		sys.exit(-1)

	sys.exit(app.exec())
