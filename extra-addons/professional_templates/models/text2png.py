# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://opensource.org/licenses/LGPL-3.0).
#
#This software and associated files (the "Software") may only be used (executed,
#modified, executed after modifications) if you have purchased a valid license
#from the authors, typically via Odoo Apps, or if you have received a written
#agreement from the authors of the Software (see the COPYRIGHT section below).
#
#You may develop Odoo modules that use the Software as a library (typically
#by depending on it, importing it and using its resources), but without copying
#any source code or material from the Software. You may distribute those
#modules under the license of your choice, provided that this license is
#compatible with the terms of the Odoo Proprietary License (For example:
#LGPL, MIT, or proprietary licenses similar to this one).
#
#It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#or modified copies of the Software.
#
#The above copyright notice and this permission notice must be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#DEALINGS IN THE SOFTWARE.
#
#########COPYRIGHT#####
# © 2017 Bernard K Too<bernard.too@optima.co.ke>
from StringIO import StringIO
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from os.path import dirname, abspath, join, isdir, exists
default_font = join(dirname(dirname(abspath(__file__))), "static", "src","fonts", "Dosis-Regular.ttf")

def text2png(text, color = "#EEEEEE", bgcolor = None, fontfullpath = exists(default_font) and default_font or None, 
        transpose=None, fontsize = 300, leftpadding = 1000, rightpadding = 20, toppadding=1200):
        """ Method to convert watermark text to image that will be merged with the report PDF
        """
        width =4960; height=7020; dpi=600;
        #width =2480; height=3508; dpi=300;
        #width =595; height=842; dpi=72;
	REPLACEMENT_CHARACTER = u'\uFFFD'
	NEWLINE_REPLACEMENT_STRING = ' ' + REPLACEMENT_CHARACTER + ' '


	font = ImageFont.load_default() if fontfullpath == None else ImageFont.truetype(fontfullpath, int(fontsize* dpi/72))
	text = text.replace('\n', NEWLINE_REPLACEMENT_STRING)

	lines = []
	line = u""

	for word in text.split():
            ##print word
		if word == REPLACEMENT_CHARACTER: #give a blank line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""
			lines.append( u"" ) #the blank line
		elif font.getsize( line + ' ' + word )[0] <= (width - rightpadding - leftpadding):
			line += ' ' + word
		else: #start a new line
			lines.append( line[1:] ) #slice the white space in the begining of the line
			line = u""

			#TODO: handle too long words at this point
			line += ' ' + word #for now, assume no word alone can exceed the line width

	if len(line) != 0:
		lines.append( line[1:] ) #add the last line

	line_height = font.getsize(text)[1] + int(8 * dpi/72) #line spacing scales with the dpi
        #img_height = line_height * (len(lines) + 1)

	img = Image.new("RGB", (width, height), bgcolor and bgcolor)
	draw = ImageDraw.Draw(img)

	y = toppadding
	for line in lines:
		draw.text( (leftpadding, y), line, color, font=font)
		y += line_height

        if transpose is not None:
            img = img.transpose(int(transpose))
        img.save('testo.pdf', resolution=600)
        return img

#show time
#text2png(u"This is\na\ntest şğıöç zaa xd ve lorem hipster", 'test.png', fontfullpath = "font.ttf")
#text2png(u"SPECIMEN\n 1234567890", 'test.png', fontfullpath = "/Users/btoo/odoo-10.0/optima/theme_common/static/src/font/Dosis-Regular.ttf")
