import QtQuick
import QtQuick.Window

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
}
