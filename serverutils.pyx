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
	except (OverflowError, MemoryError):
		return {'error': 'value too large to process'}
	except:
		return {'error': 'invalid request'}
	return result


def palindrome(message):
	message = ''.join(message.split())
	half_len = len(message) / 2.0
	for i, character in enumerate(message, 1):
		if i >= half_len + 1:
			break
		if character != message[-i]:
			return False
	return True

cdef long min_factor(long num):
	cdef long i = 0
	for i in range(2, num + 1):
		if num % i == 0:
			return i
	return num


def factor(long number):
	result = []
	cdef long total = 1
	cdef long cur_num = number
	cdef long min_number
	while total != number:
		min_num = min_factor(cur_num)
		result.append(min_num)
		total *= min_num
		cur_num = cur_num / min_num
	return result


def fib(int n):
	cdef int n1 = 0
	cdef int n2 = 0
	cdef int total = 0
	for i in range(1, n + 1):
		n2 = i
		total = total + n1 + n2
		n1 = i
	return total

