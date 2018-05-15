import vtk
from numpy import random as random
import numpy as np
from laspy.file import File
import math


class VtkPointCloud:

    def __init__(self, zMin=-100.0, zMax=100.0, maxNumPoints=1e6):
        self.maxNumPoints = maxNumPoints
        self.vtkPolyData = vtk.vtkPolyData()
        self.clearPoints()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(self.vtkPolyData)
        mapper.SetColorModeToDefault()
        mapper.SetScalarRange(zMin, zMax)
        mapper.SetScalarVisibility(1)
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)

    def addPoint(self, point):
        if self.vtkPoints.GetNumberOfPoints() < self.maxNumPoints:
            pointId = self.vtkPoints.InsertNextPoint(point[:])
            self.vtkDepth.InsertNextValue(point[2])
            self.vtkCells.InsertNextCell(1)
            self.vtkCells.InsertCellPoint(pointId)
        else:
            r = random.randint(0, self.maxNumPoints)
            self.vtkPoints.SetPoint(r, point[:])
        self.vtkCells.Modified()
        self.vtkPoints.Modified()
        self.vtkDepth.Modified()

    def clearPoints(self):
        self.vtkPoints = vtk.vtkPoints()
        self.vtkCells = vtk.vtkCellArray()
        self.vtkDepth = vtk.vtkDoubleArray()
        self.vtkDepth.SetName('DepthArray')
        self.vtkPolyData.SetPoints(self.vtkPoints)
        self.vtkPolyData.SetVerts(self.vtkCells)
        self.vtkPolyData.GetPointData().SetScalars(self.vtkDepth)
        self.vtkPolyData.GetPointData().SetActiveScalars('DepthArray')


inFile = File('../filtered_points/filtered_points_1.25.las', mode='r')
points = np.transpose(np.array([inFile.x, inFile.y, inFile.z]))

for i in range(3):
    print(np.mean(points[:, i]))
    points[:, i] -= np.mean(points[:, i])

input_len = points.shape[0]
max_val = math.ceil(max(inFile.header.max))
min_val = math.floor(min(inFile.header.min))
scale = max_val/100000

pointCloud = VtkPointCloud()
for k in range(input_len):
    point = points[k,:] / scale
    # print(point)
    # point = 20 * (random.rand(3) - 0.5)
    pointCloud.addPoint(point)
pointCloud.addPoint([0,0,0])
pointCloud.addPoint([0,0,0])
pointCloud.addPoint([0,0,0])
pointCloud.addPoint([0,0,0])

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(pointCloud.vtkActor)
renderer.SetBackground(.2, .3, .4)
renderer.ResetCamera()

# Render Window
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

# Interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)

# Begin Interaction
renderWindow.Render()
renderWindowInteractor.Start()