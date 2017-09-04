import sys


digit_string = sys.argv[1]
print(sum([int(num) for num in digit_string if num.isdigit()]))
