# functions
from pathlib import Path
from subprocess import run
import datetime
today = datetime.date.today()
study_day = today

import readchar  # 3rd party module for reading a character one at a time

from vinca.lib import classes
col = classes.Collection()
col.cache_tags()
deckdict = classes.Deckdict()

from shutil import copytree, rmtree
from sys import exit

from vinca.lib import browser
from vinca.lib.ansi import ansi

vinca_path = Path(__file__) # /path/to/vinca/__init__.py
vinca_path = vinca_path.parent # /path/to/vinca
cards_path = vinca_path / 'data' / 'cards'
decks_path = vinca_path / 'data' / 'decks.txt'
decks_vimrc = vinca_path / 'lib' / 'decks.vimrc'
tags_path = vinca_path / 'data' / 'tags.txt'


def study(args):
	queue = []
	for deck in args.decks:
		queue += browser.filter(col, deck=deck, due_date_end=study_day)
	for card in args.cards:
		queue.append(card)
	if not args.decks and not args.cards:
		queue = browser.filter(col, due_date_end=study_day)
	done_queue = []
	while queue:
		card = queue.pop()
		cont = card.review()
		if cont == -1:
			card.undo_history()
			queue.append(card)
			if not done_queue:
				break
			prev_card = done_queue.pop()
			prev_card.undo_history()
			queue.append(prev_card)
		if cont == 0:
			card.undo_history()
			break
		if cont == 1:
			card.schedule()

def linear_add(args):
	new_card = classes.Card(create=True)
	new_card.make_config('linear','linear','base')

	tags_create = [tag for deck in args.decks for tag in deck.tags_create]
	for tag in tags_create:
		new_card.add_tag(tag)
	
	# TODO: timer
	new_card.edit('a')
	new_card.add_history(today, 0, 0)
	new_card.schedule()
	
def one_liner(args):
	tags_create = []
	for deck in args.decks:
		tags_create += deck.tags_create 
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	for tag in tags_create:
		new_card.add_tag(tag)
	# BAD: this reading should be implemented elsewhere
	(new_card.path/'front').write_text(input('Q:   '))
	(new_card.path/'back').write_text(input('A:   '))
	new_card.add_history(today, 0, 0)
	new_card.schedule()
def add_basic(args):
	tags_create = []
	for deck in args.decks:
		tags_create += deck.tags_create 
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	for tag in tags_create:
		new_card.add_tag(tag)
	new_card.edit(mode='a')  # add mode
	cont = new_card.review(mode='preview')
	return new_card, cont
def add(args):
	new_card, cont = add_basic(args)
	new_card.schedule()
def add_many(args): #TODO
	 prev_card = None
	 while True:	
		 new_card, cont = add_basic(args)
		 new_card.schedule()
		 if cont == -1:
			 prev_card.review(mode='preview')  # TODO does not support multilevel
			 prev_card.undo_history()  # we do not actually want to change the old card
		 if cont == 0:
			 break
		 if cont == 1:
			 prev_card = new_card
def image_cloze(args):
	pass
def statistics(args):
	for deck in args.decks:
		all_cards = browser.filter(col, deck=deck)
		due_cards = browser.filter(all_cards, due_date_end=study_day)
		print('\n' + deck.name)
		print(f'{len(all_cards)} total')
		print(f'{len(due_cards)} due today')
	for card in args.cards:
		print(f'\nCard #{card.id}')
		print(str(card)[:50])  # TODO
		print(f'Due: {card.due_date}')
		print(f'Tags: {" ".join(card.tags)}')
		print(f'Date        Time   Grade')
		hist_lines = [f'{date} {time:5d} {grade:7d}' for date, time, grade in card.history]
		print('\n'.join(hist_lines))
	if not args.cards and not args.decks:
		due_cards = browser.filter(col, due_date_end=study_day)
		print(f'{len(col)} total')
		print(f'{len(due_cards)} due today')
def edit(args):
	if args.cards:
		for card in args.cards:
			card.edit()
		return
	vim_cmd = ['vim',decks_path] 
	vim_cmd += [f'+{args.decks[0].id + 1}'] if args.decks else []
	vim_cmd += ['-Nu',decks_vimrc]
	vim_cmd += ['-c',f'set dictionary={tags_path}']
	run(vim_cmd)
def delete(args):
	for deck in args.decks: 
		deckdict.delete(deck)
	for card in args.cards:
		if args.toggle_delete and card.deletedQ:
			card.undelete()
			continue
		card.delete()
cmd_dict = {'a':add,
	    'A':add_many,
	    'e':edit,
	    'x':delete,
	    's':study,
	    'S':statistics,
	    'l':linear_add,
	    '1':one_liner}
		
def visual_select(args, iterable):
	# allow for the selection of a card or deck
	n = len(iterable)
	sel = 0  # selected number
	print(ansi['hide_cursor'],end='')
	print('\n'*n,end='')  # move down n lines
	line_width = 50  # TODO read from terminal
	tab_width = 8
	w = line_width - tab_width
	while True:
		print(ansi['move_up_line']*n,end='') # move up n lines
		for i, item in enumerate(iterable):
			print(f"{ansi['reverse']*(i==sel)}{item.id}\t{str(item)[:w]}{ansi['reset']}")
		k = readchar.readchar()  # get key
		sel = (sel + (k=='j') - (k=='k') ) % n
		if k == 'q' or k == readchar.key.ESC:
			print(ansi['show_cursor'],end='')
			exit(0)
		if k in cmd_dict.keys():
			if type(item) is classes.Deck: args.decks = [iterable[sel]]
			if type(item) is classes.Card: args.cards = [iterable[sel]]
			cmd_dict[k](args)
			if k == 'S':
				break
			print(ansi['hide_cursor'],end='')

def query(args):
	matches = browser.search(col, args.pattern)  # list of matching cards
	for card in matches:
		if args.id_only:
			print(card.id)
			continue
		tabwidth = 8
		line_width = 50  # TODO read from terminal
		w = line_width - tabwidth
		print(f'{card.id}\t{str(card)[:w]}')
def visual_query(args):
	matches = browser.search(col, args.pattern)
	args.toggle_delete = True  # allow for the 'x' key to restore cards
	visual_select(args, matches)
def list_decks(args):
	assert deckdict, '''You have not created any decks!
		Use [e] to create a deck.
		Decks should be lines with the form:
		name +tag_to_include -tag_to_exclude =tag_to_assign_to_new_cards'''
	print(*[f'{d.id}\t{d}' for d in deckdict.list], sep='\n')
def visual_decks(args):
	assert deckdict, '''You have not created any decks!
		Use [e] to create a deck.
		Decks should be lines with the form:
		name +tag_to_include -tag_to_exclude =tag_to_assign_to_new_cards'''
	visual_select(args, deckdict.list)


def purge(args):
	for card in col:
		if card.deletedQ:
			rmtree(card.path)
# backup / export
def backup(args):
	backup_cards = []
	if not args.cards and not args.decks:
		backup_cards = col
	for card in args.cards:
		backup_cards.append(card)
	for deck in args.decks:
		backup_cards += browser.filter(col, deck=deck)

	for card in backup_cards:
		copytree(card.path, args.backup_dest / str(card.id))
	
def import_collection(args):
	rmtree(cards_path)
	copytree(args.import_path, cards_path)
