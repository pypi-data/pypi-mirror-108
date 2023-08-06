# A basic browser
import datetime
TODAY = datetime.date.today()
DAY = datetime.timedelta(days=1)
import re
from vinca.lib.ansi import ansi, AnsiStr

def query(cards, pattern='', no_fancy=False,
	   tags_include=None, tags_exclude=None, decks=None,
	   create_date_min=None, create_date_max=None,
	   seen_date_min=None, seen_date_max=None,
	   due_date_min=None, due_date_max=None,
	   editor=None, reviewer=None, scheduler=None,
	   deleted_only=False, show_deleted=False,
	   due_only=False, not_due_only = False,
	   new_only=False, not_new_only=False,
	   invert=False):
	
	# initializing a parameter to [] will cause bugs
	# since lists are mutable and parameters are created
	# when the function is defined (not when called)
	decks = decks if decks else []
	tags_include = tags_include if tags_include else []
	tags_exclude = tags_exclude if tags_exclude else []
	tags_include += [t for d in decks for t in d.tags_include]
	tags_exclude += [t for d in decks for t in d.tags_exclude]
	# compile the regex pattern for faster searching
	p = re.compile(f'({pattern})')  # wrap in parens to create regex group \1

	matches = []
	for card in cards:
		# tags
		if tags_include and not any([t in tags_include for t in card.tags]):
			continue
		if tags_exclude and any([t in tags_exclude for t in card.tags]):
			continue
		# dates
		if create_date_min and card.create_date < create_date_min:
			continue
		if create_date_max and card.create_date > create_date_max:
			continue
		if seen_date_min and card.seen_date < seen_date_min:
			continue
		if seen_date_max and card.seen_date > seen_date_max:
			continue
		if due_date_min and card.due_date < due_date_min:
			continue
		if due_date_max and card.due_date > due_date_max:
			continue
		# config
		if editor and card.editor != editor:
			continue
		if reviewer and card.reviewer != reviewer:
			continue
		if scheduler and card.scheduler != scheduler:
			continue
		# due / new / deleted
		if due_only and card.due_date > TODAY:
			continue
		if not_due_only and card.due_date <= TODAY:
			continue
		if new_only and not card.newQ:
			continue
		if not_new_only and card.newQ:
			continue
		if deleted_only and not card.deletedQ:
			continue
		if (not show_deleted and not deleted_only) and card.deletedQ:
			continue
		# pattern matchings
		if pattern and not p.search(str(card)):
			continue

		matches.append(card)

	# post-processing
	if invert:
		matches = [c for c in cards if c not in matches]
		# try using sets if things get slow
	# sort by newest
	matches.sort(key=lambda card: card.seen_date, reverse=True)
	# color matching text in red
	if pattern and not no_fancy:
		for c in matches:
			c.str = p.sub(f'{ansi["red"]}{ansi["bold"]}\\1' +
				      f'{ansi["reset_color"]}{ansi["bold_off"]}',str(c))
			c.str = AnsiStr(c)  # AnsiStr class lets slicing ignore ansi chars
	return matches
