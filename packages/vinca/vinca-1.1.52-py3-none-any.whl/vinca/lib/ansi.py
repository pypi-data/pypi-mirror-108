# ansi codes let us control the terminal just
# by printing special escape sequences
# I make heavy use of those ending in 'm'
# codes 1-10 control text attributes
# codes in the 30s control foreground color
# codes in the 40s control background color
esc = '\033['
ansi = {'reset': esc+'0m',
        'bold': esc+'1m', 'b': esc+'1m',
        'light': esc+'2m', 'dim': esc+'2m',
        'italic': esc+'3m', 'it': esc+'3m',
        'underlined': esc+'4m', 'u': esc+'4m',
        'blink': esc+'5m', 'flash': esc+'5m', 'f': esc+'5m',
        'highlight': esc+'7m', 'hi': esc+'7m', 'reverse': esc+'7m',  'mark': esc+'7m',
        'hidden': esc+'8m', 'invisible': esc+'8m',
        'red': esc+'31m', 'r': esc+'31m',
        'green': esc+'32m', 'g': esc+'32m',
        'yellow': esc+'33m',
	'blue': esc+'34m',
	# the next escape codes are more powerful
	'clear': esc+'2J',
	'move_to_top': esc+'H',  # home
	'hide_cursor': esc+'?25l',
	'show_cursor': esc+'?25h',
	'save_cursor': esc+'s',
	'restore_cursor': esc+'u',
	'save_screen': esc+'?47h',
	'restore_screen': esc+'?47l',
	'move_up_line': esc+'F',
	'clear_line': esc+'K',
	}
