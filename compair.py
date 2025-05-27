def compair(message,l,p):
    with open("typing_script.txt","r", encoding='utf-8') as file:
        lines = file.readlines()
        if lines[l][p]==message:
            p+=1
        if p==len(lines[l]):
            l+=1
            p=0
        return l,p     
# print(compair('i'))  
