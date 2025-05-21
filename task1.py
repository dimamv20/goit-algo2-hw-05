import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item):
        result = []
        for i in range(self.num_hashes):
            hash_result = int(hashlib.md5((item + str(i)).encode()).hexdigest(), 16)
            result.append(hash_result % self.size)
        return result

    def add(self, item):
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def __contains__(self, item):
        return all(self.bit_array[i] for i in self._hashes(item))
