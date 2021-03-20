import psycopg2
import re
con = psycopg2.connect(
  user="postgres",
  dbname = "forlogs",
  password="12345",
  host="127.0.0.1", 
  port="5432"
)
cursor = con.cursor()  
print("Database opened successfully")
out=open('out.txt','r')
matches = re.findall(r'.+<=.+', out.read(), re.MULTILINE)
date = []
int_id = []
log_str = []
mySql_insert_query = """TRUNCATE TABLE  message; """
cursor = con.cursor()
cursor.execute(mySql_insert_query)
con.commit()
for x in range (0,len(matches)-1):
    date=re.findall(r'\d+-\d+-\d+\s\d+:\d+:\d+',matches[x])
    dateString = ''.join(date) 
    dateString = dateString.replace("[", "")
    copy = dateString
    dateString = dateString[:0]+"'"
    dateString = dateString + copy + "'"
    int_id=re.findall(r'\s(.{6}-.{6}-.{2})',matches[x])
    intString = ''.join(int_id) 
    intString = intString.replace("[", "")
    copy = intString
    intString = intString[:0]+"'"
    intString = intString + copy + "'"
    log_str=re.findall(r'<= (.+)',matches[x])
    logString = ''.join(log_str) 
    logString = logString.replace("[", "")
    copy = logString
    logString = logString[:0]+"'"
    logString = logString + copy + "'"
    idString = "'" + str(x+1) + "'";
    mySql_insert_query = "INSERT INTO message (created, id,int_id, str) VALUES ({},{},{},{})".format(dateString,idString,intString,logString)
    cursor = con.cursor()
    cursor.execute(mySql_insert_query)
con.commit()

out=open('out.txt','r')

date = []
int_id = []
log_str = []
adr = []
regex = r"(.+=>.+)|(.+[**].+)|(.+->.+)|(.+==.+)|(.+ Completed)"

matches = re.finditer(regex, out.read(), re.MULTILINE)

mySql_insert_query = """TRUNCATE TABLE  log; """
cursor = con.cursor()
cursor.execute(mySql_insert_query)
con.commit()

for matchNum, match in enumerate(matches, start=1):
    date=re.findall(r'\d+-\d+-\d+\s\d+:\d+:\d+',match.group())
    dateString = ''.join(date) 
    dateString = dateString.replace("[", "")
    copy = dateString
    dateString = dateString[:0]+"'"
    dateString = dateString + copy + "'"
    int_id=re.findall(r'\s(.{6}-.{6}-.{2})',match.group())
    intString = ''.join(int_id) 
    intString = intString.replace("[", "")
    copy = intString
    intString = intString[:0]+"'"
    intString = intString + copy + "'"
    log_str=re.findall(r'(=>.+)|([**].+)|(->.+)|(==.+)|( Completed)',match.group())
    logString = ''.join(log_str[0])
    logString = logString.replace("[", "")
    logString = logString.replace("'", "")
    copy = logString
    logString = logString[:0] + "'"
    logString = logString + copy + "'"
    match_adr = re.findall(r'[^ @]*@[^ ]*', match.group(), re.MULTILINE);
    if match_adr != []:
        adrString = ''.join(match_adr[0])
        adrString = adrString.replace("[", "")
        adrString = adrString.replace("<","")
        adrString = adrString.replace(">","")
        adrString = adrString.replace(":","")
    else:
        adrString = ""
    copy = adrString
    adrString = adrString[:0]+"'"
    adrString = adrString + copy + "'"
    mySql_insert_query = "INSERT INTO log (created, int_id, str, address) VALUES ({},{},{},{})".format(dateString,intString,logString, adrString)
    cursor = con.cursor()
    cursor.execute(mySql_insert_query)
con.commit()
con.close()
