import math
import hashlib
from uuid import uuid4
from bitarray import bitarray


class BloomFilter:
    _fp_prob: float
    _length_of_bit_array: int
    _bit_array: bitarray
    _number_of_hash_functions: int
    _salts: list[str]

    def __init__(self, number_of_items: int, fp_prob: float):
        """
        Args:
            number_of_items (int): Number of items expected to be stored in bloom filter
            fp_prob (float): False Positive probability in decimal [0, 1]
        """

        self._fp_prob = fp_prob
        self._length_of_bit_array = self.get_length_of_bit_array(
            number_of_items, fp_prob
        )
        self._number_of_hash_functions = self.get_number_of_hash_functions(
            self._length_of_bit_array, number_of_items
        )
        self._salts = [str(uuid4()) for _ in range(self._number_of_hash_functions)]
        self._bit_array = bitarray(self._length_of_bit_array)
        self._bit_array.setall(0)  # Initialize all bits as 0 / False

        print(f"Length of bit array: {self._length_of_bit_array}")
        print(f"False positive probability: {self._fp_prob}")
        print(f"Number of hash functions: {self._number_of_hash_functions}")

    def add(self, item: str) -> None:
        """Add an item in the bloom filter

        Args:
            item (str): an item will be added to the bloom filter
        """
        digests = []
        for i in range(self._number_of_hash_functions):
            item_with_salt = self._salts[i] + item
            hex_digest = hashlib.sha256(item_with_salt.encode("utf-8")).hexdigest()
            digest = int(hex_digest, 16) % self._length_of_bit_array
            digests.append(digest)

        self._bit_array[digests] = True

    def check(self, item: str) -> bool:
        """Check an item is exist in the bloom filter

        Args:
            item (str): an item will be checked to the bloom filter

        Returns:
            bool
        """

        for i in range(self._number_of_hash_functions):
            item_with_salt = self._salts[i] + item
            hex_digest = hashlib.sha256(item_with_salt.encode("utf-8")).hexdigest()
            digest = int(hex_digest, 16) % self._length_of_bit_array

            # If any of bit is False, item not present in filter
            if self._bit_array[digest] is False:
                return False
            # Else there is might that it exist

        return True

    @classmethod
    def get_length_of_bit_array(self, number_of_items: int, fp_prob: float) -> int:
        """Calculate the length of bit array to used using following formula
        length_of_bit_array = -(items_count * lg(fp_prob)) / (lg(2)^2)

        Args:
            number_of_items (int): Number of items expected to be stored in bloom filter
            fp_prob (float): False Positive probability in decimal [0, 1]

        Returns:
            int: Length of bit array
        """

        length_of_bit_array = -(number_of_items * math.log(fp_prob)) / (
            math.log(2) ** 2
        )

        return int(length_of_bit_array)

    @classmethod
    def get_number_of_hash_functions(
        self,
        number_of_items: int,
        length_of_bit_array: int,
    ) -> int:
        """Calculate number of hash functions to be used using following formula
        number_of_hash_functions = (length_of_bit_array/number_of_items) * lg(2)

        Args:
            length_of_bit_array (int): Length of bit array
            number_of_items (int): Number of items expected to be stored in bloom filter

        Returns:
            int: Number of hash functions
        """

        number_of_hash_functions = (length_of_bit_array / number_of_items) * math.log(2)

        return int(number_of_hash_functions)
