import os
b1=['Mon','Tue','Wed','Thu','Fri','Sat']
b2=['   ','   ','   ','   ','   ','   ',]
br=['Break','Break','Break','Break','Break','Break',]
b3=['   ','9-A','10A','10A','9-A','   ',]
b4=['   ','   ','   ','11t','11t','9-B']
b5=['11t','11t','11t','11t','11t','11t',]
b6=['12t','12t','12t','   ','12t','   ']
bL=['Lunch','Lunch','Lunch','Lunch','Lunch','Lunch',]
b7=['12t','   ','12t','12t','12t','12t',]
b8=['   ','11t','   ','   ','   ','   ',]
b9=['10A','9-B','9-B','   ','   ','9-A']
os.system('color')
RED='\033[31m'
GREEN='\033[32m'
BLUE='\033[34m'
RESET='\033[0m'
print('\n'*3)
print(GREEN+'__'*37+RESET)
print(" Bells",'→','|','  1','|','  2','|','Break','|','  3','|','  4','|','  5','|','Lunch','|','  6','|','  7','|','  8','|')
print(" Time  → |",'⁰⁸¹⁵ ','|','⁰⁸⁵⁰ ','|','  ⁰⁹²⁵ ','|','⁰⁹³⁵ ','|','¹⁰¹⁰ ','|','¹⁰⁴⁵ ','|',' ¹¹²⁰  ','|','¹¹⁵⁰ ','|','¹²²⁵ ','|','⁰¹⁰⁰ ','|',sep='')
print(" Days  ↓ |",'⁰⁸⁵⁰ ','|','⁰⁹²⁵ ','|','  ⁰⁹³⁵ ','|','¹⁰¹⁰ ','|','¹⁰⁴⁵ ','|','¹¹²⁰ ','|',' ¹¹⁵⁰  ','|','¹²²⁵ ','|','⁰¹⁰⁰ ','|','⁰¹³⁵ ','|',sep='')
print(GREEN+'__'*37+RESET)
for i in range(0,6):
    print("    ",b1[i],'|',b2[i],'|',b3[i],'|',br[i],'|',b4[i],'|',b5[i],'|',b6[i],'|',bL[i],'|',b7[i],'|',b8[i],'|',b9[i],'|','\n',end='')
    print(GREEN+'--'*37+RESET)
print('\n'*3)
#print("²³¹⁰⁴⁵⁶⁷⁸⁹")
day=10
bell=10
while(day>6 or day<1):
    day=int(input("\tenter day between(1-6): "))
while (bell>8 or bell<1):
    bell=int(input("\tenter bell between(1-8): "))
def sufu(day):
    if(day==1):
        return 'st'
    elif(day==2):
        return 'nd'
    elif(day==3):
        return 'rd'
    else:
        return 'th'

suf=sufu(day)
suff=sufu(bell)
print("\t",f"On {day}{suf} day {bell}{suff} bell is in: ",sep="",end="")
print("\tClass: ",globals()[f'b{bell+1}'][day-1])
