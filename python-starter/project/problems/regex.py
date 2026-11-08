from project.problem import Problem

class Regexes(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--rgx', type=str)

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        pass