import argparse
from vinca.lib import classes
from pathlib import Path
collection = classes.collection
deckdict = classes.deckdict

import datetime

# type checking
def deck_type(arg):
	if arg.isdigit(): arg = int(arg)
	assert arg in deckdict.keys(), 'Bad deck. Use [d] to list decks'
	return deckdict[arg]
def card_type(arg):
	assert arg.isdigit()
	assert int(arg) in collection.id_list, 'Bad id. Use [q] to search for a card.'
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
		return datetime.date(*[int(x) for x in dd.split('-')])
	except:
		raise argparse.ArgumentTypeError('Bad Date. Try YYYY-MM-DD')

# argument parsing
parser = argparse.ArgumentParser()
parser.set_defaults(decks = [], cards = [],
	decks_or_cards = [], func = 'statistics')
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

query_parser = subparsers.add_parser('query',aliases=['q'],
	help='search collection for regexp')
query_parser.add_argument('pattern',nargs='?',default='')
query_parser.add_argument('-i', '--id_only',action='store_true',
	help='only output the id of the match')
query_parser.set_defaults(func = 'query')

filter_parser = subparsers.add_parser('filter',aliases=['f'],
	help='filter the collection')
filter_parser.add_argument('--decks',type=deck_type,nargs='+')
filter_parser.add_argument('--cards',type=card_type,nargs='+')
filter_parser.add_argument('--tags_include',nargs='+')
filter_parser.add_argument('--tags_exclude',nargs='+')
filter_parser.add_argument('--create_date_min',type=date_type)
filter_parser.add_argument('--create_date_max',type=date_type)
filter_parser.add_argument('--seen_date_min',type=date_type)
filter_parser.add_argument('--seen_date_max',type=date_type)
filter_parser.add_argument('--due_date_min',type=date_type)
filter_parser.add_argument('--due_date_max',type=date_type)
filter_parser.add_argument('--due_only',action='store_true')
filter_parser.add_argument('--not_due_only',action='store_true')
filter_parser.add_argument('--editor', type=str)
filter_parser.add_argument('--reviewer', type=str)
filter_parser.add_argument('--scheduler', type=str)
filter_parser.add_argument('--new_only',action='store_true')
filter_parser.add_argument('--not_new_only',action='store_true')
filter_parser.set_defaults(func = 'filter')

visual_query_parser = subparsers.add_parser('visual_query',aliases=['vq'],
	help='search for regexp and perform command on the selected card')
visual_query_parser.add_argument('pattern',nargs='?',default='')
visual_query_parser.set_defaults(func = 'visual_query')
# commands which take a deck or several cards as an argument 
study_parser = subparsers.add_parser('study',aliases=['s'],
	help='study the collection or selected deck')
study_parser.add_argument('decks_or_cards', type=deck_or_card, nargs='*')
study_parser.add_argument('--date', type=int,
	help='study as if today was [date]')
study_parser.set_defaults(func = 'study')

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
delete_parser.add_argument('-t','--toggle_delete',action='store_true',
	help='restore a card if it was previously deleted')
delete_parser.set_defaults(func = 'delete')

# commands which take no arguments
list_decks_parser = subparsers.add_parser('list_decks',aliases=['d'],
	help='list decks')
list_decks_parser.set_defaults(func = 'list_decks')

visual_decks_parser = subparsers.add_parser('visual_decks',aliases=['vd'],
	help='select a deck and perform a command on it')
visual_decks_parser.set_defaults(func = 'visual_decks')

purge_parser = subparsers.add_parser('purge',aliases=['p'],
	help='permanently delete all cards scheduled for deletion')
purge_parser.set_defaults(func = 'purge')

# commands which take a path as an argument (import / backup)
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
