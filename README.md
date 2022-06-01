# python_console
Python console apps for data

## 1) VTE View to Table Engine
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
        ansewer1 = input()
        print('2) ' + Fore.YELLOW + '(Config)' +  Fore.WHITE + ' Enter name of SQL config file:', end=' ')
        ansewer2 = input()
        SQLConnection = SQLConn(JSONFile(ansewer1, ansewer2))
        try:
            print('3) ' + Fore.LIGHTGREEN_EX + '(VIEW)' +  Fore.WHITE + ' Enter name of schema:', end=' ')
            ansewer3 = input()
            print('4) ' + Fore.LIGHTGREEN_EX + '(VIEW)' +  Fore.WHITE + ' Enter name of view:', end=' ')
            ansewer4 = input()
            SQLViewObject = SQLObject(ansewer3, ansewer4).fullname
            try:
                print('5) ' + Fore.MAGENTA+ '(Table)' +  Fore.WHITE + ' Enter name of schema:', end=' ')
                ansewer5 = input()
                print('6) ' + Fore.MAGENTA + '(Table)' +  Fore.WHITE + ' Enter name of table:', end=' ')
                ansewer6 = input()
                SQLTableObject = SQLObject(ansewer5, ansewer6).fullname
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

**martenczuk 0.1.7**

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
            time.sleep(1)
        print(Fore.GREEN + " \n Success \n ")
    except: print(Fore.RED + " \n Error \n ")       
    conn0.close()
    return None
```
The application helps in mass conversion of values to static tables.

...

Best Regards

_Kamil M._
