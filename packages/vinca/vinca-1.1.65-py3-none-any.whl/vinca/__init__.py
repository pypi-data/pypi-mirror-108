from vinca import parsing, functions
from vinca.lib.classes import Card, Deck
import sys

# parse the command line arguments
parser = parsing.parser
args = parser.parse_args()
# sort decks_or_cards appropriately
for e in args.decks_or_cards:
	if type(e) is Card:
		args.cards.append(e)
	if type(e) is Deck:
		args.decks.append(e)	
# accept a file of newline separated cards
if not sys.stdin.isatty():
	for line in sys.stdin:
		id = line.strip()
		assert id.isdigit(), f'Bad card id {id}'
		args.cards.append(Card(id))
	
# run the specified function
func = args.func
func = getattr(functions, func)
func(args)
