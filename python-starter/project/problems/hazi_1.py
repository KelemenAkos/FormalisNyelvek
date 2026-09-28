from project.problem import Problem

class DFA(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--check', help='A vizsgálandó szó vagy szavak')

    def is_chosen_problem(self, args):
        return args.check is not None

    def run(self, args):
        with open(args.input, 'r') as file:
            lines = file.readlines()

        states = lines[0].strip().split()
        alphabet = lines[1].strip().split()
        start_state = lines[2].strip()
        final_states = lines[3].strip().split()

        transitions = {}

        for line in lines[4:]:
            parts = line.strip().split()

            from_state = parts[0]
            symbol = parts[1]
            to_state = parts[2]

            transitions[(from_state, symbol)] = to_state

        words = args.check.split(',')

        results = []

        for word in words:

            current_state = start_state

            for symbol in word:
                current_state = transitions[(current_state, symbol)]

            if current_state in final_states:
                results.append("IGEN")
            else:
                results.append("NEM")

        with open(args.output, 'w') as file:
            for result in results:
                file.write(result + '\n')