import os

from chaining.backward_chaining import BackwardChaining
from chaining.forward_chaining import ForwardChaining

program = ""
while True:
    print("Do you want to use Forward or Backward chaining?")
    print("FC - Forward chaining")
    print("BC - Backward chaining")
    program = input()
    if program == "FC" or program == "BC":
        break
    print("Incorrect choice.")

file_name = ""
while True:
    file_name = input("Enter file name:\n")
    if os.path.isfile(file_name):
        break
    else:
        print("File not found.")

if program == "FC":
    ForwardChaining(file_name)
if program == "BC":
    BackwardChaining(file_name)
