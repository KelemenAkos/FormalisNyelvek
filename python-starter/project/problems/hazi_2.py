from project.problem import Problem

class determinizacio(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--det', action='store_true')

    def is_chosen_problem(self, args):
        return args.det

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

            if len(parts) != 3:
                raise ValueError("Hibas atmenet!")

            from_state = parts[0]
            symbol = parts[1]
            to_state = parts[2]

            if from_state not in states or to_state not in states:
                raise ValueError("Ismeretlen allapot!")

            if symbol not in alphabet:
                raise ValueError("Ismeretlen jel!")

            key = (from_state, symbol)

            if key not in transitions:
                transitions[key] = set()

            transitions[key].add(to_state)

        #a kezdoallapot halmazkent
        start_set = frozenset([start_state])
        new_states = [start_set]
        state_names = {start_set: 's0'}
        new_transitions = []
        i = 0

        while i < len(new_states):
            current_set = new_states[i]
            current_name = state_names[current_set]
            for symbol in sorted(alphabet):
                destination = set()

                for state in current_set:
                    key = (state, symbol)

                    if key in transitions:
                        destination.update(transitions[key])

                if len(destination) == 0:
                    continue

                destination = frozenset(destination)

                if destination not in state_names:
                    new_name = 's' + str(len(new_states))
                    state_names[destination] = new_name
                    new_states.append(destination)

                new_transitions.append((current_name, symbol, state_names[destination]))

            i += 1

        #uj vegallapotok
        new_final_states = []

        for state_set in new_states:
            if any(state in final_states for state in state_set):
                new_final_states.append(state_names[state_set])

        #atmenetek rendezese
        new_transitions.sort(key=lambda x: (x[0], x[1], x[2]))

        #kiiras
        with open(args.output, 'w') as file:
            file.write(' '.join(state_names[state] for state in new_states) + '\n')
            file.write(' '.join(sorted(alphabet)) + '\n')
            file.write('s0\n')
            file.write(' '.join(new_final_states) + '\n')

            for from_state, symbol, to_state in new_transitions:
                file.write(from_state + ' ' + symbol + ' ' + to_state + '\n')