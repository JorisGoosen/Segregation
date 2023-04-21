import QtQuick
import QtQuick.Window

Window
{
	width: 640
	height: width
	visible: true
	title: qsTr("Segregation")

	Image
	{
		id:							classroom
		source:						"image://img/whatever"
		height:						parent.height
		width:						height
		anchors.horizontalCenter:	parent.horizontalCenter
	}
}
