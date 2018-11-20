from bitarray import bitarray

NUM_ROWS_KEY = "number_of_rows"


class BitMatrix(object):

    """
    Manages the gets and sets of the bitmatrix to the various storage backends. 
    Does not know the concept of a kmer.
    """

    def __init__(self, storage):
        self.storage = storage
        self.number_of_rows = self.storage.get_integer(NUM_ROWS_KEY)

    @classmethod
    def create(cls, storage, rows):
        storage.set_bitarrays(range(len(rows)), rows)
        storage.set_integer(NUM_ROWS_KEY, len(rows))
        return cls(storage)

    def get_row(self, row_index):
        return self.storage.get_bitarray(row_index)

    def get_rows(self, row_indexes):
        # Takes advantage of batching in storage engine if available
        return self.storage.get_bitarrays(row_indexes)

    def set_row(self, row_index, bitarray):
        return self.storage.set_bitarray(row_index, bitarray)

    def set_rows(self, row_indexes, bitarrays):
        # Takes advantage of batching in storage engine if available
        return self.storage.set_bitarrays(row_indexes, bitarrays)

    def get_column(self, column_index):
        ## This is very slow, as we index row-wise. Need to know the number of rows, so must be done elsewhere
        return bitarray(
            "".join(
                [
                    str(int(i))
                    for i in self.storage.get_bits(
                        list(range(self.number_of_rows)),
                        [column_index] * self.number_of_rows,
                    )
                ]
            )
        )

    def get_columns(self, column_indexes):
        for column_index in column_indexes:
            yield self.get_column(column_index)

    def insert_column(self, column_index, bitarray):
        ## This is very slow, as we index row-wise
        self.storage.set_bits(
            list(range(len(bitarray))), [column_index] * len(bitarray), list(bitarray)
        )
