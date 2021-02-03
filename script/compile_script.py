from collections.abc import Callable
from enum import Enum

import argparse

Compilable = Callable[[], str]
Data = str

quotes = ['"', '“', '”']

class Context:
  pass

class OpeningQuote:
  _quote = "<"

  def get(self):
    return (self._quote, ClosingQuote)

class ClosingQuote:
  _quote = ">"

  def get(self):
    return (self._quote, OpeningQuote)

def dialog(context: Context, portrait: Data, dialog: str) -> Compilable:
  def compilable():
    lines = []
    line = ""
    next = ""
    break_point = 0
    quote, next_quote = OpeningQuote().get()

    lines.append(data_const([byte_data('$F4')]))
    lines.append(data_const([portrait]))
    
    def append():
      num_lines = len(lines)
      if num_lines % 2 == 1:
        lines.append(data_const([byte_data('$FC')]))
      elif num_lines > 2 and num_lines % 2 == 0:
        lines.append(data_const([byte_data('$FD')]))
      lines.append(data_const([string_data(line)]))

    def add_next():
      nonlocal line
      if next.isspace():
        return
      if len(line) + len(next) < 32:
        line += next
      else:
        append()
        line = next.strip()

    for i, c in enumerate(dialog.strip()):
      if c.isspace(): # is delimiter
        add_next()
        next = c
      elif c in quotes:
        next += quote
        quote, next_quote = next_quote.get()
      else:
        next += c
    
    add_next()
    append()
    lines.append(data_const([byte_data('$FD')]))
    
    return aggregate_compilable(lines)()
  
  return compilable
        

def compile(script: str) -> str:
  """
  Algorithm:
  1. Look at token in line
  Token determines function to parse line
  Pass it a context and the line
  Result is something which can spit out assembly
  Laziness might be important b/c context state can change while parsing.


  """ 
  pass

def data_const(d: list[Data]) -> Compilable:
  return lambda: '	dc.b	' + ','.join(d)

def aggregate_compilable(comps: list[Compilable]) -> Compilable:
  def compilable():
    return "\n".join(c() for c in comps)

  return compilable

def string_data(d: str) -> Data:
  return '"' + d + '"'

def byte_data(d: str) -> Data:
  return d;
