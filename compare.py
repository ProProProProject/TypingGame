def compare(message,l):
    clear=False
    end=False
    with open("typing_script.txt","r", encoding='utf-8') as file:
        lines = file.readlines()
        # if lines[l].replace("\n","")==message:
        if l < len(lines) and lines[l].strip() == message.strip():
            l+=1
            clear=True
        if l==len(lines):
            end=True
        return l ,clear,end   
# print(compair('i'))  
