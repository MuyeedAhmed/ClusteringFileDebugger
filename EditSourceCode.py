import os


def spaceCount(variableName):
    c = 0
    for i in range(len(variableName)):
        if variableName[i] != ' ':
            return variableName[i:], c
        c = c + 1
        

def init_decorator(newFile):
    newFile.write("import pickle\n")
    newFile.write("import os\n")
    
    newFile.write("def record_variable():\n")
    newFile.write("    def inner(f):\n")
    newFile.write("        def init(*args, **kwargs):\n")
    newFile.write("            saveFileName = 'AP_Variables/'+args[2]+'_'+args[1]+'_'+str(args[3])+'.pkl'\n")
    newFile.write("            output = open(saveFileName, 'ab')\n")
    newFile.write("            pickle.dump(args[0], output)\n")
    newFile.write("            output.close()\n")
    newFile.write("        return init\n")
    newFile.write("    return inner\n")
    newFile.write("@record_variable()\n")
    newFile.write("def _store_variable(v, vn, f, k):\n")
    newFile.write("    pass\n")
'''

def record_variable():
    def inner(f):
        def init(*args, **kwargs):
            saveFileName = 'AP_Variables/'+args[2]+'_'+args[1]+'_'+str(args[3])+'.pkl'
            output = open(saveFileName, 'ab')
            pickle.dump(args[0], output)
            output.close()
        return init
    return inner

@record_variable()
def _store_variable(v, vn, f, k):
    pass

'''

def add_decorator(newFile, spaces, functionName, variableName, lineCount):
    newFile.write(f"#<SecondRun>{spaces}if os.path.exists('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl'):\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}pickle_objects = []\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}with open('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl', 'rb') as f:\n")
    
    newFile.write(f"#<SecondRun>{spaces+' '*8}while True:\n")
    newFile.write(f"#<SecondRun>{spaces+' '*12}try:\n")
    newFile.write(f"#<SecondRun>{spaces+' '*16}pickle_objects.append(pickle.load(f))\n")
    newFile.write(f"#<SecondRun>{spaces+' '*12}except EOFError:\n")
    newFile.write(f"#<SecondRun>{spaces+' '*16}break\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}os.remove('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl')\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}_old_{variableName} = pickle_objects.pop(0)\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}if _old_{variableName} != {variableName}:\n")
    newFile.write(f"#<SecondRun>{spaces+' '*8}print('First difference at line {lineCount} and variable {variableName}')\n")
    newFile.write(f"#<SecondRun>{spaces+' '*4}for pick_obj in pickle_objects:\n")
    newFile.write(f"#<SecondRun>{spaces+' '*8}_store_variable(pick_obj, '{variableName}', '{functionName}', {lineCount})\n")

    newFile.write(f"{spaces}_store_variable({variableName}, '{variableName}', '{functionName}', {lineCount}) #<FirstRun>\n")



def CreateNewFile():
    comment_line = '#'
    comment_paragraph  = "'''"
    
    file1 = open('File.py', 'r')
    Lines = file1.readlines()
    
    newFile = open('FileNew.py', 'w')
    init_decorator(newFile)
    lineCount = 0
    commentFlag = 0
    # Strips the newline character
    for line in Lines:
        newFile.write(line)
        if comment_line in line:
            line = line.split("#")[0]
        if comment_paragraph in line:
            commentFlag = 1 if commentFlag == 0 else 0
        if commentFlag:
            continue
        if "def " in line:
            functionName = line.split('(')[0].split(' ')[1]
            print(functionName)
        if "=" in line:
            variableName = line.split('=')[0]
            variableName, sCount = spaceCount(variableName)
            spaces = ' ' * sCount
            variableName = variableName.replace(' ', '')
            if "," in variableName:
                variableNames = variableName.split(',')
                print("hue,", variableNames)
                for v in variableNames:
                    add_decorator(newFile, spaces, functionName, v, lineCount)
            else:
                add_decorator(newFile, spaces, functionName, variableName, lineCount)
                    
                
    
            
            print(line)
            print(variableName)
        lineCount += 1
    newFile.close()


def editFileForRun2():
    file1 = open('FileNew.py', 'r')
    Lines = file1.readlines()
    
    newFile = open('FileNewTemp.py', 'w')

    for line in Lines:
        line = line.replace('#<SecondRun>', '')
        if '#<FirstRun>' not in line:
            newFile.write(line)
    os.remove('FileNew.py')
    os.rename('FileNewTemp.py', 'FileNew.py')

if __name__ == "__main__":
    # CreateNewFile()
    editFileForRun2()
