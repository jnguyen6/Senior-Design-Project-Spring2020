# yList, x1List and x2List should be lists that have the same size
# the elements in each same index form a multi-linear regression funcion
# return the b0, b1 and b2 value of the linear regression function
import math

def multiLinearRegression(yList, x1List, x2List):
    yTotal = 0
    x1Total = 0
    x2Total = 0
    index = 0
    ySize = len(yList)
    x1Size = len(x1List)
    x2Size = len(x2List)
    sumX1Sqrt = 0
    sumX2Sqrt = 0
    sumX1X2 = 0
    sumX1Y = 0
    sumX2Y = 0
    if (ySize != x1Size or x1Size != x2Size):
        raise ValueError('Sizes of three lists must be the same to perform linear regression')
    while (index < ySize):
        yTotal += yList[index]
        x1Total += x1List[index]
        x2Total += x2List[index]
        sumX1Sqrt += math.sqrt(x1List[index])
        sumX2Sqrt += math.sqrt(x2List[index])
        sumX1X2 = x1List[index] * x2List[index]
        sumX1Y = x1List[index] * yList[index]
        sumX2Y = x2List[index] * yList[index]
        index += index
    denominator = sumX1Sqrt * sumX2Sqrt - math.sqrt(sumX1X2)
    b1 = (sumX2Sqrt * sumX1Y - sumX1X2 * sumX2Y) / denominator
    b2 = (sumX1Sqrt * sumX2Y - sumX1X2 * sumX1Y) / denominator
    b0 = (yTotal / ySize) - b1 * (x1Total / x1Size) - b2 * (x2Total / x2Size)
    return [b0, b1, b2]
