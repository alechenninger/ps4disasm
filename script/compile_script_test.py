try:
  from script.compile_script import *
except:
  from compile_script import *

import unittest

class CompileScriptTest(unittest.TestCase):
  def test_line_wrap(self):
    asm = dialog(Context(), '$01', "This is a test of a long line that should wrap.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"This is a test of a long line"
	dc.b	$FC
	dc.b	"that should wrap."
	dc.b	$FD''')

  def test_double_space(self):
    asm = dialog(Context(), '$01', "Maintains  a double space.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"Maintains  a double space."
	dc.b	$FD''')

  def test_can_end_line_after_dash(self):
    asm = dialog(Context(), '$01', "It is testing a very long line--broken by dashes.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"It is testing a very long line--"
	dc.b	$FC
	dc.b	"broken by dashes."
	dc.b	$FD''')

  def test_cannot_end_line_between_dashes(self):
    asm = dialog(Context(), '$01', "It's a test of a very long line--with dashes.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"It's a test of a very long"
	dc.b	$FC
	dc.b	"line--with dashes."
	dc.b	$FD''')

  def test_continues_second_line(self):
    asm = dialog(Context(), '$01', "Our fortune took flight, on swift wings from 'the desert garden'.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"Our fortune took flight, on"
	dc.b	$FC
	dc.b	"swift wings from 'the desert"
	dc.b	$FD
	dc.b	"garden'."
	dc.b	$FD''')

  def test_continues_third_line(self):
    asm = dialog(Context(), '$01', "We'll meet head-on whatever the guild throws our way.  They'll have to go looking for new cases instead of waiting for the work to come in.")
    self.assertEquals(asm(), '''	dc.b	$F4
	dc.b	$01
	dc.b	"We'll meet head-on whatever the"
	dc.b	$FC
	dc.b	"guild throws our way.  They'll"
	dc.b	$FD
	dc.b	"have to go looking for new cases"
	dc.b	$FC
	dc.b	"instead of waiting for the work"
	dc.b	$FD
	dc.b	"to come in."
	dc.b	$FD''')

  def test_script(self):
    asm = compile('''Alys: This is so great I can't believe this is a thing.
Shay: How cool! Way to go!''')

    self.assertEquals(asm, '''	dc.b	$F4
	dc.b	$02
	dc.b	"This is so great I can't believe"
	dc.b	$FC
	dc.b	"this is a thing."
	dc.b	$FD
	dc.b	$F4
	dc.b	$01
	dc.b	"How cool! Way to go!"
	dc.b	$FD''')

if __name__ == '__main__':
    unittest.main()