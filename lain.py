#!/bin/python
# -*- coding: utf-8 -*-

from os import system
from sys import argv,stdout
import r2pipe
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import Python3Lexer
from pygments.style import Style
from pygments.token import Token
import readline
import signal

def sigint_handler(signum, frame):
    print ''
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def printh(input):
   stdout.write("\x1b[0;35m")
   stdout.write("│ ")
   stdout.write("\x1b[0;33m")
   stdout.write(highlight(input, Python3Lexer(), Terminal256Formatter(style="friendly"))[:-1].replace("# ","") + "\n")

def output(fun,calls,argz,addrlist,funlist,locals,globals,modvars):
   binary = open(fun,"rb").read() # read file
   binary = binary.split("\n") # split into array
   bin    = []
   esp    = ""
   name   = fun.split("_")[1] # function name
   falst = " ".join(funlist)
   print("\x1b[0;35m┌ ")
   for i in range(len(binary)):
       try:
          if "# esp" in binary[i]:
             esp = binary[i].split(" = ")[0].replace(" ","")

          if not binary[i] == "" and not binary[i].replace(" ","").startswith("#") and not "# esp" in binary[i] and not '__name_' in binary[i] and not 'import' in binary[i] and not 'sys.exit' in binary[i]:
             if "# 0x" in binary[i]:
                bin.append(binary[i].split("# 0x")[0])
             else:
                bin.append(binary[i])
       except:
             pass

   for line in range(len(bin)):
      try:

         for j in range(1,9):
            pt = ["(","&"," ",", ",")",""]
            for p in pt:
               l = "{}v{}".format(p,j)
               g = "{}g{}".format(p,j)
               if (l in  bin[line] or g in bin[line]) and not "*v{}".format(j) in bin[line]:
                  bin[line] = bin[line].replace("{}v".format(p),"{}{}_".format(p,locals))
                  if "global " in bin[line]:
                     bin[line] = bin[line].replace("{}g{}".format(p,j),"{}{}_{}".format(p,globals,j))
                  else:
                     bin[line] = bin[line].replace("{}g{}".format(p,j),"{}{}_{}".format(p,globals,j))

         if not len(modvars) == 0:
            for i in modvars:
               o = i.split(" ")
               if name == o[0] and not o[1] in falst:
                     bin[line] = bin[line].replace(o[1],o[2])

         if "printf(&format)" in bin[line] or "printf(0x" in bin[line]:
            printh(bin[line].replace(bin[line].split("printf(")[1].split(")")[0],bin[line-1].split(" = ")[1]))

         elif "scanf(&format)" in bin[line]:
            printh(bin[line].replace("&format","{}, {}".format(bin[line-1].split(" = ")[1],bin[line-2].split(" = ")[1])))

         elif "def " in bin[line]:
            function_name = bin[line].replace(bin[line].split(" ")[1].split("(")[0],name)
            try:
               if "()" in bin[line]:
                  for i in range(100):
                     if "str" in bin[line+i] and not "str = " in bin[line+i]:
                        function_name = bin[line].replace("()","(str)")
                        break
               if "function_" in bin[line]:
                   for i in range(len(addrlist)):
                        if bin[line].split("_")[1].split("(")[0][-3:] == addrlist[i][-3:]:
                            function_name = function_name.replace(bin[line].split(" ")[1].split("(")[0],funlist[i])

               printh(function_name)
            except:
               printh(bin[line].replace(bin[line].split(" ")[1].split("(")[0],name))

         elif "strcmp(0, NULL)" in bin[line]:
            printh(bin[line].replace("0, NULL","{}, {}".format(bin[line-1].split(" = ")[1],bin[line-2].split(" = ")[1])))

         elif bin[line].split("(")[0].replace(" ","") in calls:
            list = bin[line].split("(")[1].split(")")[0].split(",") # function argz
            function_name = bin[line]  # to change function name change bin[line]

            if "function_" in bin[line]:
               for i in range(len(addrlist)):
                  if bin[line].split("_")[1].split("(")[0][-3:] == addrlist[i][-3:]:
                     function_name = bin[line].replace(bin[line].split("(")[0].replace(" ",""),funlist[i])
                     break

            if not len(modvars) == 0:
               for i in modvars:
                  o = i.split(" ")
                  if o[1] in falst:
                     function_name = function_name.replace(o[1],o[2])

            if ":" in bin[line-1]:
               pass
            elif "()" in bin[line] and "v1" in bin[line-1]:
               argzz = ""
               for i in range(1,10):
                  if ("*v1" in bin[line-i] or "v1[" in bin[line-i]):
                     argzz += bin[line-i].split("=")[1] + ", "
                  else:
                     break
               function_name = function_name.replace("()","({})".format(argzz.replace(" ","")[:-1]))
            elif not list[0] == "":
               index = ""
               try:
                  for i in range(len(list)):
                     index += bin[line-(i+1)].split(" =")[1]
                  function_name = function_name.replace(bin[line].split("(")[1].split(")")[0],",".join(index[1:].split(" "))).replace(",)",")")
               except:
                   pass
            printh(function_name)
         else:
            if not "   *{}".format(esp) in bin[line] and not "{}[".format(esp) in bin[line]:
               if not "*((&" in bin[line] and not ")   " in bin[line+1]:
                  if not "{}_1[4] =".format(locals) in bin[line]:
                     printh(bin[line])
      except:
         printh(bin[line])
   print("\x1b[0;35m└ ")

def main():
   calls   = []
   argz    = []
   locals  = "loc" # local varibales defualt name
   globals = "glob" # globals varibales defualt name
   print("\x1b[0;31m[+] Decompiling Program")
   try:
      open("/tmp/{}".format(argv[1]),"rb")
   except:
      system("retdec-decompiler.py -k -l py -o /tmp/{} {} 2>&1 > /dev/null".format(argv[1],argv[1]))

   code = open("/tmp/{}".format(argv[1]),"rb").read()
   code = code.split("\n")

   for i in range(len(code)):
      if "def" in code[i]:
         calls.append(code[i].split(" ")[1].split("(")[0])
         argz.append(len(code[i].split("def ")[1].split("(")[1].split(")")[0].split(",")))

   print("\x1b[0;31m[+] Analyzing Program")
   r2 = r2pipe.open(argv[1])
   r2.cmd("aaa")
   funlist = r2.cmd("afll").split("\n")
   funname = [] # function names
   addrlst = [] # function start addresses
   modvar  = [] # modified variables
   r2.cmd("e asm.bytes = false ; e asm.comments = false")
   path = None
   for i in range(2,len(funlist) - 3):
      funname.append((map(filter(None,funlist[i].split(" ")).__getitem__, [-1])[0]))
      addrlst.append(funlist[i].split(" ")[0])

   while True:
    try:
      function = raw_input("\x1b[0;33m[#] ").split(" ")
      if function[0] == "info" or function[0] == "i":
         if function[1] == "functions" or function[1] == "f":
             print("\x1b[0;35m┌ ")
             for i in range(len(funname)):
                 printh("{}  {}".format(addrlst[i],funname[i]))
             print("\x1b[0;35m└ ")
         elif function[1] == "strings" or function[1] == "s":
             print("\x1b[0;35m┌ ")
             strings = r2.cmd("iz").split("\n")
             for i in range(2,len(strings)-1):
                printh("{}  {}".format(strings[i].split(" ")[2],strings[i].split("ascii")[-1]))
             print("\x1b[0;35m└ ")
      elif function[0] == "exit" or function[0] == "quit":
         exit(0)
      elif function[0] == "?":
          print("\x1b[0;35m┌ ")
          for l in r2.cmd("? {}".format(function[1])).split("\n"):
             printh(l)
          print("\x1b[0;35m└ ")
      elif function[0] == "clear" or function[0] == "c":
          system("clear")
      elif function[0] == "rename" or function[0] == "r":
         if path == None:
            print("[x] Decompile First")
         elif function[1] == "locals" or function[1] == "l":
            locals = function[2] # local variables name
         elif function[1] == "globals" or function[1] == "g":
            globals = function[2] # local variables name
         else:
            if len(modvar) == 0:
               modvar.append(path.split("_")[1] + " " + function[1] + " " + function[2])
            else:
               for i in range(len(modvar)):
                  m = modvar[i].split(" ")
                  if function[1] == m[2]:
                      modvar[i] = modvar[i].replace(m[2],function[2])
                      break
                  else:
                      modvar.append(path.split("_")[1] + " " + function[1] + " " + function[2])

            for j in range(len(funname)):
               if function[1] in funname[j]:
                  r2.cmd("afn {} {}".format(function[2],funname[j]))
                  funlist = r2.cmd("afll").split("\n")
                  funname = []
                  for i in range(2,len(funlist) - 3):
                     funname.append((map(filter(None,funlist[i].split(" ")).__getitem__, [-1])[0]))


      elif function[0] == "decompile" or function[0] == "d":
         indx = -1
         for i in range(len(funname)):
             if function[1] == funname[i] or "sym.{}".format(function[1]) == funname[i]:
                 indx = i
                 break

         if indx == -1:
             print("[x] Function Not Found")
         else:

            rx = '-'.join(map(filter(None,funlist[indx+2].split(" ")).__getitem__, [6,8]))
            path = "/tmp/{}_{}".format(argv[1],function[1])
            try:
                open(path,"rb")
            except:
                system("retdec-decompiler.py --select-ranges {} -l py {} -o {} 2>&1 > /dev/null".format(rx,argv[1],path))
            output(path,calls,argz,addrlst,funname,locals,globals,modvar)
    except:
       exit()


if __name__ == '__main__':
   main()
