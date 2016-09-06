import pyodbc,csv

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=Deimos;DATABASE=LRTtime;UID=sa;PWD=gat3k33per')
cursor = cnxn.cursor()

startDate = input('Start Date(mm/dd/yyyy): ')
endDate = input('End Date(mm/dd/yyyy): ')

payDates =[31,28,31,30,31,30,31,31,30,31,30,31]

endMonth = endDate.split("/")[0]
endYear = endDate.split("/")[2]
endDay = 15;
if(int(endDate.split("/")[1])>15):
	endDay = payDates[endMonth-1]
	
csvName =  str(endMonth)+"-"+str(endDay)+"-"+str(endYear)+'.csv'

cursor.execute("SELECT EmpID,ExcTypeID,SUM(ExcAmount) + (select COUNT(ExcAmount) "
+"FROM [LRTTime].[dbo].[ExcDb] WHERE EmpID = ETime.EmpID AND ExcTypeID = ETime.ExcTypeID AND ExcTypeID = 'W' AND ApproveFlag ='Y' AND ExcDate between '"+startDate+"' AND '"+endDate+"')*8 "
+"+ (select COUNT(ExcAmount) FROM [LRTTime].[dbo].[ExcDb] WHERE EmpID = ETime.EmpID AND ExcTypeID = ETime.ExcTypeID AND ExcTypeID = 'H' AND ApproveFlag ='Y' AND ExcDate between '"+startDate+"' AND '"+endDate+"')*8 as Hours "
+",(select COUNT(ExcAmount) FROM [LRTTime].[dbo].[ExcDb] WHERE EmpID = ETime.EmpID AND ApproveFlag ='Y' AND ExcDate between '"+startDate+"' AND '"+endDate+"')*8  as [TotalHours]"
+"FROM [LRTTime].[dbo].[ExcDb] AS ETime WHERE ExcDate between "+"'"+startDate+"'"+" AND "+"'"+endDate+"'" +" GROUP BY ExcTypeID,EmpID ORDER BY EmpID")

#"Select * from ExcDb Where ExcDate between '6/22/2015' and '7/03/2015'")

rows = cursor.fetchall()

with open(csvName,'w') as csvfile:
	fieldnames = ['Employee ID','ExcTypeID','Hours','Total Hours']
	dialectE = csv.excel
	dialectE.lineterminator = "\n"
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames,dialect=dialectE)
	writer.writeheader()
	
	Eid = ""
	
	for row in rows:
		if(Eid!=row.EmpID):
			writer.writerow({})
			Eid = row.EmpID
		writer.writerow({'Employee ID' : row.EmpID,'ExcTypeID' : row.ExcTypeID,'Hours' : row.Hours,'Total Hours' : row.TotalHours})
		
		
	#row.EndTime,row.ApproveFlag,row.SubmitDate,row.UpdateDate,row.DecMgs)
	
	#row.ExcDate,row.EmpID,row.ExcTypeID,row.ExcAmount,row.StartTime,row.BreakStart1,row.BreakEnd1
	#row.LunchStart,row.LunchEnd,row.BreakStart2,row.BreakEnd2
print("CSV file Created")
	
	#dont forget to use the group by employee ID method then order by date!