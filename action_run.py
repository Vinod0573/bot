
import os
import sys

# insert path of this script in syspath so actions.py will be found
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

sys.argv.append('run')
sys.argv.append('actions')
arg_list = ['--actions', 'actions.actions', '--port', '5135', '-vv']
sys.argv.extend(arg_list)
print(sys.argv)

from rasa.__main__ import main
# from rasa_sdk.endpoint import app

if __name__ == "__main__":
    main()

