from vinca import parsing, functions
from vinca.lib.classes import Card, Deck

# parse the command line arguments
parser = parsing.parser
args = parser.parse_args()
for e in args.decks_or_cards:
	if type(e) is Card:
		args.cards.append(e)
	if type(e) is Deck:
		args.decks.append(e)	

# run the specified function
func = args.func
func = getattr(functions, func)
func(args)
