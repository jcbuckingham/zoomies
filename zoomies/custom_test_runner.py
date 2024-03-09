from colorama import init, Fore, Style
from django.test.runner import DiscoverRunner

class ColoredTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        init()  # Initialize colorama

        # Print colorized test output
        print(Fore.BLUE + 'Running tests...' + Style.RESET_ALL)

        # Call the original run_tests method
        result = super().run_tests(test_labels, extra_tests, **kwargs)

        # Print colorized test result summary
        if result > 0:
            print(Fore.RED + f"{result} test(s) failed." + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'All tests passed!' + Style.RESET_ALL)

        return result

