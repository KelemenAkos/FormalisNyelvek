from project.problem import Problem

class DFA(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--check', help='A vizsgálandó szó vagy szavak')

    def is_chosen_problem(self, args):
        return args.check is not None

    def run(self, args):
        with open(args.input, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

        states = lines[0].split()
        alphabet = lines[1].split()
        start_state = lines[2]
        final_states = lines[3].split()

        transitions = {}

        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                from_state, symbol, to_state = parts
                transitions[(from_state, symbol)] = to_state

        # Több szó kezelése (vesszővel elválasztva)
        words = args.check.split(',') if args.check else []

        results = []

        for word in words:
            current_state = start_state
            is_rejected = False

            for symbol in word:
                # Ellenőrizzük, hogy létezik-e az átmenet
                if (current_state, symbol) in transitions:
                    current_state = transitions[(current_state, symbol)]
                else:
                    # Ha nincs átmenet vagy ismeretlen a szimbólum, a szót elutasítjuk
                    is_rejected = True
                    break

            # Ha megszakadt az átmenet hiánya miatt, NEM
            if is_rejected:
                results.append("NEM")
            elif current_state in final_states:
                results.append("IGEN")
            else:
                results.append("NEM")

        with open(args.output, 'w') as file:
            for result in results:
                file.write(result + '\n')