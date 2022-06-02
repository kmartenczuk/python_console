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