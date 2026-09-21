#!/usr/bin/env python3

import sys
import re

# Usage: python circuitParse.py inputFile
def main():
  input_file = sys.argv[1]
  inputs = []
  outputs = []
  gates = []

  with open(input_file) as f:
    for line in f:
      res = re.split(r'[(=,)]', line)

      if res[0] == "INPUT":
        inputs.append(res[1])
      elif res[0] == "OUTPUT":
        outputs.append(res[1])
      else:
        cnt = len(res)
        tmpgates = []
        tmpgates.append(res[0])
        tmpgates.append(res[1])
        cnt = cnt - 3
        tmpgates.append(cnt)
        for i in range(cnt):
          tmpgates.append(res[2+i])
        gates.append(tmpgates)

  # print(inputs)
  # print(outputs)
  # print(gates)

  with open("output.txt", "w") as f:
    f.write("Inputs: ")
    for i in inputs:
      f.write(i + ", ")
    f.write('\n')

    f.write("Outputs: ")
    for i in outputs:
      f.write(i + ", ")
    f.write('\n')

    f.write("Gates: " + '\n')
    for gate in gates:
      f.write(str(gate[0]) + ": " + str(gate[2]) + "-input" + str(gate[1]) + " of ")
      for i in range(gate[2]):
        f.write(str(gate[3+i]) + ",")
      f.write('\n')

  





if __name__ == '__main__':
  main()