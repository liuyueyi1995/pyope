import numpy.random as numpy_random
from pyope.errors import NotEnoughCoinsError, InvalidCoinError


def sample_hgd(in_range, out_range, nsample, seed_coins):
    """Get a sample from the hypergeometric distribution, using the provided bit list as a source of randomness"""
    numpy_random.seed(seed_coins)
    in_size = in_range.size()
    out_size = out_range.size()
    assert in_size > 0 and out_size > 0
    assert in_size <= out_size
    assert out_range.contains(nsample)

    # 1-based index of nsample in out_range
    nsample_index = nsample - out_range.start + 1
    if in_size == out_size:
        # Input and output domains have equal size
        return in_range.start + nsample_index - 1

    in_sample_num = numpy_random.hypergeometric(in_size, out_size - in_size, nsample_index)
    if in_sample_num == 0:
        return in_range.start
    elif in_sample_num == in_size:
        return in_range.end
    else:
        in_sample = in_range.start + in_sample_num
        assert in_range.contains(in_sample)
        return in_sample


def sample_uniform(in_range, seed_coins):
    """Uniformly select a number from the range using the bit list as a source of randomness"""
    cur_range = in_range.copy()
    assert cur_range.size() != 0
    # Sentinel value
    seed_coins.append(None)
    bit_iterator = iter(seed_coins)
    while cur_range.size() > 1:
        mid = int((cur_range.start + cur_range.end) / 2)
        bit = next(bit_iterator)
        if bit == 0:
            cur_range.end = mid
        elif bit == 1:
            cur_range.start = mid + 1
        elif bit is None:
            raise NotEnoughCoinsError()
        else:
            raise InvalidCoinError()
    assert cur_range.size() == 1
    return cur_range.start
