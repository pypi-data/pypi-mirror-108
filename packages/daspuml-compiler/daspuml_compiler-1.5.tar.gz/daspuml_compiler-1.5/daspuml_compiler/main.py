import argparse
import logging
import os
import sys

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from plantuml import PlantUML

if __name__ is not None and "." in __name__:
    from .DaspumlLexer import DaspumlLexer
    from .DaspumlParser import DaspumlParser
    from .LogicalListener import LogicalListener
    from .IndexingListener import IndexingListener
    from .Register import Register
else:
    from DaspumlLexer import DaspumlLexer
    from DaspumlParser import DaspumlParser
    from LogicalListener import LogicalListener
    from IndexingListener import IndexingListener
    from Register import Register


class MyErrorListener(ErrorListener):
    def __init__(self):
        super(MyErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxError("Syntax error")


def generate_output(outfile, outdir):
    if outfile is None:
        outfile = "result.png"
    if outdir is None:
        outdir = ""
    server = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    server.processes_file(filename="output.txt", outfile=outfile, directory=outdir)


def compile_daspuml(input_file, outfile, outdir, remove_output_file, is_verbose=False):
    if is_verbose:
        sys.tracebacklimit = 0
    logging.basicConfig(level=logging.DEBUG)
    input_source_code = FileStream(input_file, encoding="utf-8")
    lexer = DaspumlLexer(input_source_code)
    if is_verbose:
        lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = DaspumlParser(stream)
    if is_verbose:
        parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())

    tree = parser.start()
    register = Register()
    walker = ParseTreeWalker()

    uml = IndexingListener(register)
    walker.walk(uml, tree)

    uml = LogicalListener(register)
    walker.walk(uml, tree)

    generate_output(outfile, outdir)
    if remove_output_file and os.path.isfile("output.txt"):
        os.remove('output.txt')
    return register


def main(remove_output_file=True):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='a name of file with source code with daspUML')
    parser.add_argument('-d', '--output_dir', help='a name of output directory')
    parser.add_argument('-o', '--output', help='a name of output png file')
    parser.add_argument('-v', '--verbose', action='store_true', help='a name of output png file')
    args = parser.parse_args()

    if not args.verbose:
        compile_daspuml(args.input_file, args.output, args.output_dir, remove_output_file=remove_output_file, is_verbose=True)
    else:
        compile_daspuml(args.input_file, args.output, args.output_dir, remove_output_file=remove_output_file)


if __name__ == '__main__':
    main()
