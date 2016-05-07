def process_request(request):
	process_table = {
		'factor': factor,
		'palindrome': palindrome,
		'fibonacci': fib
	}
	func, data = request.items()[0]
	try:
		result = process_table[func](data)
	except KeyError:
		return {'error': 'invalid request'}
	return result


def palindrome(message):
	message = ''.join(message.split())
	half_len = len(message) / 2.0
	for i, char in enumerate(message, 1):
		if i >= half_len + 1:
			break
		if char != message[-i]:
			return False
	return True


def factor(number):
	for i in range(2, number + 1):
		if number % i == 0:
			fact = number / i
			return [i] + factor(fact)
	return []


def fib(n):
	total = 0
	n1 = 0
	n2 = 0
	for i in range(1, n + 1):
		n2 = i
		total += n1 + n2
		n1 = i
	return total
