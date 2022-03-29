import time
import pyautocad as ac
from pyautocad import APoint, aDouble

from core.model import Model, Root
from core.sink import ElectricalSink
from core.model import Panel
from core.transmission import Cable, Transformer

acad = ac.Autocad()
acadModel = acad.ActiveDocument.ModelSpace


def createSwbCables(cable, swbY, swbCableNum, swbLength, swbCableX):
    print("Printing the cables that connect to the SWB")

    # This is the Y coordinate of the MSWB, spatial geometry tracking
    cableY = swbY

    # Spatial Geometry of the insertion points adjustments (Make global?)
    xTxtAdj = 2
    yLengthTxtAdj = 5
    ySizeTxtAdj = 18
    yChildTxtAdj = 19

    # Length Point Definition
    cableLengthTxtX = swbCableX + xTxtAdj
    cableLengthTxtY = cableY - yLengthTxtAdj
    cableLengthPoint = APoint(cableLengthTxtX, cableLengthTxtY, 0)

    # Size Point Definition
    cableSizeTxtX = swbCableX - xTxtAdj
    cableSizeTxtY = cableY - ySizeTxtAdj
    cableSizePoint = APoint(cableSizeTxtX, cableSizeTxtY, 0)

    # Child Point Definition
    cableChildX = swbCableX + xTxtAdj
    cableChildY = cableY - yChildTxtAdj
    cableChildPoint = APoint(cableChildX, cableChildY, 0)

    # Cable Point Definition
    cablePoint = APoint(swbCableX, cableY, 0)

    # Insertion of the cable, x position is variable
    acadModel.InsertBlock(cablePoint, 'shortLine', 1, 1, 1, 0)

    # Insertion of cable size
    sizeTxt = acad.model.AddText("3 - " + cable.selected_size + "mm\u00b2", cableSizePoint, 1)
    sizeTxt.Rotate(cableSizePoint, 4.71239)  # Rotation in radians

    # Insertion of Cable Length
    acad.model.AddText(str(cable.length) + "mm", cableLengthPoint, 1)

    # This is the load center for the cable. This splitting is happening because of the way that program
    # groups together the load centers. It removes any potential hyphen's and numbers after it
    loadCenterChildFullString = str(cable.get_children()[0].name).split("-", 1)
    loadCenterChild = loadCenterChildFullString[0].split(" ", 2)

    # Insertion of the load center
    childTxt = acad.model.AddText("P" + loadCenterChild[2], cableChildPoint, 1)
    childTxt.Rotate(cableChildPoint, 4.71239)

    # Spatial geometry stuff
    swbCableX = swbCableX + swbLength / swbCableNum
    return swbCableX


def createRootCables(cable, rootPtX, rootPtY, rootRadius):
    print("Printing the cable that connects root to SWB")
    # Spatial Geometry of the insertion points adjustments
    xTxtAdj = 2
    yLengthTxtAdj = 5
    ySizeTxtAdj = 18

    # Root Cable Point Definition
    rootCableX = rootPtX
    rootCableY = rootPtY - rootRadius
    cablePoint = APoint(rootCableX, rootCableY, 0)

    # Cable Length Point Definition
    cableLengthTxtX = rootCableX + xTxtAdj
    cableLengthTxtY = rootCableY - yLengthTxtAdj
    cableLengthPoint = APoint(cableLengthTxtX, cableLengthTxtY, 0)

    # Cable Size Point Definition
    cableSizeTxtX = rootCableX - xTxtAdj
    cableSizeTxtY = rootCableY - ySizeTxtAdj
    cableSizePoint = APoint(cableSizeTxtX, cableSizeTxtY, 0)

    # Insertion of the cable, x position is variable
    acadModel.InsertBlock(cablePoint, 'shortLine', 1, 1, 1, 0)

    # Insertion of size text
    sizeTxt = acad.model.AddText("3 - " + cable.selected_size + "mm\u00b2", cableSizePoint, 1)
    sizeTxt.Rotate(cableSizePoint, 4.71239)  # Rotation in radians

    # Insertion of length text
    acad.model.AddText(str(cable.length) + "mm", cableLengthPoint, 1)


def createPowerPanelCables(cable, cableX, tempY):
    print("These cables are going to connect to Panels")

    # NOTE: var TempY is used just to get the extra cables out of the way in the dwg

    cableLengthTxtX = cableX + 2
    cableLengthTxtY = tempY - 5
    cableSizeTxtX = cableX + 2
    cableSizeTxtY = tempY - 8

    cablePoint = APoint(cableX, tempY, 0)
    cableLengthPoint = APoint(cableLengthTxtX, cableLengthTxtY, 0)
    cableSizePoint = APoint(cableSizeTxtX, cableSizeTxtY, 0)  # point definitions above
    acadModel.InsertBlock(cablePoint, 'shortLine', 1, 1, 1, 0)  # insertion of the cable, x position is variable
    'acad.model.AddText(cable.selected_size, cableSizePoint, 1)'  # inserts text
    'acad.model.AddText(cable.num_conductors, cableNumPoint, 1)'
    acad.model.AddText(cable.selected_size + "mm\u00b2", cableSizePoint, 1)
    acad.model.AddText(str(cable.length) + "mm", cableLengthPoint, 1)
    cableX += 15
    return cableX


def createCables(cables, rootPtX, rootPtY, rootRadius, swbLength, swbY):
    ############################
    ### Variable Definitions ###
    ############################

    cableY = swbY  # This is the Y coordinate of the MSWB, spatial geometry tracking
    swbCableX = 0  # this number is just the start of the series of SWB cables
    swbCableNum = 0  # Necessary for tracking of spatial geometry

    cableNum = 0  # This is not necessary, only used for bug testing

    cableX = 0  # Temporary
    tempY = cableY - 50  # this is temporary for all cables not connected to MSWB

    # This loop is necessary for spatial geometry stuff
    for cable in cables:
        if str(cable.get_parents().name) == "Main Switchboard":
            swbCableNum += 1

    ##########################
    ### Creation of Cables ###
    ##########################
    for cable in cables:

        # Bug testing
        """
        parent = cable.get_parents()
        child = cable.get_children()
        # print("parent for " + str(cableNum) + " " + str(parent))
        # print("child  for " + str(cableNum) + " " + str(child))
        """

        # Prints Root Cable(s)
        if str(cable.get_parents().name) == "Root":
            createRootCables(cable, rootPtX, rootPtY, rootRadius)
            cableNum += 1  # counting / changing the X dim

        # Prints Main SWB cables
        elif str(cable.get_parents().name) == "Main Switchboard":
            swbCableX = createSwbCables(cable, swbY, swbCableNum, swbLength, swbCableX)
            cableNum += 1  # counting / changing the X dim

        # Prints ~others~
        else:
            cableX = createPowerPanelCables(cable, cableX, tempY)
            cableNum += 1  # counting / changing the X dim

    return cableNum


#  Think about how to link these two ^v up, maybe class, return lists, unsure


def createRoot(components, swbLength, swbY):
    for comp in components:
        if str(comp.name) == "Main Switchboard":
            rootPwr = str("%.1f" % abs(comp.power_in.power / 1000)) + " kW"
            # Method might be fkd because of power drops between switchboard and root
            radius = 6
            rootX = swbLength / 2
            rootY = swbY + radius + 26.4
            rootPt = APoint(rootX, rootY, 0)
            rootTextPoint = APoint(rootX - radius / 2, rootY + radius + 1)
            acad.model.AddCircle(rootPt, radius)
            rootTxtX = rootX - 3
            rootTxtY = rootY
            rootTxtPt = APoint(rootTxtX, rootTxtY, 0)
            acad.model.AddText(rootPwr, rootTxtPt, 1.5)
            acad.model.AddText("Root", rootTextPoint, 2)
    return [rootX, rootY, radius]


def organizeCables():
    print()


def print_component_info(comp):
    print(comp.name)
    print("Power in: " + str("%.1f" % abs(comp.power_in.power / 1000)) + " kW")
    if not isinstance(comp, ElectricalSink):
        print("Power out: " + str("%.1f" % abs(comp.power_out.power / 1000)) + " kW")
        print("Power drop: " + str("%.1f" % abs(comp.power_out.power - comp.power_in.power)) + " W")
    print("Voltage: " + str("%.1f" % abs(comp.power_in.voltage)) + " V")
    print("Current: " + str("%.1f" % abs(comp.power_in.current)) + " A")
    if isinstance(comp, Cable):
        print("Resistance: " + str("%.6f" % comp.resistance) + " Ohms")
    print("")


def print_cable_size(cable):
    print(cable.name)
    print(cable.selected_size)
    print(cable.num_conductors)
    print("")


def format_power(power):
    return "%.1f" % abs(power.power / 1000) + " kW"


def main():
    epla_path = "C:/Users/koliver/Desktop/senir yr/sem 2/this/electrical-systems-model/electrical_systems_model/data" \
                "/EPLA_default.csv "  # MUST MUST MUST change the EPLA in model as well
    load_cases = [1, 2, 3, 4]
    model = Model()
    start = time.time()
    model.load_epla(epla_path)
    model.build()
    build_time = time.time() - start
    model.print_tree()

    start = time.time()
    root_powers = model.solve(load_cases)
    solve_time = time.time() - start

    cables = model.export_cables()
    print(cables)
    for cable in cables:
        print_cable_size(cable)

    model.export_tree(show_cables=True)
    model.export_tree(show_cables=False)

    """
    for case in load_cases:
        print("Load Case " + str(case) + ": " + format_power(root_powers.pop()))
    print('\n')
    """

    components = model.export_components()
    for comp in components:
        print_component_info(comp)

    """
    print("Model Evaluation Times")
    print("Build Time: " + str("%.0f" % (build_time * 1000)) + " ms")
    print("Solve Time: " + str("%.0f" % (solve_time * 1000)) + " ms")
    """

    ###########################
    ### Start of my changes ###
    ###########################

    swbLength = 200  # Swb length, must work on
    YRefCord = 100  # Where the swb is created

    # Creation of the swb - maybe make a function
    swbPoint1 = APoint(0, YRefCord)
    swbPoint2 = APoint(swbLength, YRefCord)
    acad.model.Addline(swbPoint1, swbPoint2)

    # Creates the root, must be before the createCables function
    rootPt = createRoot(components, swbLength, YRefCord)

    # Creates the cables
    createCables(cables, rootPt[0], rootPt[1], rootPt[2], swbLength, YRefCord)


if __name__ == "__main__":
    main()
