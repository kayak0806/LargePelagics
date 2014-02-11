import datetime
import parsedata
import thinkplot

x = [1,2,3]
y = [4,5,6]

thinkplot.Scatter(x,y)
thinkplot.Show()

rawData = parsedata.parseFile('drifter.tab')

timeData = [point[0] for point in rawData]ge

print timeData
