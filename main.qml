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
			text:	"Max migration distance and density:"
			color:	"yellow"
			width:	left.width
			height:	contentHeight
			horizontalAlignment: Text.AlignHCenter
		}

		Slider
		{
			id:			maxMigrationSlider
			height:		40
			//color: "purple"
			onMoved:	brug.maxMigration = maxMigrationSlider.value
			width:		leftColumn.width
			value:		brug.maxMigration
			from:		0
			to:			12
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
				anchors
				{
					top:	resetKnop.top
					bottom:	resetKnop.bottom
					right:	parent.right
					left:	resetKnop.right
				}

				value:		brug.maxKids
				onMoved:	brug.maxKids = value
			}
		}
	}
}
