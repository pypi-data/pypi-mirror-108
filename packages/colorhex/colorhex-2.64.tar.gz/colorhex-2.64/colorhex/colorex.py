validhex = '0123456789ABCDEF'.__contains__

BOLD = '\033[1m'
BLINKING = '\033[5m'
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'

def formathex(data):
	return ''.join(filter(validhex, data.upper()))

def colorex(text, hexcode, style=None):
	"""Prints text in a color using a hex digit, aswell some styles too, such as bold, italic, blinking & underline text. The hex digit & style can be none, but text is required

	Example: 

	from colorex import *
	print(colorex('lol', '7289da', style=[BLINKING, BOLD, ITALIC, UNDERLINE]))"""

	hexint = int(formathex(hexcode), 16)

	if style is not None:
		return '\x1B[38;2;{};{};{}m{}{}\x1B[0m'.format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, ''.join(style), text)

	else:
		return '\x1B[38;2;{};{};{}m{}\x1B[0m'.format(hexint>>16, hexint>>8&0xFF, hexint&0xFF, text)