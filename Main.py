import os
import sys
import string

def loginCall(username,Pass):
    Password=open("Main//pass.txt",'r')
    Login=False
    for i in Password:
        st=i.rstrip()
        tempPass=st.split()
        if len(tempPass)==0:
            continue
        if(username==tempPass[1] and Pass==tempPass[3]):
            Login=True
    return Login

#Starting interface
print("\n\n\n\t\t\t\t\t\t\t\tWELCOME TO FACULTY LEAVE REQUEST SYSTEM\n\n\n\n\n")

trialLeft=3
while(trialLeft):
    username=input("\t\t\t\t\t\t\t\t\tEnter username: ")
    Pass=input("\t\t\t\t\t\t\t\t\tEnter password: ")
    if loginCall(username,Pass):
        os.system('cls' if os.name == 'nt' else 'clear')
        break
    else:
        print("Wrong username or password")
        trialLeft-=1
        print("trialLeft: ",trialLeft)
if(trialLeft==0):
    print("All attempt wrong contact system administrator")
    sys.exit()


#Main interface
print("\n\n\t\t\t\t\t\t\t\t\tFACULTY LEAVE REQUEST INTERFACE\n\n")
print("Welcome! {}".format(username))

schedule=open("Student_Timetable//K18RD.txt",'r')
timeTable=[]
for i in schedule:
    print(i)
    tempTimeTable=i.split()
    if len(tempTimeTable)==0 or tempTimeTable[0] not in ['MONDAY','TUESDAY','WEDNESDAY','THRUSDAY','FRIDAY']:
        continue
    timeTable.append(tempTimeTable)
schedule.close()

print("\n\t\t\t\t\t\t\t\t{} time table for K18RD\n".format(username))

file=open("Student_Timetable//{}.txt".format(username),'r')
for i in file:
    print(i)
    
#Day for leave    
Day=input("Enter leave day (like TUESDAY): ")

#finding timeSlots for adjustment
TimeSlots=[]
fh=open("Student_Timetable//{}.txt".format(username),'r')
for k in fh:
    tempArr=k.split()
    if len(tempArr)==0:
        continue
    if tempArr[0]==Day:
        TimeSlots=[z for z,val in enumerate(tempArr) if val==username]
fh.close()

#finding available teachers for adjustment
Teachers=['Teacher_A','Teacher_B','Teacher_C','Teacher_D','Teacher_E']
TeacherAvailable=[]
for i in Teachers:
    if i==username:
        continue
    fh=open("Faculty_Timetable//{}.txt".format(i),'r')
    for k in fh:
        tempArr=k.split()
        if len(tempArr)==0:
            continue
        if tempArr[0]==Day:
            for p in TimeSlots:
                if tempArr[p]=='B':
                    TeacherAvailable.append([tempArr.count('O'),p,i])
    fh.close()         
       
#Check for any left timeSlots
count=0
for x in TimeSlots:
    for i in TeacherAvailable:
        if i[1]==x:
            count+=1
            break
if len(TeacherAvailable)==0:
    print("No Teachers available for adjustment")
    print("Cannot apply for leave")
    sys.exit()
elif count!=len(TimeSlots): 
    print("No Teachers available for adjustment for some lectures")
    print("Cannot apply for leave")
    sys.exit()

#Choose Teacher for adjustment according to less workload on teacher that day
TimeSlotsDic={1:'9-10',2:'10-11',3:'11-12',4:'12-1',5:'1-2',6:'2-3',7:'3-4',8:'4-5'}
TeacherAssigned=[]
for i in TimeSlots:
    workload=[]
    for t in TeacherAvailable:
        if t[1]==i:
            workload.append([t[0],t[1],t[2]])
    workload.sort(reverse=True)
    TeacherAssigned.append([workload[0][1],workload[0][2]])
    print("\nTeacher for Adjustments for {0} slot from {1} with least Workload: ".format(Day,TimeSlotsDic[i]),workload[0][2])
#change the timetable
TeacherAssigned.sort()
schedule=open("Student_Timetable//K18RD.txt",'r')
leave=open("Student_Timetable//LEAVE.txt", 'w')
for i in schedule:
    if Day in i:
        if len(TeacherAssigned)==1:
            line=i.replace(username,TeacherAssigned[0][1],1)
            leave.write(line)
            continue
        elif len(TeacherAssigned)==2:
            line=i.replace(username,TeacherAssigned[0][1],1).replace(username,TeacherAssigned[1][1],1)
            leave.write(line)
            continue
    leave.write(i)
schedule.close()   
leave.close()

#print adjusted timetable
print("\n\n\t\t\t\t\t\t\t\t\tAdjusted time table")
leave=open("Student_Timetable//LEAVE.txt", 'r')
for i in leave:
    print(i)
leave.close()

print("\n\n\t\t\t\t\t\t\t\t\t\tAdjustement Successful")







