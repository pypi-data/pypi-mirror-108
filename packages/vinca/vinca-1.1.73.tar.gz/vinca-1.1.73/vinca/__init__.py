from vinca import parsing, functions
from vinca.lib.classes import Card, Deck
import sys

def main():
	# parse the command line arguments
	parser = parsing.parser
	args = parser.parse_args()
	# sort decks_or_cards appropriately
	for e in args.decks_or_cards:
		if type(e) is Card:
			args.cards.append(e)
		if type(e) is Deck:
			args.decks.append(e)	
	# accept a file of newline separated card ids
	if not sys.stdin.isatty():
		for line in sys.stdin:
			id = line.strip().split()[0]  # first field
			assert id.isdigit(), f'Bad card id {id}'
			args.cards.append(Card(id))
		# reconnect stdin to tty in case we used a pipe
		sys.stdin = open('/dev/tty')  
		
	# run the specified function
	func = args.func
	func = getattr(functions, func)
	func(args)

if __name__=='__main__':
	main()
