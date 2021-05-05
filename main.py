import dictionary
import sys

if len(sys.argv) == 2:
    if dictionary.SPELL_CHECKER.check(sys.argv[1]):
        print('Sentence is correct')
    else:
        print('Sentence is NOT correct')

else:
    print('Argument line is invalid')
