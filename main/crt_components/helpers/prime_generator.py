class Prime_Generator:
    def __init__(self):
        self.primes = []
        self.curr = 2

    def get_next_prime(self):
        while True:
            # true if current number is not divisible by any previous prime
            if all(self.curr % p != 0 for p in self.primes):
                self.primes.append(self.curr) # append current number
                yield self.curr # return current number + save function state
            self.curr += 1 # function resumes here if yield executes

    def get_current_prime(self):
        if self.primes:
            return self.primes[-1]
        else:
            return None # if self.primes is empty
    
    def get_previous_prime(self):
        if self.primes:
            return self.primes[-2]
        else:
            return None
        