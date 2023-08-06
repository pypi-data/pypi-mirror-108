import argparse
from vinca.lib import classes
from pathlib import Path
collection = classes.collection
deckdict = classes.deckdict

import datetime
TODAY = datetime.date.today()
DAY = datetime.timedelta(days=1)

# type checking
def deck_type(arg):
	if arg.isdigit(): arg = int(arg)
	assert arg in deckdict.keys(), f'Bad deck {arg}. \
		Use [d] to list decks'
	return deckdict[arg]
def card_type(arg):
	assert arg.isdigit()
	assert int(arg) in collection.id_list, f'Bad id {arg}. \
		Use [q] or [f] to search for a card.'
	return classes.Card(arg)
def deck_or_card(arg):
	if arg.isdigit(): arg = int(arg)
	if arg in deckdict.keys():  # can be deck's name or deck id
		return deckdict[arg]
	if arg in collection.id_list:
		return classes.Card(arg) 
	raise argparse.ArgumentTypeError(f'''\n\n
		"{arg}" is neither a deck nor a card.
		Valid arguments are:
		1) A deck name
		2) A deck id (use d to list deck ids)
		3) A card id (use q to search for a card id)''')
def date_type(arg):
	try:
		return TODAY + int(arg) * DAY
	except:
		pass  # arg cannot be interpreted as an integer
	try:
		return datetime.date(*[int(x) for x in arg.split('-')])
	except:
		raise argparse.ArgumentTypeError(f'''\n\n
			Invalid Date: {arg}. Valid dates are:
			1) -7		(one week ago)
			2) 2021-06-03	(June 3rd)''')

# argument parsing
parser = argparse.ArgumentParser()
parser.set_defaults(decks = [], cards = [],
	decks_or_cards = [], func = 'statistics', mode='normal')
subparsers = parser.add_subparsers()
# commands which take a deck as an argument
one_liner_parser = subparsers.add_parser('one_liner',aliases=['1'],
	help='add a basic card quickly')
one_liner_parser.add_argument('decks',type=deck_type,nargs='*')
one_liner_parser.set_defaults(func = 'one_liner')

linear_add_parser = subparsers.add_parser('linear_add',aliases=['l'],
	help='for lyrics, poetry, oratory, etc.')
linear_add_parser.add_argument('decks',type=deck_type,nargs='*')
linear_add_parser.set_defaults(func = 'linear_add')

add_parser = subparsers.add_parser('add',aliases=['a'],
	help='add a basic card')
add_parser.add_argument('decks',type=deck_type,nargs='*')
add_parser.set_defaults(func = 'add')

add_many_parser = subparsers.add_parser('add_many',aliases=['A'],
	help='add several basic cards')
add_many_parser.add_argument('decks',type=deck_type,nargs='*')
add_many_parser.set_defaults(func = 'add_many')


image_cloze_parser = subparsers.add_parser('image_cloze',aliases=['ic'],
	help='generate an image cloze card')
image_cloze_parser.add_argument('image_path',type=Path)
image_cloze_parser.add_argument('decks',type=deck_type,nargs='*')
image_cloze_parser.set_defaults(func = 'image_cloze')

# QUERY
query_parent = argparse.ArgumentParser('query_parent',add_help=False)
query_parent.add_argument('pattern',nargs='?',default='')
# optional args of browser.query function
query_parent.add_argument('-v','--invert',action='store_true')
query_parent.add_argument('--decks',type=deck_type,nargs='+', default=[])
query_parent.add_argument('--cards',type=card_type,nargs='+', default=[])
query_parent.add_argument('--tags_include',nargs='+', metavar='TAGS')
query_parent.add_argument('--tags_exclude',nargs='+', metavar='TAGS')
query_parent.add_argument('--create_date_min',type=date_type, metavar='DATE')
query_parent.add_argument('--create_date_max',type=date_type, metavar='DATE')
query_parent.add_argument('--seen_date_min',type=date_type, metavar='DATE')
query_parent.add_argument('--seen_date_max',type=date_type, metavar='DATE')
query_parent.add_argument('--due_date_min',type=date_type, metavar='DATE')
query_parent.add_argument('--due_date_max',type=date_type, metavar='DATE')
query_parent.add_argument('--due_only',action='store_true')
query_parent.add_argument('--not_due_only',action='store_true')
query_parent.add_argument('--editor', type=str)
query_parent.add_argument('--reviewer', type=str)
query_parent.add_argument('--scheduler', type=str)
query_parent.add_argument('--deleted_only',action='store_true')
query_parent.add_argument('--show_deleted',action='store_true')
query_parent.add_argument('--new_only',action='store_true')
query_parent.add_argument('--not_new_only',action='store_true')
query_parent.add_argument('--no_fancy',action='store_true')
query_parent.set_defaults(func = 'query')

query_parser = subparsers.add_parser('query',aliases=['q'],
	parents=[query_parent],
	help='search collection for regexp and filter it')
query_parser.add_argument('-i','--id_only',action='store_true',
	help='only output the id of the match (facilitates piping)')
visual_query_parser = subparsers.add_parser('visual_query',aliases=['vq'],
	parents=[query_parent],
	help='search for regexp, filter it, and perform command on the selected card')
visual_query_parser.set_defaults(mode='visual')

# commands which take a deck or several cards as an argument 
study_parser = subparsers.add_parser('study',aliases=['s'],
	help='study the collection or selected deck')
study_parser.add_argument('decks_or_cards', type=deck_or_card, nargs='*')
study_parser.add_argument('--date', type=int,
	help='study as if today was [date]')
study_parser.set_defaults(func = 'study')

preview_parser = subparsers.add_parser('preview',aliases=['p'],
	help='preview the collection or selected deck')
preview_parser.add_argument('decks_or_cards', type=deck_or_card, nargs='*')
preview_parser.add_argument('--date', type=int,
	help='preview as if today was [date]')
preview_parser.set_defaults(func = 'preview')

statistics_parser = subparsers.add_parser('statistics',aliases=['S'],
	help='statistics about the selected deck or card')
statistics_parser.add_argument('decks_or_cards', type=deck_or_card, nargs='*')
statistics_parser.set_defaults(func = 'statistics')
# TODO miscellaneous options for more advanced statistics
edit_parser = subparsers.add_parser('edit',aliases=['e'],
	help='edit the selected deck or card')
edit_parser.add_argument('decks_or_cards',type=deck_or_card,nargs='*')
edit_parser.set_defaults(func = 'edit')

delete_parser = subparsers.add_parser('delete',aliases=['x'],
	help='delete the selected deck or card')
delete_parser.add_argument('decks_or_cards',type=deck_or_card, nargs='*')
delete_parser.set_defaults(func = 'delete')

# commands which take no arguments
# DECKS
list_decks_parser = subparsers.add_parser('list_decks',aliases=['d'],
	help='list decks')
list_decks_parser.set_defaults(func = 'list_decks')
visual_decks_parser = subparsers.add_parser('visual_decks',aliases=['vd'],
	help='select a deck and perform a command on it')
visual_decks_parser.set_defaults(func = 'list_decks', mode='visual')

# PURGE
purge_parser = subparsers.add_parser('purge',
	help='permanently delete all cards scheduled for deletion')
purge_parser.set_defaults(func = 'purge')

# commands which take a path as an argument (import / backup)
# IMPORT EXPORT
backup_parser = subparsers.add_parser('backup',aliases=['b','export'],
	help='backup all cards')
backup_parser.add_argument('backup_dest',type=Path)
backup_parser.add_argument('decks_or_cards',type=deck_or_card,nargs='*') 
backup_parser.set_defaults(func = 'backup')

import_parser = subparsers.add_parser('import',aliases=['i'],
	help='import a collection of cards')
import_parser.add_argument('import_path',type=Path)
import_parser.add_argument('-o','--overwrite',action='store_true',
	help='overwrite the existing collection')
import_parser.set_defaults(func = 'import_collection')

def get_parser():
	return parser
