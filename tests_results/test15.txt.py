
def SUBSTRING(s, start, length):
    return s[start:start+length]


def UCASE(s):
    return s.upper()


def LENGTH(s):
    return len(s)


def LCASE(s):
    return s.lower()


def MOD(a, b):
    return a % b


def DIV(a, b):
    return a / b

GreetingComponents: list = [str()] * 5
FinalMessage: str = str()
BaseMessage = 'Happy '
TempStr: str = str()
FileContent: str = str()
GreetingComponents[1] = 'International'
GreetingComponents[2] = 'Working'
GreetingComponents[3] = SUBSTRING("Women's Empowerment", 1, 7)
GreetingComponents[4] = 'Day'
with open("config.txt", 'w') as __fp:
    pass
with open("config.txt", 'w') as __fp:
    __fp.write(FileContent)

with open("config.txt", 'r') as __fp:
    pass
with open("config.txt", 'r') as __fp:
    FileContent = __fp.read()

if LENGTH(FileContent) > 0:
    GreetingComponents[2] = UCASE(SUBSTRING(FileContent, 1, 7))
    
def BuildMessage():
    FinalMessage = BaseMessage
    for Index in range(1, 4):
        if GreetingComponents[Index] == "Women's":
            TempStr = LCASE(GreetingComponents[Index])
            TempStr = UCASE(SUBSTRING(TempStr, 1, 1)) + SUBSTRING(TempStr, 2, 3)
        else:
            TempStr = GreetingComponents[Index]
        FinalMessage = FinalMessage + TempStr
        if Index < 4:
            FinalMessage = FinalMessage + ' '
            
ValidationNumber: int = int()
ValidationNumber = (MOD(LENGTH(FinalMessage), 10)) + DIV(2023, 1000)
__case = ValidationNumber
if __case == 2:
    BuildMessage()
elif __case == 5:
    print('System Error: Validation failed')
else:
    while ValidationNumber != 0:
        ValidationNumber = 0
BuildMessage()
print(FinalMessage, "Happy International Working Women's Day!")