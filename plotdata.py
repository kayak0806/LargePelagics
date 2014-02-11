import datetime
import parsedata
import thinkplot

rawData = parsedata.parseFile('drifter.tab')

timeData = [point[0] for point in rawData]
lightData = [point[2] for point in rawData]

print lightData

thinkplot.Scatter(timeData,lightData)
thinkplot.Show()

