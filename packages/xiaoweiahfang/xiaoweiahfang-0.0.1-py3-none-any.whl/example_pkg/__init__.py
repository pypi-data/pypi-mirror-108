### (ansname) ###
#hallo name
a001 = "hello"
B001 = "Hello"

B001C = "what 7 u say"

### (ansans)*/
#name
a002 = "what is your name"
B002 = "My name is choco."

#you
a003 = "who are you"
B003 = "I am a Xiao Wei, a chat robot made by David Shem."

#eat
a004 = "do you like chocolate"
B004 = "Yes, I like chocolate."
B004B = "No, I only like chocolate."

a004C = "do you like eat chocolate"
B004C = "Yes, I like eat chocolate."
B004D = "No, I only like eat chocolate."

a004E = "what do you like to eat"
B004E = "I like chocolate."

#dknow
a998 = "i dont know."

#bye
a999 = "bye"

def chatting(inputans):
    username = "Xiao Wei"
    inputans = inputans.lower()
    if inputans == a002:
        print(username + " : " + B002)
    elif inputans == a001:
        print(username + " : " + B001)
    elif inputans == a004E:
        print(username + " : " + B004E)
    elif inputans == a003:
        print(username + " : " + B003)
    else:
        print(username + " : " + B001C)

if __name__ == '__main__':
    # testing
    chatting("what is your name")


###############
#   522 A 4   #
###############
table1 = {"A":[3,4,6],
          "B":[4,3,6],
          "C":[3,8,4],
          "D":[0,0,0],
          "E":[6,4,8],
          "F":[8,4,6],
          "G":[3,8,6],
          }
            
table2 = {"A":[1,4,5],
          "B":[0,0,0],
          "C":[1,4,5],
          "D":[4,1,5],
          "E":[5,4,1],
          "F":[5,4,1],
          "G":[4,1,5],
          }

def FindLink(destinationNode:str,UnavailableLink:int,NodeRoutingTable:dict):
  
    for x in range(0,len(NodeRoutingTable[destinationNode])):
        if UnavailableLink != NodeRoutingTable[destinationNode][x]:
            return NodeRoutingTable[destinationNode][x]
    return 0

def a522a4(ans):
    ans = FindLink("E",4,table1)
    print(ans)

    
################
#   522 A 5b   #
################

EncrytionTable = {"a":"d","b":"e","c":"f","d":"g","e":"h","f":"i","g":"j","h":"k",
                  "i":"l","j":"m","k":"n","l":"o","m":"p","n":"q","o":"r","p":"s",
                  "q":"t","r":"u","s":"v","t":"w","u":"x","v":"y","w":"z","x":"a",
                  "y":"b","z":"c"," ":" "}

def Substitute(InputChar:str):
    IsUpperCharacter = InputChar.isupper() 
    x = InputChar.lower() 
    if IsUpperCharacter: 
        return EncrytionTable[x].upper()
    else:
        return EncrytionTable[x]

def a522a5b():
    MyString = str('Test the encryption is working')
    NewString = str('')
    for EachChar in MyString:
        NewString += Substitute(EachChar)
    print(NewString)