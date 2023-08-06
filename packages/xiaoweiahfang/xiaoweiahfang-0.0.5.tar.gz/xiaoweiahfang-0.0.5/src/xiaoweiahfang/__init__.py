
xiaoweisay = {"hello":"Hello",
              "what is your name":"My name is choco.",
              "who are you":"I am a Xiao Wei, a chat robot made by David Shem.",
              "what do you like to eat":"I like to eat chocolate.",
              "do you like chocolate":"Yes, I like chocolate.",
              "do you like eat chocolate":"Yes, I like eat chocolate.",

              "i dont know.":"i dont know.",
              "what 7 u say":"what 7 u say",
              "bye":"bye"
              }
              
xiaoweithink = {"do you like":"No, I only like chocolate.",
                "do you like eat":"No, I only like eat chocolate.",
               }
              


def chatting(inputans):
    username = "Xiao Wei"
    inputans = inputans.lower()

    for x in xiaoweisay:
        if inputans == x:
            return username + " : " +  xiaoweisay[x]
            
    for x in xiaoweithink:
        if x in inputans:
            return username + " : " +  xiaoweithink[x]

    return "what 7 u say"

if __name__ == '__main__':
    # testing
    print(chatting("what is your name"))
    print(chatting("do you like car"))

