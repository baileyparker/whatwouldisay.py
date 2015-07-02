What Would I Say?
=================

![Frank Caliendo](https://nbcpresspass.files.wordpress.com/2014/02/6lhbt.gif)

Imitation *is* the highest form of flattery!

## What?
This script uses a [variable-order Markov model](http://en.wikipedia.org/wiki/Variable-order_Markov_model) to imitate your word choice and speech patterns by training a Markov chain on your iMessage logs. It also performs some smart formatting and recognizes common patterns such as smilies. The output is somewhat comprehensible, but often has comedic glitches and grammatical errors.

## How?
Clone this repo and execute the following command:

	python whatwouldisay.py

Depending on how many messages you have saved, this process could take some time (I haven't gotten to profiling and optimizing yet)! But eventually you should see a somewhat decent imitation of you (multiple calls to this are sped up by automatic caching, see below for more details).

For a more realistic imitation, you could always have your imitation *spoken* to you:

	python whatwouldisay.py | say

(Of course this only works on OSX, but so does this script so that shouldn't be an issue.)

You can also adjust the `--order` flag (which controls the greatest order of the Markov model) for some hilarious results:

	python whatwouldisay.py --order 1  # mostly nonsense
	python whatwouldisay.py --order 2  # the default
	python whatwouldisay.py --order 4  # output is mostly logical statements
	python whatwouldisay.py --order 8  # often whole conversations will be repeated

Do be careful with memory usage, though. It grows exponentially with order due to the nature of Markov chains.

Also note that for performance the script automatically caches a model for each order in `.markov_cache.pickle`. ~~Even for a few orders, this file can grow to hundreds of megabytes in size.~~ **Updated so that cache files are now compressed and optimized to be reasonably sized.** However, you can still remove it without any averse side effects (other than slower future execution) or prevent its creation with the `--no-chain-cache` flag.

## Wait...iMessage Logs?
Yes, all of your iMessage conversations (that you haven't deleted) are stored in a [SQLite database](https://sqlite.org/) saved at `~/Library/Messages/chat.db`. By opening it up in an SQLite editor and performing some SQL-fu you can find out some fairly interesting things about your text/instant messaging habits (such as total words/characters sent, most popular words, most active conversations, profanity frequency, etc.).

## Variable-order...huh?
[Markov chains](http://en.wikipedia.org/wiki/Markov_chain) are a popular CS/math paradigm that rely on current state (and the probability of numerous past outcomes of this state) to predict future states. In their simplest form (1st order), a Markov chain is a 2D matrix mapping a single state to the next state. To generate a chain, you first choose a starting state (randomly or statistically) and then check the matrix to find the most likely outcome. You report this outcome and then check the table for the next outcome that would most likely follow the outcome you just chose.

Markov chains are well suited for constructing somewhat readable language because for the most part words in sentences depend on those before them. For example, after encountering the word "the," you will most likely find a noun. This can be learned through basic statistics by training the Markov model with lots of data.

In this script, the implementation is slightly more complicated than the description above in two ways. First, because choosing the most probable outcome would generate a lot of duplicate and predictable text, I instead chose to use a weighted random algorithm to choose predicted outcomes (next words or punctuation).

Secondly, I used a variable-order model with a sliding context for the beginning of training data. What this means is for a 3rd order model, the following input

    Java is to JavaScript what Car is to Carpet

would be transformed into the following state and outcome pairs:

    ((), 'Java')
    (('Java'), 'is')
    (('Java', 'is'), 'to')
    (('Java', 'is', 'to'), 'JavaScript')
    (('is', 'to', 'JavaScript'), 'what')
    (('to', 'JavaScript', 'what'), 'Car')
    (('JavaScript', 'what', 'Car'), 'is')
    (('what', 'Car', 'is'), 'Carpet')

This sliding context allows for us to randomly choose the first outcome by using the context `()` and from there building until we have enough outcomes to start using the true 3rd degree model.

## Options

There are several options that `whatwouldisay.py` can be run with to alter its output.

  - `--order`: The maximal order of the Markov model used (if you've never generated a model for this order before, expect a decent amount of processing time), default: `2`
  - `--number`: The number of separate imitations to ouput, default: `1`
  - `--words`: The approximate number of words to output per imitation (note this includes punctuation, so that is why this is an estimate), default: `100`
  - `--no-chain-cache`: Don't cache the model generated to the `.markov_cache.pickle` file

## Roadmap

  - **Optimize performance** (profiling & exploring multithreading/processing)
  - Remove irrelevant bits of text such as links and emails
  - Better support for special character such as quotes and parenthesis (which the model rarely chooses to close because it loses their context for lower orders)
  - No force formatting (better model the capitlization and spacing of the imitatee)
