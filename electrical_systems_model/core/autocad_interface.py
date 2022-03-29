# This is where I will input all my autocad code

# USE CLASSES AND REFERNECE BEN+ALEX'S CODE

import pyautocad as ac

from pyautocad import APoint, Autocad, aDouble

acad = ac.Autocad()

print(acad.doc.name)

p = aDouble(0, 0, 0, 10, 20, 0, 69, 69, 0)
acad.model.AddPolyline(p)
acad.model.InsertBlock(p)


def switchBoard(centerX, centerY, sB_X_Dim, sB_Y_Dim):
    """have the dimension of this depend on the amount of items in the switchboard"""
    centerPt = APoint(centerX, centerY)

    sB_TL = APoint(centerX - sB_X_Dim, centerY + sB_Y_Dim)
    sB_TR = APoint(centerX + sB_X_Dim, centerY + sB_Y_Dim)
    sB_BR = APoint(centerX + sB_X_Dim, centerY - sB_Y_Dim)
    sB_BL = APoint(centerX - sB_X_Dim, centerY - sB_Y_Dim)

    sBTopLine = acad.model.AddLine(sB_TL, sB_TR)
    sBRightLine = acad.model.AddLine(sB_TR, sB_BR)
    sBBottomLine = acad.model.AddLine(sB_BR, sB_BL)
    sBLeftLine = acad.model.AddLine(sB_BL, sB_TL)


def bus(sBcenterX, sBcenterY, sB_X_Dim, busNum):
    bus_X_Dim = 15
    bus_Y_Dim = 1
    busCenterY = sBcenterY
    clearance = bus_X_Dim / 2
    i = 0
    while (i < busNum):
        'May cause issues with the size of the switchboard and overlapping'
        busCenterX = sBcenterX - sB_X_Dim + bus_X_Dim + i * 2 * sB_X_Dim / busNum + clearance

        bus_TL = APoint(busCenterX - bus_X_Dim, busCenterY + bus_Y_Dim)
        bus_TR = APoint(busCenterX + bus_X_Dim, busCenterY + bus_Y_Dim)
        bus_BR = APoint(busCenterX + bus_X_Dim, busCenterY - bus_Y_Dim)
        bus_BL = APoint(busCenterX - bus_X_Dim, busCenterY - bus_Y_Dim)

        busTopLine = acad.model.Addline(bus_TL, bus_TR)
        busRightine = acad.model.Addline(bus_TR, bus_BR)
        busBottomLine = acad.model.Addline(bus_BR, bus_BL)
        busLeftLine = acad.model.Addline(bus_BL, bus_TL)

        i = i + 1


sB_X_Dim = 200
sB_Y_Dim = 50
sBcenterX = 200
sBcenterY = 100
switchBoard(sBcenterX, sBcenterY, sB_X_Dim, sB_Y_Dim)
bus(sBcenterX, sBcenterY, sB_X_Dim, 5)

acad.prompt("Hello World\n")
