import os
import re

def spaceCount(variableName):
    c = 0
    for i in range(len(variableName)):
        if variableName[i] != ' ':
            return variableName[i:], c
        c = c + 1
        
def checkMultiline(line, stack = []):
    # print(line)
    mulLine = False
    if line.endswith('\\\n'):
        mulLine = True
    open_list = ["[","{","("]
    close_list = ["]","}",")"]
    # print("Brackets: ", end='')
    for i in line:
        
        if i in open_list:
            stack.append(i)
            # print(i, end='')

        elif i in close_list:
            # print(i, end='')

            pos = close_list.index(i)
            if ((len(stack) > 0) and
                (open_list[pos] == stack[len(stack)-1])):
                stack.pop()
            else:
                return "Unbalanced"
    # print(' - ', stack, mulLine)
    return mulLine, stack
    
def init_decorator(newFile):
    newFile.write("import pickle\n")
    newFile.write("import os\n")
    newFile.write("import numpy\n")
    
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
            
    
    newFile.write("def second_run_compare(variable, variableName, functionName, lineCount):\n")
    newFile.write("    filePath = f'AP_Variables/{functionName}_{variableName}_{lineCount}.pkl'\n")
    newFile.write("    iterationFilePath = f'AP_Variables/{functionName}_{variableName}_{lineCount}.txt'\n")
    newFile.write("    sameValue = 1\n")
    newFile.write("    if os.path.exists(filePath):\n")
    newFile.write("        iteration = 1\n")
    newFile.write("        if os.path.exists(iterationFilePath):\n")
    newFile.write("            with open(iterationFilePath) as f:\n")
    newFile.write("                line = f.readline().rstrip()\n")
    newFile.write("                iteration = int(line)+1\n")
    newFile.write("            iterationFile = open(iterationFilePath, 'w')\n")
    newFile.write("            iterationFile.write(str(iteration))\n")
    newFile.write("            iterationFile.close()\n")
    newFile.write("        else:\n")
    newFile.write("            iterationFile = open(iterationFilePath, 'w')\n")
    newFile.write("            iterationFile.write('1')\n")
    newFile.write("            iterationFile.close()\n")
    newFile.write("        with open(filePath, 'rb') as f:\n")
    newFile.write("            for i in range(iteration):\n")
    newFile.write("                try:\n")
    newFile.write("                    _old_variable = pickle.load(f)\n")
    newFile.write("                except EOFError:\n")
    newFile.write("                    print(f'During Run 1, variable {variableName} in line {lineCount} changed {iteration-1} times. But in Run 2 it changed more than that')\n")    
    newFile.write("                    break\n")
    newFile.write("        if type(variable) is not numpy.ndarray:\n")
    newFile.write("            if _old_variable != variable:\n")
    newFile.write("                sameValue = 0\n")
    newFile.write("                print(f'Difference at line {lineCount} and variable {variableName}')\n")
    newFile.write("        else:\n")
    newFile.write("            if (_old_variable == variable).all() == False:\n")
    newFile.write("                sameValue = 0\n")
    newFile.write("                print(f'Difference at line {lineCount} and variable {variableName}')\n")
    newFile.write("        trace = open('Trace.csv', 'a')\n")
    newFile.write("        trace.write(f\"{str(variableName)},{str(functionName)},{str(lineCount)},{str(iteration)},{str(sameValue)}\\n\")\n")
    newFile.write("        trace.close()\n")
    
    
    
    

def add_decorator(newFile, spaces, functionName, variableName, lineCount):
    
    newFile.write(f"#<SecondRun>{spaces}second_run_compare({variableName}, '{variableName}', '{functionName}', {lineCount})\n")
    
    
    # newFile.write(f"#<SecondRun>{spaces}if os.path.exists('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl'):\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}pickle_objects = []\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}with open('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl', 'rb') as f:\n")
    
    # newFile.write(f"#<SecondRun>{spaces+' '*8}while True:\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*12}try:\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*16}pickle_objects.append(pickle.load(f))\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*12}except EOFError:\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*16}break\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}os.remove('AP_Variables/{functionName}_{variableName}_{lineCount}.pkl')\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}_old_{variableName} = pickle_objects.pop(0)\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}if _old_{variableName} != {variableName}:\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*8}print('First difference at line {lineCount} and variable {variableName}')\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*4}for pick_obj in pickle_objects:\n")
    # newFile.write(f"#<SecondRun>{spaces+' '*8}_store_variable(pick_obj, )\n")

    newFile.write(f"{spaces}_store_variable({variableName}, '{variableName}', '{functionName}', {lineCount}) #<FirstRun>\n")



def CreateNewFile():
    comment_line = '#'
    comment_paragraph1  = "'''"
    comment_paragraph2  = "\"\"\""
    
    
    file1 = open('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation_old.py', 'r')
    file1Lines = file1.readlines()
    Lines = iter(file1Lines)
    newFile = open('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/APFileNew.py', 'w')
    init_decorator(newFile)
    lineCount = 0
    commentFlag = 0
    # Strips the newline character
    functionName = ''
    for line in Lines:
        newFile.write(line)
        lineCount += 1
        # print(line)
        # print(lineCount)
        
        if comment_paragraph1 in line:
            while comment_paragraph1 not in line:
                line = next(Lines)
                lineCount += 1
                newFile.write(line)
                print(line)
            continue
        # print(line)
        if comment_paragraph2 in line:
            # print(line)
            while comment_paragraph2 not in line:
                line = next(Lines)
                lineCount += 1
                newFile.write(line)
                # print(line)
            continue
            
        if comment_line in line:
            line = line.split("#")[0]
        
        if "def " in line:
            functionName = line.split('(')[0]
            functionName = functionName.replace('def', '')
            functionName = functionName.replace(' ', '')
            # mulLine, bracketStack = checkMultiline(line)
            # print(functionName)
            while ':' not in line:
                line = next(Lines)
                lineCount += 1
                newFile.write(line)
            continue
        
        chars_to_remove = ['==', '>=', '<=', '!=']
        for char_to_remove in chars_to_remove:
            line = line.replace(char_to_remove, '')
        
            
        if "=" in line:
            
            variableName = line.split('=')[0]
            variableName, sCount = spaceCount(variableName)
            spaces = ' ' * sCount
            variableName = variableName.replace(' ', '')
            if '\"' in variableName:
                continue
            if '[' in variableName:
                insideBracket = re.findall("\[.+\]", variableName)
                for iB in insideBracket:
                    variableName = variableName.replace(iB, '')
            if '.flat' in variableName:
                variableName = variableName.replace('.flat', '')
                
            mulLine, bracketStack = checkMultiline(line)            
            
            while len(bracketStack) != 0 or mulLine:
                # print(bracketStack)
                line = next(Lines)
                lineCount += 1
                newFile.write(line)
                mulLine, bracketStack = checkMultiline(line, bracketStack)
            if "," in variableName:
                variableNames = variableName.split(',')
                # print("hue,", variableNames)
                for v in variableNames:
                    add_decorator(newFile, spaces, functionName, v, lineCount)
                continue
            operators = ['+', '-', '*', '/']
            if any(operator in variableName for operator in operators):
                for oprt in operators:
                    variableName = variableName.replace(oprt, '')
                add_decorator(newFile, spaces, functionName, variableName, lineCount)
                continue
            if 'with' in variableName:
                continue
            
            
            add_decorator(newFile, spaces, functionName, variableName, lineCount)
            continue
        mulLine, bracketStack = checkMultiline(line)
        # print(mulLine, bracketStack)
        while len(bracketStack) != 0 or mulLine:
            line = next(Lines)
            lineCount += 1
            newFile.write(line)
            mulLine, bracketStack = checkMultiline(line, bracketStack)
    newFile.close()
    os.remove('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation.py')

    os.rename('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/APFileNew.py', '/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation.py')

def editFileForRun2():
    file1 = open('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation.py', 'r')
    Lines = file1.readlines()
    
    newFile = open('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/APFileNewTemp.py', 'w')

    for line in Lines:
        line = line.replace('#<SecondRun>', '')
        if '#<FirstRun>' not in line:
            newFile.write(line)
    os.remove('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation.py')
    os.rename('/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/APFileNewTemp.py', '/Users/muyeedahmed/Desktop/DecoratorTest/scikit-learn/sklearn/cluster/_affinity_propagation.py')




import numpy as np
import pandas as pd
    
if __name__ == "__main__":
    
    # CreateNewFile()
    # from sklearn.cluster import AffinityPropagation
    # filepath = '/Users/muyeedahmed/Desktop/Research/Dataset/robot-failures-lp1.csv'
    # X = pd.read_csv(filepath)
    # X=X.to_numpy()
    
    # # # # X = np.array([[1, 2], [1, 4], [1, 0], [4, 2], [4, 4], [4, 0]])
    # # # # X = np.random.rand(10,4)
    # # # # X = np.random.randint(5, size=(2000, 4))
    
    # clustering = AffinityPropagation(random_state=None).fit(X)
    # print(clustering.cluster_centers_)
    
    
    # editFileForRun2()
    # trace = open('Trace.csv', 'w')
    # trace.write("Variable Name,Function Name,Line Count,iteration,Same Value)}\n")
    # trace.close()    
    
    # from sklearn.cluster import AffinityPropagation
    # clustering = AffinityPropagation(random_state=None).fit(X)
    # print(clustering.cluster_centers_)
    
    trace = pd.read_csv('Trace.csv')
    INIT = []
    ITER = []
    seq = []
    StartOfLoop = -1
    for i in range(trace.shape[0]):
        if trace['iteration'][i] == 1 and StartOfLoop == -1:
            INIT.append(trace['Line Count'][i])
        if trace['iteration'][i] > 1 or StartOfLoop > -1:
            if trace['Line Count'][i] in INIT:
                INIT.remove(trace['Line Count'][i])
            if  trace['Line Count'][i] == StartOfLoop:
                ITER = list(set(ITER+seq))
            if StartOfLoop == -1:
                StartOfLoop = trace['Line Count'][i]
                ITER.append(trace['Line Count'][i])
            seq.append(trace['Line Count'][i])
            # iterationValue = trace['iteration'][i]

    print(ITER)
    
    
