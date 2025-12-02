import itertools
import tkinter as tk  
import sys
import os
import time

initChars = "abcdefghijklmnopqrstuvwxyz" 

def resourcePath(relativePath):
  base_path = getattr(sys, '_MEIPASS', None)
  if base_path is None:
      base_path = os.path.dirname(os.path.abspath(__file__)) 
  return os.path.join(base_path, relativePath)

def checkPermutations():
  startTime = time.perf_counter()
  activeChars = []
  count=0
  combination=0
  wordlist = []
  letters = []

  list = root.nametowidget('listbox')
  list.delete(0, tk.END)
  label = root.nametowidget('info')
  label.config(text="")
  for i in range (26):
    checkb = alphpabetContainer.nametowidget(f'check{initChars[i]}')
    varname = checkb.cget("variable")
    state = root.getvar(varname)
    if int(state):
        activeChars.append(checkb.cget("text").lower())
  activeChars="".join(activeChars)
  permutations = itertools.product(activeChars, repeat=5)

  for i in range(5):
    entry = letterContainer.nametowidget(f'entry{i}')
    letters.append(entry.get().lower() if entry.get() != "" else None)

  l1,l2,l3,l4,l5 = letters  
  for permutation in permutations: 
    if ((permutation[0] == l1 or l1 is None)
        and (permutation[1] == l2 or l2 is None)
        and (permutation[2] == l3  or l3 is None)
        and (permutation[3] == l4 or l4 is None)
        and (permutation[4] == l5  or l5 is None)):

      word = "".join(permutation)
      if word in words:
        wordlist.append(word)
        count+=1     
      combination+=1

  endTime = time.perf_counter()
  timeTaken = endTime - startTime
  updateWindow(wordlist, count, combination, timeTaken)

def updateWindow(wordlist, count, combination, timeTaken):
  label.config(text=f"Total valid words found: {count}\nTotal combinations checked: {combination}\nTime taken: {timeTaken:.6f} seconds")
  label.grid(row=0, column=2, pady=10)

  for w in wordlist:
    list.insert(tk.END, w)
  list.grid(row=1, column=2)

validWordFile = resourcePath(r"valid-wordle-words.txt")
with open(validWordFile, "r") as open_file:
  words = set(open_file.read().splitlines())

root = tk.Tk()
root.title("Wordle Helper")
alphpabetContainer = tk.Frame(root, relief="solid", borderwidth=1, padx=5, pady=5, background="grey30")
alphpabetContainer.grid(row=0, column=0)
letterContainer = tk.Frame(root, relief="solid", borderwidth=1, padx=5, pady=5, background="grey30")
letterContainer.grid(row=1, column=0)
alphpabetCount = 0
defaultChecked = tk.IntVar(value=1)

list = tk.Listbox(root, name='listbox', font=('Arial', 14), relief="solid", borderwidth=1)
label = tk.Label(root, name='info', font=('Arial', 14))
label.config(text=f"Type in known letters into the boxes and deselect unused letters.\n\nClick 'Find Words' to search for possible words.")
label.grid(row=2, column=0, pady=10)  
check = tk.Button(root, text="Find Words", height=2, width=15, font=('Arial', 14), relief="solid", borderwidth=1, background="grey30", fg="grey80", command=checkPermutations)
check.grid(row=1, column=1)

for chars in initChars:
  var = tk.IntVar(value=1) 
  checkb = tk.Checkbutton(alphpabetContainer, text=chars.upper(), font=('Arial', 15), variable=var, name=f'check{chars}', background="grey40")
  checkb.var = var
  checkb.grid(row=0, column=alphpabetCount, padx=1, sticky='w')
  alphpabetCount += 1

for i in range(5):
  entry = tk.Entry(letterContainer, width=2, font=('Arial', 24), name=f'entry{i}', background="grey80", justify='center') 
  entry.grid(row=1, column=i, padx=5, pady=5, sticky='w')
  entry.bind("<KeyRelease>", lambda event, e=entry: e.delete(1,"end") if len(e.get()) > 1 else None)

root.geometry("1750x350")
root.resizable(False, False)
root.config(background="grey40")
root.grid_columnconfigure(0, weight=1) 
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

show = root.mainloop()
try: 
  root.winfo_exists()
except tk.TclError as e:
  e=str(e).capitalize()
  print(f"{e} - (The program has likely been closed.)")
else:
  show()