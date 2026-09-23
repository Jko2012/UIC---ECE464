#!/usr/bin/env python3

import sys
import re

# Usage: python circuitParse.py inputFile
def main():
  input_file = sys.argv[1]
  inputs = [] #list of tuples, (node, level)
  outputs = [] #list of tuples, (node, level)
  gates = [] #each entry is [node, level, type, numInputs, {inputNode0, inputNode1, ... , inputNodeN}]
  unleveledGates = set() #same as gates

  tmpOutputs = []

  with open(input_file) as f:
    for line in f:
      if line[0] == "#":
        continue

      res = re.split(r'[(=,)]', line)

      if res[0] == "INPUT":
        tmpinput = (res[1].strip(), 0)
        inputs.append(tmpinput)
      elif res[0] == "OUTPUT":
        tmpOutputs.append(res[1].strip())
      elif len(res) >= 3:
        cnt = len(res)
        tmpgate = []
        tmpgate.append(res[0].strip())
        tmpgate.append(0)
        tmpgate.append(res[1].strip())
        cnt = cnt - 3
        tmpgate.append(cnt)
        tmpinputs = set()
        for i in range(cnt):
          tmpinputs.add(res[2+i].strip())
        tmpgate.append(tuple(tmpinputs))
        unleveledGates.add(tuple(tmpgate))

  print(inputs)
  print(tmpOutputs)
  print(unleveledGates)

  tmpgates = []
  for gate in unleveledGates: #first find gates with only level 0 nodes as input
    #find each gate's level
    skipgate = False
    level = 0
    for input in gate[4]: #take each input for the gate
      foundMatch = False

      for node in inputs: #check each level 0 node
        if input == node[0]: #look for matching level 0 node
          level = 1
          foundMatch = True #indicate we found a node match

      if foundMatch == False: #if any gate inputs are not a level 0 node, skip it for later
        skipgate = True

    if skipgate:
      continue

    tmpgates.append(gate)
    tmpgate = list(gate)
    tmpgate[1] = level
    gates.append(tmpgate)

  for gate in tmpgates:
    unleveledGates.remove(gate)

  while len(unleveledGates) > 0:
    tmpgates = []
    for gate in unleveledGates: #find gates with other gates as input
      #find each gate's level
      skipgate = False
      level = 0
      for input in gate[4]: #take each input for the gate
        foundMatch = False

        
        for node in inputs: #check each level 0 node
          if input == node[0]: #look for matching level 0 node
            level = 1
            foundMatch = True #indicate we found a node match
            
        for node in gates: #check each gate
          if input == node[0]: #look for matching input node
            if (node[1] + 1) > level: 
              level = (node[1] + 1) #level of gate is 1 greater than input node
            foundMatch = True #indicate we found a node match
  
        if foundMatch == False: #if any gate inputs are not a leveled gate, skip it for later
          skipgate = True
  
      if skipgate:
        continue

      tmpgates.append(gate)
      tmpgate = list(gate)
      tmpgate[1] = level
      gates.append(tmpgate)
    
    for gate in tmpgates:
      unleveledGates.remove(gate)

  for node in tmpOutputs:
    for gate in gates:
      if node == gate[0]:
        tmp = (node, gate[1])
        outputs.append(tmp)



  with open("output.txt", "w") as f:
    f.write("Inputs: ")
    for i in inputs:
      f.write(i[0] + ", ")
      f.write("level 0")
    f.write('\n')

    f.write("Outputs: ")
    for i in outputs:
      f.write(i[0] + ", level " + str(i[1]))
      f.write('\n')

    f.write("Gates: " + '\n')
    for gate in gates:
      f.write(str(gate[0]) + ": " + str(gate[3]) + "-input " + str(gate[2]) + " of ")
      for i in gate[4]:
        f.write(str(i) + ", ")
      f.write("level " + str(gate[1]))
      f.write('\n')

  





if __name__ == '__main__':
  main()