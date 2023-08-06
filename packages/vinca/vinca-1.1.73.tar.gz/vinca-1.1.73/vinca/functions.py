# TODO testing
from pathlib import Path
from shutil import copytree, rmtree
from subprocess import run
import inspect
import datetime
today = datetime.date.today()

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


def study(args, mode='review'):
	# rethink: could be this visual or very simple
	queue = []
	if not args.decks and not args.cards:
		queue = browser.query(col, due_only=True)
	for deck in args.decks:
		queue += browser.query(col, deck=deck, due_only=True)
	queue += args.cards
	done_queue = []
	while queue:
		card = queue.pop()
		cont = card.review(mode=mode)
		if cont == -1:  # go back a card
			card.undo_history()
			queue.append(card)
			if not done_queue:
				continue
			prev_card = done_queue.pop()
			prev_card.undo_history()
			queue.append(prev_card)
		if cont == 0:  # exit
			card.undo_history()
			break
		if cont == 1:  # continue
			card.schedule()
			done_queue.append(card)
def preview(args):
	study(args, mode='preview')

# generators
def linear_add(args):
	new_card = classes.Card(create=True)
	new_card.make_config('linear','linear','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
	new_card.edit('a')
	new_card.schedule()
	return new_card
def one_liner(args):
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
	front = input('Q:   ')
	back = input('A:   ')
	(new_card.path/'front').write_text(front)
	(new_card.path/'back').write_text(back)
	new_card.add_history(today, 0, 0)
	new_card.schedule()
	if args.mode == 'visual':
		front_lines = 1 + (5+len(front))//COLUMNS
		back_lines = 1 + (5+len(back))//COLUMNS
		print(ansi['move_up_line']*(front_lines + back_lines), end='')
		print(ansi['clear_to_bottom'],end='')  #TODO rethink
	return new_card
def add(args):
	new_card = classes.Card(create=True)
	new_card.make_config('base','base','base')
	new_card.add_tags([tag for deck in args.decks for tag in deck.tags_create])
	new_card.edit(mode='a')  # add mode
	# new_card.review(mode='preview')
	new_card.schedule()
	return new_card
def add_many(args): 
	add_cmds = {'a': add, 'l': linear_add, '1': one_liner}
	print(ansi['hide_cursor'],end='')
	print('Add Cards')
	print(*[f'{key}\t{cmd.__name__}' for key,cmd in add_cmds.items()],sep='\n')
	k = readchar.readchar()
	if k not in add_cmds:
		print(ansi['show_cursor'],end='')
		return
	new_card = add_cmds[k](args)
	print(ansi['move_up_line']*(1+len(add_cmds)) + ansi['clear_to_bottom'],end='')
	visual_select(args,[new_card],mode='cards')
def image_cloze(args):
	pass
def statistics(args):
	if len(args.cards) == 1:
		card = args.cards[0]
		print(f'\nCard #{card.id}')
		print(str(card)[:COLUMNS])
		print(f'Tags: {" ".join(card.tags)}')
		print(f'Due: {card.due_date}')
		print('Date\t\tTime\tGrade')
		print(*[f'{date}\t{time}\t{grade}' for date, time, grade in card.history],sep='\n',end='')
		if args.mode=='visual':
			print(ansi['move_up_line']*(5+len(card.history)), end='')
		return
	all_cards = args.cards if args.cards else browser.query(col, decks=args.decks) 
	due_cards = browser.query(all_cards, due_only=True)
	new_cards = browser.query(all_cards, new_only=True)
	print(f'Total\t{len(all_cards)}')
	print(f'Due\t{len(due_cards)}')
	print(f'New\t{len(new_cards)}')
	if args.mode=='visual':
		print(ansi['move_up_line']*3,end='')
def edit(args):
	if args.cards:
		card = args.cards[0]
		card.edit()
		# refresh the card's summary string
		card.str = card.default_str()  
		return
	# otherwise edit the decks file
	vim_cmd = ['vim',decks_path] 
	vim_cmd += [f'+{args.decks[0].id + 1}'] if args.decks else []
	vim_cmd += ['-Nu',decks_vimrc]
	vim_cmd += ['-c',f'set dictionary={tags_path}']
	run(vim_cmd)
def delete(args):
	for deck in args.decks: 
		deck.deletedQ = not deck.deletedQ
	for card in args.cards:
		if card.deletedQ: card.undelete()
		else: card.delete()

# visual selection
cmd_dict = {'a':add,
	    'A':add_many,
	    'e':edit,
	    'x':delete,
	    's':study,
	    'p':preview,
	    'S':statistics,
	    'l':linear_add,
	    '1':one_liner}
def visual_select(args, iterable, mode):
	# TODO keep the size of this function under control
	assert mode in ['decks','cards']
	# allow for the selection of a card or deck
	n = len(iterable)
	sel = 0  # selected number
	print(ansi['hide_cursor'],end='')  # TODO put hide_cursor, show_cursor in __init__ for safety and dryness
	print('\n'*n,end='')  # move down n lines
	while True:
		print(ansi['move_up_line']*n,end='') # move up n lines
		for i, item in enumerate(iterable):
			# TODO create a sane formatting system
			w = COLUMNS - TAB_WIDTH - 10*item.deletedQ  # allotted width of the card string.
			d = (ansi['red']+'[deleted]' + ansi['reset_color'] + ' ')*item.deletedQ
			print(ansi['reverse']*(i==sel),end='') 
			print(f'{item.id}\t{d}{str(item)[:w]:{w}}{ansi["reset"]}')
		k = readchar.readchar()  # get key
		sel = (sel + (k=='j') - (k=='k') ) % n

		if k == 'q' or k == readchar.key.ESC:
			print(ansi['clear_to_bottom'],end='')
			print(ansi['show_cursor'],end='')
			return
		if k in cmd_dict:
			print(ansi['clear_to_bottom'],end='')
			if mode=='decks': args.decks = [iterable[sel]]  # TODO allow decks for add_many, but do not delete them
			if mode=='cards': args.cards = [iterable[sel]]
			print(ansi['show_cursor'],end='')
			new_card = cmd_dict[k](args)
			if new_card and mode=='cards':
				iterable = [new_card] + iterable
				print('')  # print a blank newline
				n += 1
				sel = 0
			print(ansi['hide_cursor'],end='')
def list_decks(args):
	assert deckdict, 'You have no decks. Use [e] to make a deck.'
	if args.mode=='visual':
		visual_select(args, deckdict.list, mode='decks')
		deckdict.save_decks()  # i.e. make deletion permanent
		return
	print(*[f'{d.id}\t{d}' for d in deckdict.list], sep='\n')
def query(args):
	unfiltered_cards = args.cards if args.cards else col
	# get query parameters as a list of strings
	query_kwargs = inspect.getargspec(browser.query).args[1:]
	# check that args has these. (E.g. if reviewer is a parameter, check args.reviewer exists.)
	assert all([hasattr(args, param) for param in query_kwargs])
	matches = browser.query(unfiltered_cards,
		# feed the keyword args editor=args.editor, due=args.due, 
		**{param : getattr(args, param) for param in query_kwargs})
	if not matches:
		print('No matches.')
		return
	if args.mode=='visual':
		visual_select(args, matches, mode='cards')
		return
	for card in matches:
		d = (ansi['red']+'[deleted]' + ansi['reset_color'] + ' ')*card.deletedQ
		w = COLUMNS - TAB_WIDTH - 10*card.deletedQ  # allotted width of the card string.
		print(str(card.id) + ('\t' + d + str(card)[:w]) * (not args.id_only))

def purge(args):
	for card in browser.query(col, deleted_only=True):
		rmtree(card.path)
# backup / export
def backup(args):
	backup_cards = [] if args.cards or args.decks else col
	backup_cards += [c for d in args.decks for c in browser.query(col, deck=d)]
	backup_cards += args.cards

	for card in backup_cards:
		copytree(card.path, args.backup_dest / str(card.id))
def import_collection(args):
	if args.overwrite:
		rmtree(cards_path)
		copytree(args.import_path, cards_path)
		return
	for new_id,card_path in enumerate(args.import_path.iterdir(), start=max(col.id_list) + 1):
		copytree(card_path, cards_path / str(new_id))
