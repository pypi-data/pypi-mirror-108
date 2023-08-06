# The metareviewer which implements specific reviewers
import datetime
today = datetime.date.today()
import importlib
	
grade_dict = {'x': -1,
	      'q': 0,
	      'u': 0,
	      'h': 0,
	      '1': 1,
	      '2': 2,
	      '3': 3,
	      '4': 4,
	      ' ': 3,
	      '\r': 3,
	      '\n': 3}
cont_dict = {'x': 1,
	     'q': 0,
	     'u': -1,
	     'h': -1,
	     '1': 1,
	     '2': 1,
	     '3': 1,
	     '4': 1,
	     ' ': 1,
	     '\r': 1,
	     '\n': 1}
assert cont_dict.keys() == grade_dict.keys()

def review(card, mode='review'):
	assert mode in ['review','preview']

	start = datetime.datetime.now()  # begin card timer

	# dynamically import the required reviewer module
	# a specifc reviewer is responsible for returning a key to the generic reviewer
	m = importlib.import_module('.'+card.reviewer, package = 'vinca.reviewers')
	key = m.review(card, mode)  # the reviewer gives back the key

	stop = datetime.datetime.now()
	elapsed_time = min(120, (stop - start).seconds)

	if key in ['e','f','b','t','*']:
		card.edit(mode = key)
		return card.review(mode = 'preview')
	elif key in grade_dict.keys():
		cont = cont_dict[key]
		grade = grade_dict[key] 
		grade = grade if mode=='review' or grade<0 else 0
	else:
		raise ValueError(f'The key you pressed is not valid. Try {grade_dict.keys()}')
	card.add_history(today, elapsed_time, grade)
	return cont

def default_str(card):
	m = importlib.import_module('.'+card.reviewer, package = 'vinca.reviewers')
	assert hasattr(m, 'default_str'), f'{card.reviewer} must implement \
		the default_str method to represent this card on the command line'
	return m.default_str(card)
