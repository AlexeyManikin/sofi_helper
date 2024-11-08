__author__ = 'Alexey Y Manikin'

import classes.telegram
import traceback

if __name__ == '__main__':
    try:
        classes.telegram.run()
    except Exception as e:
        print((traceback.format_exc()))