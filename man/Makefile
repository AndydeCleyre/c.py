# Copyright (c) 2015-2016 Stefan Tatschner
#
# doc/Makefile
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

RST_MAN				= rst2man
RST_MAN_FLAGS		=
RST_HTML			= rst2html5-mg
RST_HTML_FLAGS		= --bootstrap-css

MAN1_RSTS	= $(wildcard *.1.rst)
DOC_MAN1	= $(patsubst %.rst,%,$(MAN1_RSTS))
MAN_RST		= $(MAN1_RSTS)
DOC_HTML	= $(patsubst %.rst,%.html,$(MAN_RST))
INCLUDES	= footer.rst
CSS			=

all: man html

man: man1
man1: $(DOC_MAN1)

html: $(DOC_HTML)

%.1 : %.1.rst $(INCLUDES)
	$(RST_MAN) $(RST_MAN_FLAGS) $< $@

%.html : %.rst $(INCLUDES) $(CSS)
	$(RST_HTML) $(RST_HTML_FLAGS) $< $@
