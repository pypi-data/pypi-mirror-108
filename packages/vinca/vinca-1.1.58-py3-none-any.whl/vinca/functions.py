from pathlib import Path
from shutil import copytree, rmtree
from subprocess import run
import datetime
today = datetime.date.today()
study_day = today

import readchar  # 3rd party module for reading a character one at a time

from vinca.lib import classes
col = classes.collection  # TODO classes should not initialize vars
deckdict = classes.deckdict
from vinca.lib import browser
from vinca.lib.ansi import ansi
from vinca.lib.terminal import COLUMNS, LINES, TAB_WIDTH

vinca_path = Path(__file__) # /path/to/vinca/functions.py
vinca_path = vinca_path.parent # /path/to/vinca
cards_path = vinca_path / 'data' / 'cards'
decks_path = vinca_path / 'data' / 'decks.txt'
decks_vimrc = vinca_path / 'lib' / 'decks.vimrc'
tags_path = vinca_path / 'data' / 'tags.txt'


def study(args):
	queue = []
	if not args.decks and not args.cards:
		queue = browser.filter(col, due_only=True)
	for deck in args.decks:
		queue += browser.filter(col, deck=deck, due_only=True)
	queue += args.cards
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
			done_queue.append(card)

# generators
def linear_add(args):
	new_card = classes.Card(create=True)
	new_card.make_config('linear','linear','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
	new_card.edit('a')
	new_card.schedule()
def one_liner(args):
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
	# BAD: this reading should be implemented elsewhere
	(new_card.path/'front').write_text(input('Q:   '))
	(new_card.path/'back').write_text(input('A:   '))
	new_card.add_history(today, 0, 0)
	new_card.schedule()
def add_basic(args):
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
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
		all_cards = browser.filter(col, decks=[deck])
		due_cards = browser.filter(all_cards, due_only=True)
		new_cards = browser.filter(all_cards, new_only=True)
		print(f'Total\t{len(all_cards)}')
		print(f'Due\t{len(due_cards)}')
		print(f'New\t{len(new_cards)}')
	for card in args.cards:
		print(f'\nCard #{card.id}')
		print(card)
		print(f'Tags: {" ".join(card.tags)}')
		print(f'Due: {card.due_date}')
		print('Date\t\tTime\tGrade')
		print(*[f'{date}\t{time}\t{grade}' for date, time, grade in card.history],sep='\n')
	if not args.cards and not args.decks:
		due_cards = browser.filter(col, due_only=True)
		new_cards = browser.filter(col, new_only=True)
		print(f'Total\t{len(col)}')
		print(f'Due\t{len(due_cards)}')
		print(f'New\t{len(new_cards)}')
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

# visual selection
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
	w = COLUMNS - TAB_WIDTH  # desired string width
	while True:
		print(ansi['move_up_line']*n,end='') # move up n lines
		for i, item in enumerate(iterable):
			print(ansi['reverse']*(i==sel) + str(item.id) + 
				'\t' + str(item)[:w] + ansi['reset'])
		k = readchar.readchar()  # get key
		sel = (sel + (k=='j') - (k=='k') ) % n
		if k == 'q' or k == readchar.key.ESC:
			print(ansi['show_cursor'],end='')
			return
		if k in cmd_dict.keys():
			if type(item) is classes.Deck: args.decks = [iterable[sel]]
			if type(item) is classes.Card: args.cards = [iterable[sel]]
			cmd_dict[k](args)
			if k == 'S':
				break
			print(ansi['hide_cursor'],end='')

def list_decks(args):
	assert deckdict, 'You have no decks! Use [e] to make a deck.'
	print(*[f'{d.id}\t{d}' for d in deckdict.list], sep='\n')
def visual_decks(args):
	assert deckdict, 'You have no decks! Use [e] to make a deck.'
	visual_select(args, deckdict.list)
def query(args):
	matches = browser.search(col, args.pattern, fancy=True)  # list of matching cards
	if not matches:
		print('No matches.')
		return
	w = COLUMNS - TAB_WIDTH  # desired string width
	for card in matches:
		print(str(card.id) + ('\t' + str(card)[:w]) * (not args.id_only))
		
def visual_query(args):
	matches = browser.search(col, args.pattern, fancy=True)
	if not matches:
		print('No matches.')
		return
	args.toggle_delete = True  # allow for the 'x' key to restore cards
	visual_select(args, matches)
def filter(args):
	print(args)

def purge(args):
	for card in browser.filter(col, deleted_only=True):
		rmtree(card.path)
# backup / export
def backup(args):
	backup_cards = [] if args.cards or args.decks else col
	backup_cards += [c for d in args.decks for c in browser.filter(col, deck=d)]
	backup_cards += args.cards

	for card in backup_cards:
		copytree(card.path, args.backup_dest / str(card.id))
def import_collection(args):
	# TODO implement a hash comparison to prevent card duplication
	if args.overwrite:
		rmtree(cards_path)
		copytree(args.import_path, cards_path)
		return
	for new_id,card_path in enumerate(args.import_path.iterdir(), start=max(col.id_list) + 1):
		copytree(card_path, cards_path / str(new_id))
