#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentTypeError
import pickle
from sys import stderr


from markov import MarkovBuilder
from utils.imessage import get_messages_from_me
from utils.text import get_words, make_sentences


# Cache for `MarkovGenerator` seralized object
CACHE_FILE = '.markov_cache.pickle'


def positive_int(name):
    """
    Type for ArgumentParser that defines a positive integer.
    """
    def inner(value):
        try:
            value = int(value)
            assert(value > 0)
            return value

        except:
            raise ArgumentTypeError(
                "{} must be a positive integer".format(name))

    return inner


description = 'Imitate you by using Markov chains trained on your iMessages'
arg_parser = ArgumentParser(description=description)

arg_parser.add_argument('--order', type=positive_int('order'),
                        default=2, help='The order of Markov chain to use')

arg_parser.add_argument('--number', type=positive_int('number'),
                        default=1, help='The number of imitations to output')

arg_parser.add_argument('--words', type=positive_int('words'),
                        default=100,
                        help='The approx number of words per imitation')

arg_parser.add_argument('--no-chain-cache', dest='cache',
                        action='store_false',
                        help='Don\'t cache the Markov chain generator')

arg_parser.set_defaults(cache=True)

args = arg_parser.parse_args()


def imitate(generator, num_words):
    """
    Imitate a person given their iMessage Markov chain and a desired word
    length.
    """
    return make_sentences(generator.generate(num_words)) + '\n'


if __name__ == '__main__':
    cache = {}

    try:
        with open(CACHE_FILE, 'r') as f:
            cache = pickle.load(f)

    except:
        pass

    # Attempt to use the cache if available
    try:
        gen = cache[args.order]

    except KeyError:
        # Generate a chain if a cached one for a given order doesn't exist
        markov = MarkovBuilder(order=args.order)

        for message in get_messages_from_me():
            markov.train(get_words(message))

        gen = markov.build()

        if args.cache:
            cache[args.order] = gen

            try:
                with open(CACHE_FILE, 'w') as f:
                    pickle.dump(cache, f, protocol=2)

            except IOError:
                sys.stderr.write('ERROR: Could not write cache file\n')

    sep = '\n' + ''.join(['-'] * 40) + '\n\n'

    print(sep.join(imitate(gen, args.words) for _ in range(args.number)))
