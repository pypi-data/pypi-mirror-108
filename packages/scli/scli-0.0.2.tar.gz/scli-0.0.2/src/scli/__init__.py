import time

print("Mind that developer is still breaking is keyboard to get me ready!!")

def timer(func):
	def inner(*args, **kwargs):
		start_ts = time.time()
		func(*args, **kwargs)
		end_ts = time.time()
		print(f"Time taken to execute {func.__name__} : {end_ts - start_ts:.2f} seconds")
	return inner

