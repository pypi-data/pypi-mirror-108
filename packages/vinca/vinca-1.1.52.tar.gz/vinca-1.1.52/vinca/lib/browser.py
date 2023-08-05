# A basic browser
# we are not trying to optimize anything
# a very easy way to speed up deck queues and statistics
# would be to provide the browser a sorted collection of cards
# the search could stop after due_date_end
import re

def filter(cards,
	   tags_include=None, tags_exclude=None, deck=None,
	   create_date_start=None, create_date_end=None,
	   seen_date_start=None, seen_date_end=None,
	   due_date_start=None, due_date_end=None,
	   last_difficulty=None,
	   editor=None,
	   reviewer=None,
	   scheduler=None,
	   deleted=False,
	   suspended=False,
	   new_only=False,
	   review_only=False):
	
	# initializing a parameter to [] will cause bugs
	tags_include = tags_include if tags_include else []
	tags_exclude = tags_exclude if tags_exclude else []

	matches = []

	for card in cards:
		if deck:
			tags_include += deck.tags_include
			tags_exclude += deck.tags_exclude
		if tags_include and not any([t in tags_include for t in card.tags]):
			continue
		if tags_exclude and any([t in tags_exclude for t in card.tags]):
			continue
		if create_date_start and card.create_date < create_date_start:
			continue
		if create_date_end and card.create_date > create_date_start:
			continue
		if seen_date_start and card.seen_date < seen_date_start:
			continue
		if seen_date_end and card.seen_date > seen_date_start:
			continue
		if card.suspendedQ or card.deletedQ:
			continue
		if due_date_start and card.due_date < due_date_start:
			continue
		if due_date_end and card.due_date > due_date_end:
			continue
		
		if editor and card.editor != editor:
			continue
		if reviewer and card.reviewer != reviewer:
			continue
		if scheduler and card.scheduler != scheduler:
			continue

		if new_only and not card.newQ:
			continue
		if review_only and card.newQ:
			continue
		# TODO: pattern matching for small files using grep

		matches.append(card)

	# print(f'matches = {matches}')
	return matches

def search(cards, pattern):
	# This lets us search our collection for a regular expression
	# TODO A fancy parameter which will highlight the matched pattern
	# (Which would be better than anki!)

	p = re.compile(pattern)
	return [c for c in cards if p.search(str(c))]
