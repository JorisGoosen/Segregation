import QtQuick
import QtQuick.Window
import QtQuick.Controls 2.15
import QtQuick.Controls
import QtQuick.Layouts
import nl.jorisgoosen.Segregation


Window
{
	id:			raam
	width:		1280
	height:		800
	visible:	true
	visibility:	Window.Maximized
	title:		qsTr("Segregation")
	color:		"black"


	Image
	{
		id:							classroom
		source:						"image://img/whatever?" + revision
		height:						parent.height
		width:						height
		anchors.horizontalCenter:	parent.horizontalCenter
		smooth:						!brug.blocky
	}

	Column
	{
		id:	rightColumn
		anchors
		{
			left:	classroom.right
			top:	classroom.top
			right:	parent.right
			bottom:	classroom.bottom
		}

		Keys.onEscapePressed:	raam.quit() //https://open.spotify.com/track/4J8ms7TbPISBz71G5z2SGS


		Text
		{
			text:	"Intolerance and similarity:"
			color:	"yellow"
			width:	rightColumn.width
			height:	contentHeight
			horizontalAlignment: Text.AlignHCenter
		}

		Slider
		{
			id:			intoleranceSlider
			height:		40
			//color: "purple"
			onMoved:	brug.intolerance = intoleranceSlider.value
			width:		rightColumn.width
			value:		brug.intolerance
		}

		Slider
		{
			id:			similaritySlider
			width:		rightColumn.width
			height:		40
			//title:		"similarity"
			onMoved:	brug.similarity = similaritySlider.value
			//color: "green"
			value:		brug.similarity
		}

	}

	Column
	{
		id:	leftColumn
		anchors
		{
			right:	classroom.left
			top:	classroom.top
			left:	parent.left
			bottom:	classroom.bottom
		}

		Keys.onEscapePressed:	raam.quit() //https://open.spotify.com/track/4J8ms7TbPISBz71G5z2SGS

		Text
		{
			text:	"Max migration and neighbor distance,\n and class settings, init & reset:"
			color:	"yellow"
			width:	leftColumn.width
			height:	contentHeight
			horizontalAlignment: Text.AlignHCenter
		}

		Item
		{
			width:		leftColumn.width
			height:		40
			SpinBox
			{
				id:				maxMigrationSlider
				editable:		true
				onValueChanged:	brug.maxMigration = maxMigrationSlider.value
				value:			brug.maxMigration
				from:			0
				to:				classRoom.sourceSize.width

				anchors
				{
					top:		parent.top
					bottom:		parent.bottom
					left:		parent.left
					right:		parent.horizontalCenter
				}
			}

			SpinBox
			{
				id:				neighbourSlider
				editable:		true
				onValueChanged:	brug.ratioRadius = neighbourSlider.value

				value:			brug.ratioRadius
				from:			1
				to:				6
				stepSize:		1


				anchors
				{
					top:		parent.top
					bottom:		parent.bottom
					right:		parent.right
					left:		parent.horizontalCenter
				}
			}
		}

		Item
		{
			height:		resetKnop.implicitHeight
			width:		leftColumn.width

			Button
			{
				id:			resetKnop
				text:		"Reset"
				onClicked:	brug.resetClass()
			}

			Slider
			{
				id:			maxKidsSlider
				anchors
				{
					top:	resetKnop.top
					bottom:	resetKnop.bottom
					right:	sizeSlider.left
					left:	resetKnop.right
				}

				value:		brug.maxKids
				onMoved:	brug.maxKids = value
			}

			SpinBox
			{
				id:				sizeSlider
				editable:		true
				anchors
				{
					top:		parent.top
					bottom:		parent.bottom
					right:		parent.right
				}

				value:			brug.classSize
				onValueChanged:	brug.classSize = value
				from:			4
				to:				2048
				stepSize:		1
			}
		}


		CheckBox
		{
			id:					blockyCheck

			width:				parent.width
			height:				implicitHeight

			checked:			brug.blocky
			onCheckedChanged: 	brug.blocky = checked

		}
	}
}
