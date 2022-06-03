# python_console
Python console apps for data

## 1) VTE View to Table Converter
> Console

![vte1](https://user-images.githubusercontent.com/59306140/171512935-43eb3fd3-137b-4d46-9b1d-1b068186a7b9.jpg)


#### Description: 
To copy data from views to tables we need sql database config file and name of view and table only.

- First we enter path and name of sql config file (.json format).
- Next app will ask for name of schema view and table.

**vte.py**

```
from colorama import Back, init, Fore, Style
from martenczuk import SQLConn, SQLObject, JSONFile, VTE

def main():
    init(autoreset=True)
    margin = '##############'
    line = margin + margin + margin
    print(Fore.BLACK + Back.LIGHTWHITE_EX + '\n' + margin + line + margin + '\n' + margin + '#####   VIEW -> TABLE SQL CONVERTER  #####' + margin + '\n'+ margin + line + margin +'\n')
    try: 
        print('1) ' + Fore.YELLOW + '(Config)' +  Fore.WHITE + ' Enter path to SQL config file:', end=' ')
        answer1 = input()
        print('2) ' + Fore.YELLOW + '(Config)' +  Fore.WHITE + ' Enter name of SQL config file:', end=' ')
        answer2 = input()
        SQLConnection = SQLConn(JSONFile(answer1, answer2))
        try:
            print('3) ' + Fore.LIGHTGREEN_EX + '(VIEW)' +  Fore.WHITE + ' Enter name of schema:', end=' ')
            answer3 = input()
            print('4) ' + Fore.LIGHTGREEN_EX + '(VIEW)' +  Fore.WHITE + ' Enter name of view:', end=' ')
            answer4 = input()
            SQLViewObject = SQLObject(answer3, answer4).fullname
            try:
                print('5) ' + Fore.MAGENTA+ '(Table)' +  Fore.WHITE + ' Enter name of schema:', end=' ')
                answer5 = input()
                print('6) ' + Fore.MAGENTA + '(Table)' +  Fore.WHITE + ' Enter name of table:', end=' ')
                answer6 = input()
                SQLTableObject = SQLObject(answer5, answer6).fullname
                try:
                    VTE(SQLViewObject, SQLTableObject, SQLConnection)
                except: print(Fore.RED + '\nERROR: SQL VIEW OR Table Object not found. \n')
            except: pass
        except: pass
    except: print(Fore.RED + '\nError: Invalid SQL config file. \n')
    if input('Enter any key to exit\n'): exit()
if __name__ == "__main__":
    main()
```

### Requirements

**>martenczuk 0.1.6**

```
pip install martenczuk
```

> JSONFile CLASS
```
class JSONFile:
    def __init__(self, path, name) -> object:
        self.filepath = path
        self.filename = name
        self.data = json.load(open(self.filepath + '/' + self.filename + '.json'))
```

> SQL Connection CLASS

```
class SQLConn:
    def __init__(self, configFile: JSONFile) -> object:
        self.drivers = configFile.data['drivers']
        self.server = configFile.data['server']
        self.port = configFile.data['port']
        self.user = configFile.data['user']
        self.password = configFile.data['password']
        self.database = configFile.data['database']
        self.trustmode = configFile.data['Trusted_Connection']
        self.conn = pypyodbc.connect('DRIVER={' + self.drivers + '};SERVER='+ self.server +';UID='+ self.user +';PWD='+ self.password +';DATABASE='+ self.database +';Trusted_Connection='+ self.trustmode +';')
```

> SQL Object CLASS

```
class SQLObject:
    def __init__(self, schemaName, objectName) -> object:
        self.schema = "[" + schemaName + "]"
        self.object = "[" + objectName + "]"
        self.fullname = self.schema + "." + self.object
```

> VTE Function

```
def VTE(source: SQLObject, destination: SQLObject, SQLConnection: SQLConn):
    init(autoreset = True)
    print(Style.DIM + Back.WHITE + Fore.BLACK + "\n SQL View " + source + " is converted to SQL Table " + destination + " in database " + SQLConnection.database + "  " + Fore.CYAN + Back.BLACK + "\n\n   Please Stand By...\n")
    conn0 = SQLConnection.conn
    cursor = conn0.cursor()
    cols = cursor.execute("""Select [name] from sys.columns WHERE object_id = OBJECT_ID('"""+source+"""')""").fetchall()
    cols_string = cols[0][0]
    try:
        for i in range (1,len(cols)): cols_string += " , [" + cols[i][0] + "]"
        rows = cursor.execute("""Select ["""+cols[0][0]+"""] from """+source+""" ORDER BY date""").fetchall()
        for i in tqdm(range(len(rows))):
            row = cursor.execute("""Select * from """+source+""" WHERE """+cols[0][0]+"""='"""+rows[i][0]+"""'""").fetchall()
            values_string = "'" + row[0][0] + "'"
            for j in range (1,len(row[0])): values_string += ",'" + str(row[0][j])+"'"
            try: cursor.execute(""" Insert into """ + destination + """ (""" + cols_string + """) VALUES (""" + values_string + """)""")
            except: pass
            cursor.commit()
        print(Fore.GREEN + " \n Success \n ")
    except: print(Fore.RED + " \n Error \n ")       
    conn0.close()
    return None
```
The application helps in data conversion to static tables.

## 2) CTE CSV to SQL Table Exporter
> Console

![cte1](https://user-images.githubusercontent.com/59306140/171796862-6415709d-2f18-45e9-823b-43309da6a12b.jpg)


#### Description: 
To copy data from CSV files to tables we need path and name of CSV file, sql database config file and name of table only.

- First we enter path and name of CSV file.
- We enter path and name of SQL Config file (.json format)
- Next app will ask for name of schema and table.

**cte.py**

```
from colorama import Back, init, Fore, Style
from martenczuk import SQLConn, SQLObject, JSONFile, CSVFile, CTE

def main():
    init(autoreset=True)
    margin = '##############'
    line = margin + margin + margin
    print(Fore.BLACK + Back.LIGHTWHITE_EX + '\n' + margin + line + margin + '\n' + margin + '#####    CSV -> SQL TABLE EXPORTER   #####' + margin + '\n'+ margin + line + margin +'\n')
    try: 
        print('  1) ' + Fore.LIGHTGREEN_EX + '(CSV)' +  Fore.WHITE + ' Enter path to CSV file:', end=' ')
        answer1 = input()
        print('  2) ' + Fore.LIGHTGREEN_EX + '(CSV)' +  Fore.WHITE + ' Enter name of CSV file:', end=' ')
        answer2 = input()
        print('  3) ' + Fore.LIGHTGREEN_EX + '(CSV)' +  Fore.WHITE + ' Enter delimiter:', end=' ')
        answer3 = input()
        CSVObject = CSVFile(answer1, answer2, answer3)
        try:
            print('  4) ' + Fore.YELLOW + '(Config)' +  Fore.WHITE + ' Enter path to SQL config file:', end=' ')
            answer4 = input()
            print('  5) ' + Fore.YELLOW + '(Config)' +  Fore.WHITE + ' Enter name of SQL config file:', end=' ')
            answer5 = input()
            SQLConnection = SQLConn(JSONFile(answer4, answer5))
            try:
                print('  6) ' + Fore.MAGENTA+ '(SQL)' +  Fore.WHITE + ' Enter name of schema:', end=' ')
                answer6 = input()
                print('  7) ' + Fore.MAGENTA + '(SQL)' +  Fore.WHITE + ' Enter name of table:', end=' ')
                answer7 = input()
                SQLTableObject = SQLObject(answer6, answer7)
                try:
                    CTE(CSVObject, SQLTableObject, SQLConnection)
                except: print(Fore.RED + '\nERROR: CSV file OR SQL Table Object not found. \n')
            except: pass
        except: pass
    except: print(Fore.RED + '\nError: Invalid CSV file. \n')
    if input('Enter any key to exit\n'): exit()
if __name__ == "__main__":
    main()
```

### Requirements

**>martenczuk 0.2.3**

```
pip install martenczuk
```

> CTE

```
def CTE(source: CSVFile, destination: SQLObject, SQLConnection: SQLConn):
    init(autoreset = True)
    print(Style.DIM + Back.WHITE + Fore.BLACK + "\n CSV file " + source.filename + ".csv is exported to SQL Table " + destination.fullname + " in database " + SQLConnection.database + "  " + Fore.CYAN + Back.BLACK + "\n\n   Please Stand By...\n")
    CSV_arr = source.array
    col_string = "[" + CSV_arr[0][0] + "]"
    for i in range (1,len(CSV_arr[0])):
        if CSV_arr[0][i] == "":
            print(Fore.RED + " \n File is empty or check columns \n ")
            return 0
        col_string += " , [" + CSV_arr[0][i] +"]"
    conn0 = SQLConnection.conn
    cursor = conn0.cursor()
    cols_SQL = cursor.execute("""Select [name] from sys.columns WHERE object_id = OBJECT_ID('"""+destination.fullname+"""')""").fetchall()
    cols_SQL_string = "[" + cols_SQL[0][0] +"]"
    try:
        for i in range (1,len(cols_SQL)): cols_SQL_string += " , [" + cols_SQL[i][0] + "]"
        if cols_SQL_string != col_string:
            print(Fore.RED + " \n Columns in file and in database are different \n ")
            return 0
        else:
            for i in tqdm(range(len(CSV_arr)-1)):
                values_string = "'" + CSV_arr[i+1][0] + "'"
                for j in range (1,len(CSV_arr[i])): values_string += ",'" + str(CSV_arr[i+1][j])+"'"
                try: cursor.execute(""" Insert into """ + destination.fullname + """ (""" + col_string + """) VALUES (""" + values_string + """)""")
                except: pass
                cursor.commit()
            print(Fore.GREEN + " \n Success \n ")
    except: print(Fore.RED + " \n Error \n ")
    conn0.close()
    return 0
```
The application helps in data export from CSV files to static tables.

Best Regards

_Kamil M._
