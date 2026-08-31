"""anoieu-fuzz -- a fuzzer for Eunoia-based proof checkers.

anoieu reads a signature and says what is wrong with it. anoieu-fuzz does the
opposite: it writes signatures and proofs nobody would write, hands them to a
checker, and watches for the answer a checker should never give.

It is deliberately ignorant. It does not know what a proof means, whether a
rule is sound, or what CPC is for; it knows the *shape* of the languages and
the *interface* of a checker. Everything it reports is therefore a fact about
two runs rather than about mathematics:

- two checkers disagree about the same file (`ethos` accepts, `logos` refuses);
- one checker dies without saying why -- a signal, or no diagnostic at all;
- one checker never answers.

That is the whole oracle, and it is why the fuzzer needs no semantics.
"""

__version__ = "0.1.0"
