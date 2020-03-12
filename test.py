from herja.decorators import Main
@Main(
    (['input'], dict(help='The name of the input file.')),
    (['output'], dict(help='The name of the output file.')),
)
def main(args):
    print(args)
    return 0

