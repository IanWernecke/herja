# herja
=======

## A repository of python code for quality of life purposes.

Packages:
* herja.logging
* herja.settings

Modules:
* herja.assertions
* herja.common
* herja.constants
* herja.conversions
* herja.decorators
* herja.fs
* herja.net


Common features:

The easily accessible use of this module is probably the Main decorator. This decorator automatically parses input given
on the command line and attempts to parse it according to a simple argument parser. The decorators expects \*args to
represent a tuple of (list, dictionary) type that can be applied as \*args and \*\*kwargs to the standard add_argument
call on an argparse.ArgumentParser object. The result of the parsing is given to the decorated function if the
\_\_name\_\_ attribute of the area where \@Main decorates is '\_\_main\_\_'.

An example is easier than words, anyway:

> from herja.decorators import Main
> @Main(
>   (['input'], dict(help='The name of the input file.')),
>   (['output'], dict(help='The name of the output file.'))
> )
> def main(args):
>   print(args)
>   # example invocation:
>   #   python thisfile.py my_input.txt my_output.pdf
>   # creates:
>   #   Namespace(input='my_input.txt', output='my_output.pdf')
>   return 0
