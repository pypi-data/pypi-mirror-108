from colorama import init
import traceback
import inspect
init()

class TestFailed(Exception):
    def __init__(self, expected, got, message="Test failed."):
        self.expected = expected
        self.got = got
        self.message = message
        super().__init__(self.message)
class TestSucceeded(Exception):
    def __init__(self, extra="", message="Test succeeded"):
        self.extra = extra
        self.message = message
        super().__init__(self.message)

class PromisedValue:
    def __init__(self, actualValue):
        self.actualValue = actualValue

    # EXPECTATION CHECKS
    def toBe(self, expectedValue):
        if expectedValue == self.actualValue:
            raise TestSucceeded()
        else:
            raise TestFailed(expectedValue, self.actualValue)

    def toRaise(self, expectedError=Exception):
        if issubclass(self.actualValue, expectedError):
            raise TestSucceeded(f"error '{self.actualValue.__name__}' thrown")
        else:
            raise TestFailed(f"'{expectedError.__name__}'", f"'{self.actualValue.__name__}'")

def expect(value):
    if inspect.isfunction(value):
        try:
            return PromisedValue(value())
        except Exception as e:
            return PromisedValue(e.__class__)
    else:
        return PromisedValue(value)

def it(description, function, reply='min', parameters=[]):
    try:
        function(*parameters)
    except TestFailed as e:
        print("\033[37;1;41m"+" FAIL "+"\033[0m", end=' ')
        print("on ["+description+"]")
        if reply != 'min':
            print(f'  expected: {e.expected}')
            print(f'  received: {e.got}')
            print()
    except TestSucceeded as e:
        print("\033[37;1;42m"+" PASS "+"\033[0m", end=' ')
        print(description, end='')
        if e.extra != "":
            print(f': {e.extra}', end='')
        print()
        if reply != 'min':
            print()
    except Exception:
        print("\033[37;1;41m"+" FAIL "+"\033[0m", end=' ')
        print("on ["+description+"]")
        if reply != 'min':
            print()
        traceback.print_exc()
        if reply != 'min':
            print()

class describe:
    def __init__(self, description):
        self.description = description
        self.fails = 0
    def it(self, description, function, reply='min', parameters=[]):
        try:
            function(*parameters)
        except TestFailed as e:
            print("    ", "\033[37;1;41m"+" FAIL "+"\033[0m", end=' ')
            print("on ["+description+"]")
            if reply != 'min':
                print("    ", f'  expected: {e.expected}')
                print("    ", f'  received: {e.got}')
                print()
            self.fails += 1
        except TestSucceeded:
            print("    ", "\033[37;1;42m"+" PASS "+"\033[0m", end=' ')
            print(description)
            if reply != 'min':
                print()
        except Exception:
            print("    ", "\033[37;1;41m"+" FAIL "+"\033[0m", end=' ')
            print("on ["+description+"]")
            if reply != 'min':
                print()
            traceback.print_exc()
            if reply != 'min':
                print()
            self.fails += 1
    def verify(self):
        print()
        if self.fails == 0:
            print("\033[37;1;42m"+" TEST SUITE PASS "+"\033[0m", end=' ')
            print(self.description)
        else:
            print("\033[37;1;41m"+" TEST SUITE FAIL "+"\033[0m", end=' ')
            print("in ["+self.description+"]")
