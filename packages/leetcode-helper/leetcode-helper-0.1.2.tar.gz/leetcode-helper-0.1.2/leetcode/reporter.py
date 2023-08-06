import prettytable as pt
import time
import traceback
from threading import Timer
 
def time_limit(interval):
    # From: https://blog.csdn.net/Homewm/article/details/92127567
    def wraps(func):
        def time_out():
            raise TimeoutError()
 
        def deco(*args, **kwargs):
            timer = Timer(interval, time_out)
            timer.start()
            res = func(*args, **kwargs)
            timer.cancel()
            return res
        return deco
    return wraps


# https://gist.github.com/vratiu/9780109
class Color:
    @classmethod
    def red(cls, obj):
        return '\033[0;31m{}\033[0m'.format(obj)
    
    @classmethod
    def green(cls, obj):
        return '\033[0;32m{}\033[0m'.format(obj)
    
    @classmethod
    def default(cls, obj):
        return '{}'.format(obj)

    @classmethod
    def color(cls, obj, color=None):
        def __single(obj, color=None):
            if color.startswith('r'):
                return cls.red(obj)
            elif color.startswith('g'):
                return cls.green(obj)
            else:
                return cls.default(obj)
        
        if isinstance(obj, list):
            for i in range(len(obj)):
                obj[i] = __single(obj[i], color)
        else:
            obj = __single(obj, color)

        return obj

    
def testPass(true_output, expect_output, testPassMethod=None):
    if testPassMethod: 
        return testPassMethod(true_output, expect_output)
    return true_output == expect_output

def do_test(method, *test_input, timeout=5):
    @time_limit(timeout)
    def _do_test(method, *test_input):
        return method(*test_input)
    
    return _do_test(method, *test_input)


def report(method, testcases, expect=False, verbose=True):
    tb = pt.PrettyTable()

    if expect:
        tb.field_names = ['Status', 'Time', 'Output', 'Expect', 'Test Case']
    else:
        tb.field_names = ['Status', 'Time', 'Output', 'Test Case']

    pass_count = 0

    for test in testcases:
        row = tb.field_names.copy()
        expect_output = test[0]
        test_input = test[1]

        
        # Cols
        if expect:
            row[3] = expect_output
            row[4] = test_input
        else:
            row[3] = test_input

        try:
            starttime = time.time()
            # true_output = do_test(method, *test_input) #method(*test_input)
            true_output = method(*test_input)
            passtime = time.time() - starttime
            row[1] = "{:.7f}s".format(passtime)
            row[2] = true_output

            if len(str(test_input)) > 120:
                test_input = str(test_input)[:120] + '...'

            if testPass(true_output, expect_output):
                pass_count += 1
                row[0] = "√ PASS "
                row = Color.color(row, "green")
                if verbose:
                    tb.add_row(row)
            else:
                row[0] = "X WRONG"
                # row = Color.color(row, "red")
                tb.add_row(row)
        
        except TimeoutError as e:
            row[0] = "! TLE"
            row[1] = row[2] = "nil"
            row = Color.color(row, "red")
            tb.add_row(row)

        except Exception as e:      
            row[0] = "! ERROR"
            row[1] = row[2] = "nil"
            row = Color.color(row, "red")
            tb.add_row(row)

            print("Program error on testcase {}".format(test))
            print(traceback.format_exc())

    print(tb)
    print('Total {}, pass {}, fail {}'.format(len(testcases), pass_count, len(testcases) - pass_count))