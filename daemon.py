import pymssql
import time

conn = pymssql.connect(server='deimos', user='sa', password='gat3k33per', database='LRTTime')
cursor = conn.cursor()
cursor.execute('SELECT Exc.*, proj.*,(SELECT P.project_desc  FROM [LRTTime].[dbo].[Project] as T LEFT JOIN [LRTApp].[dbo].[PJPROJ] as P ON T.ProjectID = P.Project WHERE T.[id] = proj.[id]) as [Project],(SELECT E.pjt_entity_desc FROM [LRTTime].[dbo].[Project] as T LEFT JOIN [LRTApp].[dbo].[PJPENT] as E ON T.TaskID = E.pjt_entity AND SUBSTRING (T.ProjectID, 1, 16) = E.project WHERE T.[id] = proj.[id]) as [Task] FROM [dbo].[ExcDb] as Exc LEFT JOIN [dbo].[Project] as proj ON Exc.EmpID = proj.EmpID AND Exc.ExcDate = proj.date WHERE Exc.ExcDate >=\'2015/8/11\' ORDER BY Exc.ID,Exc.EmpID')

row = cursor.fetchone()
totalHours = 0;
while row:
    print( str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "                 "+str(totalHours))
    
    if row[23] is not None:
        totalHours += int(row[23])
    row = cursor.fetchone()
    time.sleep(.1)
    
print(totalHours)