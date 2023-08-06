import os
from lxml import etree
import glob
import numpy as np
from read_roi import read_roi_file
from read_roi import read_roi_zip
import xml.etree.ElementTree as ET
import cv2
from xml.dom import minidom

def postProc(pathCarpeta):
    #IMPORTANTE: Intuyo que tanto los xmls como los .roi se van a encontrar en la misma carpeta
    boxesXmls = []  # list that stores all the lists of boxes of all xml
    boxesROI = []
    boxes = []  # list that will contain all the squares of each xml
    for fichero in os.listdir(pathCarpeta):  # We go through the files in the folder
        (nombreFichero, extension) = os.path.splitext(fichero)
        #if (extension == ".xml"):  # we stay with those who are xmls and we go through them looking for a box
        #   boxes = [] #guardo los box
        if(extension== ".zip"):
            #leo el archivo roi
            print(fichero)
            roi = read_roi_zip(pathCarpeta+fichero)
            key = list(roi.keys())[0]
            union = zip(roi[key]['x'],roi[key]['y'])
            #sacamos pares de coordenadas x,y
            lista = list(union)
            #busco el xml correspondiente
            boxes = readAndGenerateImage(pathCarpeta+nombreFichero+".xml")
            newboxes=[]
            anchura = []
            altura = []
            for x,y in lista: #recorremos la lista y vemos si contienen cuadros
                encontrado = False
                if not (0 < x < 175 and 0 < y < 37):
                    for box in boxes:
                        (category, (xmin, ymin, xmax, ymax), confidence) = box
                        anchura.append(xmax-xmin)
                        altura.append(ymax-ymin)

                        if xmin<x<xmax and ymin<y<ymax:
                            #print('dentro')
                            encontrado = True

                    if encontrado== False:
                        #print(altura)
                        medialt = np.mean(altura)
                        medianch = np.mean(anchura)
                        xnew = x-(medialt/2)
                        ynew = y-(medianch/2)
                        w = medianch+xnew
                        h = medialt+ynew
                        newboxes.append(('glandula', (xnew, ynew, w, h), '1.0'))
            image = cv2.imread(pathCarpeta+nombreFichero+".jpg")
            (hI, wI) = image.shape[:2]
            if (len(image.shape) == 3):
                d = 3
            else:
                d = 1
            #print(pathCarpeta + nombreFichero+".xml")
            file = open(pathCarpeta + "/" + nombreFichero+".xml", "w")

            for b in newboxes:
                boxes.append(b)

            file.write(generateXML(nombreFichero, pathCarpeta, wI, hI, d, boxes))
            file.close()

def generateXML(filename,outputPath,w,h,d,boxes):
    top = ET.Element('annotation')
    childFolder = ET.SubElement(top, 'folder')
    childFolder.text = 'images'
    childFilename = ET.SubElement(top, 'filename')
    childFilename.text = filename[0:filename.rfind(".")]
    childPath = ET.SubElement(top, 'path')
    childPath.text = outputPath + "/" + filename
    childSource = ET.SubElement(top, 'source')
    childDatabase = ET.SubElement(childSource, 'database')
    childDatabase.text = 'Unknown'
    childSize = ET.SubElement(top, 'size')
    childWidth = ET.SubElement(childSize, 'width')
    childWidth.text = str(w)
    childHeight = ET.SubElement(childSize, 'height')
    childHeight.text = str(h)
    childDepth = ET.SubElement(childSize, 'depth')
    childDepth.text = str(d)
    childSegmented = ET.SubElement(top, 'segmented')
    childSegmented.text = str(0)
    for box in boxes:
        confidence=1.0
        if(len(box)==2):
            (category, (x,y,xmax,ymax)) = box
        else:
            (category, (x, y, xmax, ymax),confidence) = box
        childObject = ET.SubElement(top, 'object')
        childName = ET.SubElement(childObject, 'name')
        childName.text = category
        childPose = ET.SubElement(childObject, 'pose')
        childPose.text = 'Unspecified'
        childTruncated = ET.SubElement(childObject, 'truncated')
        childTruncated.text = '0'
        childDifficult = ET.SubElement(childObject, 'difficult')
        childDifficult.text = '0'
        childConfidence = ET.SubElement(childObject, 'confidence')
        childConfidence.text = str(confidence)
        childBndBox = ET.SubElement(childObject, 'bndbox')
        childXmin = ET.SubElement(childBndBox, 'xmin')
        childXmin.text = str(x)
        childYmin = ET.SubElement(childBndBox, 'ymin')
        childYmin.text = str(y)
        childXmax = ET.SubElement(childBndBox, 'xmax')
        childXmax.text = str(xmax)
        childYmax = ET.SubElement(childBndBox, 'ymax')
        childYmax.text = str(ymax)
    return prettify(top)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def readAndGenerateImage(labelPath):
    tree = ET.parse(labelPath)
    root = tree.getroot()
    objects = root.findall('object')
    #if(len(objects)<1):
    #    raise Exception("The xml should contain at least one object")
    boxes = []
    for object in objects:
        category = object.find('name').text
        confidence = object.find('confidence')
        if confidence is None:
            confidence=1.0
        else:
            confidence = float(confidence.text)
        bndbox = object.find('bndbox')
        xmin  = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        ymax = int(bndbox.find('ymax').text)
        xmax = int(bndbox.find('xmax').text)
        boxes.append((category, (xmin, ymin, xmax, ymax),confidence))
    return boxes

postProc("/home/ancasag/Descargas/test2/")