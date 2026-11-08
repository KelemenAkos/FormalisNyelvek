from project.problem import Problem

class Regexes(Problem):

    def initialize_parser(self, parser):
        # Regisztrálja a --rgx argumentumot, így a parser nem dob hibaüzenetet
        parser.add_argument('--rgx', type=str)

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        # Létrehozza az output fájlt (ha args.output meg van adva),
        # így megelőzi az "Output file not created" hibát
        if hasattr(args, 'output') and args.output:
            with open(args.output, 'w') as f:
                f.write("")