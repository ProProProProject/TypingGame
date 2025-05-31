def compair(message,l):
    clear=False
    end=False
    with open("typing_script.txt","r", encoding='utf-8') as file:
        lines = file.readlines()
        if lines[l][:-1]==message:
            l+=1
            clear=True
        if l==len(lines):
            end=True
        return l ,clear,end    
# print(compair('i'))  
