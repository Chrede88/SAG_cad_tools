""" This module holds function that are useful
for creating CAD desings based on non-zero wide LWPolyLines.
All these functions rely on the ezdxf python package.
"""

import ezdxf
import time
import matplotlib.pyplot as plt

# /////////////////////
# //// Load file /////
# ////////////////////

def load_dxf(path):

	"""	Load dxf file using ezdxf package for python.
		Args: path (type:str) """

	fileContainer = ezdxf.readfile(path)
	return fileContainer


def save_dxf(fileContainer):

	""" Save a dxf file. Add time stamp to loaded filename
		if override is False.

		Args:	fileContainer (type:ezdxf.drawing.Drawing) """

	path = fileContainer.filename
	timestamp = int(time.time())
	fileContainer.saveas(path[:-4]+'_'+str(timestamp)+'.dxf')

# //////////////////
# //// Layers /////
# /////////////////

def create_layer(fileContainer,newLayer,layerAttr):

	""" Create a new layer called 'newLayer'.
		Layer colors: red:1, blue:5, white:7

		Args:	fileContainer (type:ezdxf.drawing.Drawing),
				newLayer (type:str),
				layerAttr (type:dict) """

	fileContainer.layers.new(name=newLayer, dxfattribs=layerAttr)

def print_layers(fileContainer):

	""" Print names of all layers in the file, plus the number of
		layers.
		Args: fileContainer (type:ezdxf.drawing.Drawing) """

	print('Layers in file {}:\n'.format(fileContainer.filename))

	for layer in fileContainer.layers:
		print('Layer: {} with color {}'.format(layer.dxf.name,layer.get_color()))

	print('\nTotal number of layers: {}'.format(len(fileContainer.layers)))

# ///////////////////////
# //// LWPolyLines /////
# //////////////////////

def create_LWPolyLine(fileContainer,points,width,lineAttr):

	""" Create a LWPolyLine.
		Specify layer in 'lineAttr' dict, {'layer':'LAYERNAME'}.

		Args:	fileContainer (type:ezdxf.drawing.Drawing),
				points (type:tuple),
				width (type:float),
				lineAttr (type:dict) """

	msp = fileContainer.modelspace()
	# creates a zero width LWPolyLine
	line = msp.add_lwpolyline(points,dxfattribs=lineAttr)
	if width != 0:
		line.dxf.const_width = width

def create_SAG_contact_layer(fileContainer,layerName,sourceLayer,color):

	""" Creates a new layer called 'layerName'.
		Adds LWPolyLines on top of nonzero width LWPolyLines
		from 'sourceLayer', with a smaller width. Widths are defined
		in the lookup table 'width_lookup'.

		Args:	fileContainer (type:ezdxf.drawing.Drawing),
				layerName (type:str),
				sourceLayer (type:str),
				color (type:int) """

	width_lookup = {'5.0':4.0,'4.0':3.0,'3.0':2.0,'2.0':1.0,'1.0':0.5,'0.5':0.3}

	msp = fileContainer.modelspace()

	# create new layer
	create_layer(fileContainer, layerName, layerAttr={'color': color})

	# find all LWPolyLines in sourceLayer
	lines = msp.query('LWPOLYLINE[layer=="{}"]'.format(sourceLayer))

	# create new LWPolyLines with reduced width
	for line in lines:
		line_width = line.dxf.const_width
		if line_width != 0:
			new_width = width_lookup.get(str(line_width))
			if isinstance(new_width, float) is False:
				new_width = line_width
			with line.points() as points:
				create_LWPolyLine(fileContainer,points,new_width,
					lineAttr={'layer': layerName})
