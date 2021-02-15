#!/usr/bin/env python3

from collections.abc import Callable
from enum import Enum

import argparse

Compilable = Callable[[], str]
Data = str

QUOTES = ['"', '“', '”']

def string_data(d: str) -> Data:
  return '"' + d + '"'

def byte_data(d: int) -> Data:
  if d > 255:
    raise ValueError(d, 'must be <=255')
  return f'${d:0>2X}';

PORTRAIT = byte_data(244)
NEW_LINE = byte_data(252)
CONTINUE = byte_data(253)
END_DIALOG = byte_data(255)

class Context:
  pass

tokens: dict[str, Callable[[Context, str], Compilable]] = {
  "alys": lambda ctx, d: dialog(ctx, byte_data(2), d),
  "shay": lambda ctx, d: dialog(ctx, byte_data(1), d),
  "narrator": lambda ctx, d: dialog(ctx, byte_data(0), d),
  "text": lambda ctx, t: text(ctx, t),
}

transforms: dict[str, str] = {
  '‘': "'",
  '’': "'",
  '': "'",
  '–': '--',
  '…': '...',
}

class OpeningQuote:
  _quote = "<"

  def get(self):
    return (self._quote, ClosingQuote)

class ClosingQuote:
  _quote = ">"

  def get(self):
    return (self._quote, OpeningQuote)

def dialog(context: Context, portrait: Data, dialog: str) -> Compilable:
  dialog_stripped = dialog.strip()

  def compilable():
    lines = []
    line = ""
    break_point = 0
    quote, next_quote = OpeningQuote().get()

    lines.append(data_const([PORTRAIT]))
    lines.append(data_const([portrait]))
    
    def append(line: str):
      num_lines = len(lines)
      if (num_lines - 2) % 4 == 1:
        lines.append(data_const([NEW_LINE]))
      elif (num_lines - 2) % 4 == 3:
        lines.append(data_const([CONTINUE]))
      lines.append(data_const([string_data(line)]))

    for i, c in enumerate(dialog_stripped):
      c = transforms.get(c, c)

      # Update breakpoint to index if c is breakable based on context
      # If line is too long, break at breakpoint and add to new line and reset breakpoint
      # Else, add to line
      if is_breakable(c, dialog_stripped, i):
        break_point = len(line)

      if len(line) == 32:
        append(line[:break_point])
        line = line[break_point:].lstrip()
        break_point = 0

      if c in QUOTES:
        line += quote
        quote, next_quote = next_quote.get()
      elif c.isspace() and line == "":
        pass
      else:
        line += c
    
    if len(line) > 0:
      append(line)
    
    lines.append(data_const([CONTINUE]))
    
    return aggregate_compilable(lines)()
  
  return compilable

def text(context: Context, dialog: str) -> Compilable:
  dialog_stripped = dialog.strip()

  def compilable():
    lines = []
    line = ""
    break_point = 0
    quote, next_quote = OpeningQuote().get()
    
    def append(line: str):
      num_lines = len(lines)
      if (num_lines - 2) % 2 == 1:
        lines.append(data_const([END_DIALOG]))
      lines.append(data_const([string_data(line)]))

    for i, c in enumerate(dialog_stripped):
      c = transforms.get(c, c)

      # Update breakpoint to index if c is breakable based on context
      # If line is too long, break at breakpoint and add to new line and reset breakpoint
      # Else, add to line
      if is_breakable(c, dialog_stripped, i):
        break_point = len(line)

      if len(line) == 32:
        append(line[:break_point])
        line = line[break_point:].lstrip()
        break_point = 0

      if c in QUOTES:
        line += quote
        quote, next_quote = next_quote.get()
      elif c.isspace() and line == "":
        pass
      else:
        line += c
    
    if len(line) > 0:
      append(line)
    
    lines.append(data_const([END_DIALOG]))
    
    return aggregate_compilable(lines)()
  
  return compilable        

def compile(script: str) -> str:
  ctx = Context()
  return aggregate_compilable(
    [compile_line(ctx, l) for l in script.splitlines()])()

def compile_line(ctx: Context, line: str) -> Compilable:
  token, arg = line.split(sep=':', maxsplit=2)
  token = token.lower().strip()
  if token in tokens:
    return tokens[token](ctx, arg)
  raise ValueError(token, 'unknown token')

def data_const(d: list[Data]) -> Compilable:
  return lambda: '	dc.b	' + ','.join(d)

def aggregate_compilable(comps: list[Compilable]) -> Compilable:
  def compilable():
    return "\n".join(c() for c in comps)
  return compilable

def is_breakable(c: str, dialog: str, i: int) -> bool:
  if c.isspace():
    return True

  if c != '-' and i > 0 and dialog[i - 1] == '-':
    return True

  if c != '.' and i > 0 and dialog[i - 1] == '.':
    return True
  
  return False

parser = argparse.ArgumentParser(description='Compiles a script DSL into PSIV dialog asm')
parser.add_argument('script',type=open)
args = parser.parse_args()

with args.script as script:
  print(compile(script.read()))