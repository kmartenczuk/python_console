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