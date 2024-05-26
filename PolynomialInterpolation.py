import sqlite3,ast, copy

class LagrangePolynomial:
    """used for performing lagrange interpolation"""

    def __init__(self):
        """initialize Lagrange polynomial by using data points stored in the dataPoints.db file"""

        #Extract the data from the dataPoints.db file
        conn = sqlite3.connect('databases/dataPoints.db')
        cursor = conn.cursor()

        cursor.execute("SELECT json_data FROM data")
        rows = cursor.fetchall()

        xy = ast.literal_eval(rows[0][0])

        self.extractPoints(xy)

        
    def extractPoints(self, dataPoints):
        """extract the data points stored in the db file and construct a list of tuple (x,y)"""

        self.DataPoints = []
        for i in range(len(dataPoints[0])):
            self.DataPoints.append((float(dataPoints[0][i]), float(dataPoints[1][i])))

    def lagrange_interpolate_value(self,x):
        y = 0 #y corresponding to given x
        numerator   = 1
        denominator = 1

        workingPoints = copy.copy(self.DataPoints)
        
        for i in range(len(self.DataPoints)):
            x1,y1 = workingPoints.pop(i)
            for j in range(len(workingPoints)):
                numerator   *= (x- workingPoints[j][0])
                denominator *= (x1 - workingPoints[j][0])
            y += float(y1) * numerator/denominator

            workingPoints = copy.copy(self.DataPoints)
            numerator = 1
            denominator = 1

        return round(y,3)
    
    def generateDataPoints(self):
        """returns list of tuples of length 2 
         
         x_init  --> start of the interval
         h       --> stepsize
         n       --> total number of points to be generated"""
        
        sorted_points = sorted(self.DataPoints)
        new_points = []
        x = sorted_points[0][0]

        while x <= sorted_points[-1][0]:
            new_points.append((x, self.lagrange_interpolate_value(x)))
            x += 0.05
        
        return new_points
