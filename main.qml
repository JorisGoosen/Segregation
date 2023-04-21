import QtQuick
import QtQuick.Window
import QtQuick.Controls 2
import nl.jorisgoosen.Segregation


Window
{
	width:		800
	height:		width
	visible:	true
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

	Slider
	{
		id:			intoleranceSlider
		onMoved:	brug.intolerance = intoleranceSlider.value
		anchors
		{
			left:	classroom.right
			top:	parent.top
			right:	parent.right
		}
		value:		brug.intolerance
	}
}
