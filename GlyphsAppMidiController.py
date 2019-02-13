import mido
import time
from ScriptingBridge import SBObject, SBApplication
from pprint import pprint

Glyphs = SBApplication.applicationWithBundleIdentifier_("com.GeorgSeifert.Glyphs2")
doc = Glyphs.open_("/Users/florentindemoffarts/Documents/IllustratorMIDIExtension/GlyphsPlugin/test.glyphs")
font = doc.font()
currentGlyph = font.glyphs()[0]
currentLayer = currentGlyph.layers()[0]
currentPath = currentLayer.paths()[0]
currentNode = currentPath.nodes()[0]

axisToggle = "x"
currentNodeIndex = 0
currentYPos = 0
currentXPos = 0

# pprint((list(set(dir(currentLayer)) - set(dir(SBObject)))))
# pprint((list(set(dir(layer)) - set(dir(SBObject)))))

with mido.open_input() as inport:
	for msg in inport:
		print(msg)

		# Changing X/Y axis
		if(hasattr(msg, 'note')):
			if(msg.note == 43 and msg.velocity == 127):
				if(axisToggle == "x"):
					axisToggle = "y"
				elif(axisToggle == "y"):
					axisToggle = "x"
				# print(axisToggle)

		# Big wheel turning
		elif(hasattr(msg, 'control')):
			if(msg.control == 53):
				if(axisToggle == "x"):
					# currentXPos = currentNode.xPosition()
					# To the right
					if(msg.value == 65):
						currentXPos = currentXPos + 1
					# To the left
					elif(msg.value == 63):
						currentXPos = currentXPos - 1
					currentNode.setXPosition_(currentXPos)
					# print('currentXPos: ')
					 # print(currentXPos)

				elif(axisToggle == "y"):
					# currentYPos = currentNode.yPosition()
					# To the right
					if(msg.value == 65):
						currentYPos = currentYPos + 1
					# To the left
					elif(msg.value == 63):
						currentYPos = currentYPos - 1
					currentNode.setYPosition_(currentYPos)

			elif(msg.control == 56):
				nodeCount = currentPath.nodes().count()

				if(msg.value == 65):
					if(currentNodeIndex < nodeCount - 1):
						currentNodeIndex = currentNodeIndex + 1
					elif(currentNodeIndex >= nodeCount - 1):
						currentNodeIndex = 0
				elif(msg.value == 63):
					if(currentNodeIndex > 0):
						currentNodeIndex = currentNodeIndex - 1
					elif(currentNodeIndex <= 0):
						currentNodeIndex = nodeCount - 1

				currentNode = currentPath.nodes()[currentNodeIndex]
				print(currentNodeIndex)
