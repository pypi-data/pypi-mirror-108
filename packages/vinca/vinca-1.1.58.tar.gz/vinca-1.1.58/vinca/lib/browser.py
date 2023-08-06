# A basic browser
import datetime
today = datetime.date.today()
day = datetime.timedelta(days=1)
import re
from vinca.lib.ansi import ansi, AnsiStr

def filter(cards,
	   tags_include=None, tags_exclude=None, decks=None,
	   create_date_min=None, create_date_max=None,
	   seen_date_min=None, seen_date_max=None,
	   due_date_min=None, due_date_max=None,
	   due_only=False, not_due_only = False,
	   editor=None, reviewer=None, scheduler=None,
	   deleted_only=False, not_deleted_only=False,
	   new_only=False, not_new_only=False):
	
	# initializing a parameter to [] will cause bugs
	# since lists are mutable and parameters are created
	# when the function is defined (not when called)
	decks = decks if decks else []
	tags_include = tags_include if tags_include else []
	tags_exclude = tags_exclude if tags_exclude else []
	tags_include += [t for d in decks for t in d.tags_include]
	tags_exclude += [t for d in decks for t in d.tags_exclude]

	if due_only:
		due_date_max = today
	if not_due_only:
		due_date_min = today + day
		

	matches = []

	for card in cards:
		if tags_include and not any([t in tags_include for t in card.tags]):
			continue
		if tags_exclude and any([t in tags_exclude for t in card.tags]):
			continue
		if create_date_min and card.create_date < create_date_min:
			continue
		if create_date_max and card.create_date > create_date_min:
			continue
		if seen_date_min and card.seen_date < seen_date_min:
			continue
		if seen_date_max and card.seen_date > seen_date_min:
			continue
		if deleted_only and not card.deletedQ:
			continue
		if not_deleted_only and card.deletedQ:
			continue
		if due_date_min and card.due_date < due_date_min:
			continue
		if due_date_max and card.due_date > due_date_max:
			continue
		
		if editor and card.editor != editor:
			continue
		if reviewer and card.reviewer != reviewer:
			continue
		if scheduler and card.scheduler != scheduler:
			continue

		if new_only and not card.newQ:
			continue
		if not_new_only and card.newQ:
			continue

		matches.append(card)

	return matches

def search(cards, pattern, fancy=False):
	# This lets us search our collection for a regular expression
	# (Which would be better than anki!)

	p = re.compile(f'({pattern})')  # wrap in parens to create regex group \1
	matches = [c for c in cards if p.search(str(c))]
	if fancy:
		for c in matches:
			c.str = p.sub(f'{ansi["red"]}{ansi["bold"]}\\1' +
				      f'{ansi["reset_color"]}{ansi["bold_off"]}',str(c))
			c.str = AnsiStr(c)
	return matches
