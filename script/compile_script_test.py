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

if __name__ == '__main__':
    unittest.main()