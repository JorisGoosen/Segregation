# This Python file uses the following encoding: utf-8
import sys
import queue
import random
from pathlib			import Path
from PySide6.QtGui		import QGuiApplication
from PySide6.QtQml		import QQmlApplicationEngine
from PySide6.QtQuick	import QQuickImageProvider
from PIL				import Image, ImageQt


classroom	= Image.new("RGBA", (200, 200)) #default init is black
prio		= queue.PriorityQueue()

def placeAgent(pos, col):
	classroom.putpixel(pos, col)
	prio.put(pos)

def initClassroom():
	maxKids = (classroom.width * classroom.height) / 5
	print(maxKids)
	kiddos  = set()
	while len(kiddos) < maxKids:
		len(kiddos)
		newKid = (random.randint(0, classroom.width-1), random.randint(0, classroom.height-1))
		if newKid not in kiddos:
			kiddos |= set([(newKid[0], newKid[1])])
			col = (0, 0, 0, 1)
			while col[0] == 0 and col[1] == 0 and col[2] == 0:
				col = (random.randint(0,1)*255, random.randint(0,1)*255, random.randint(0,1)*255, 255) #(random.random(), random.random(), random.random(), 1.0)
			placeAgent(newKid, col)

def updateClassroom():
	print("make me")

class ImgProvider(QQuickImageProvider):
	def __init__(self):
		super().__init__(QQuickImageProvider.Image)

	def requestImage(self, id, size, requestedSize):
		classCopy = classroom.copy()
		if requestedSize is tuple and len(tuple) == 2 and requestedSize.x > 0 and requestedSize.y > 0:
			classCopy.resize(requestedSize)
		return ImageQt.ImageQt(classCopy)


if __name__ == "__main__":
	app			= QGuiApplication(sys.argv)
	engine		= QQmlApplicationEngine()
	qml_file	= Path(__file__).resolve().parent / "main.qml"

	initClassroom()
	print(prio)

	imgProvider = ImgProvider()
	engine.addImageProvider("img", imgProvider)

	engine.load(qml_file)

	if not engine.rootObjects():
		sys.exit(-1)

	sys.exit(app.exec())
