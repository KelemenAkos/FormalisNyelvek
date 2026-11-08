from project.problem import Problem

class minimalizalas(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--mini', action='store_true')

    def is_chosen_problem(self, args):
        return args.mini

    def run(self, args):
        with open(args.input, 'r') as file:
            lines = file.readlines()

        states = lines[0].strip().split()
        alphabet = lines[1].strip().split()
        start_state = lines[2].strip()
        final_states = lines[3].strip().split()

        transitions = {}

        #atmenetek beolvasasa es ellenorzese
        for line in lines[4:]:
            parts = line.strip().split()

            if len(parts) == 0:
                continue

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

            if key in transitions and transitions[key] != to_state:
                raise ValueError("Nem determinisztikus automata!")

            transitions[key] = to_state

        if start_state not in states:
            raise ValueError("Ismeretlen kezdoallapot!")

        for state in final_states:
            if state not in states:
                raise ValueError("Ismeretlen vegallapot!")

        #elerheto allapotok meghatarozasa
        reachable = [start_state]
        i = 0

        while i < len(reachable):
            current_state = reachable[i]

            for symbol in alphabet:
                key = (current_state, symbol)

                if key in transitions:
                    destination = transitions[key]

                    if destination not in reachable:
                        reachable.append(destination)

            i += 1

        active_states = []

        for state in states:
            if state in reachable:
                active_states.append(state)

        #piramis letrehozasa
        n = len(active_states)

        marked = []

        for i in range(n):
            row = []

            for j in range(n):
                row.append(False)

            marked.append(row)

        #vegallapot es nem vegallapot
        for i in range(n):
            for j in range(i + 1, n):

                if (active_states[i] in final_states and
                    active_states[j] not in final_states):

                    marked[i][j] = True
                    marked[j][i] = True

                elif (active_states[i] not in final_states and
                      active_states[j] in final_states):

                    marked[i][j] = True
                    marked[j][i] = True

        #allapotparok vizsgalata
        changed = True

        while changed:
            changed = False

            for i in range(n):
                for j in range(i + 1, n):

                    if marked[i][j]:
                        continue

                    for symbol in alphabet:
                        key1 = (active_states[i], symbol)
                        key2 = (active_states[j], symbol)

                        #ha mindket atmenet hianyzik
                        if key1 not in transitions and key2 not in transitions:
                            continue

                        #ha csak az egyik atmenet letezik
                        if key1 not in transitions or key2 not in transitions:
                            marked[i][j] = True
                            marked[j][i] = True
                            changed = True
                            break

                        #celallapotok indexei
                        dest1 = active_states.index(transitions[key1])
                        dest2 = active_states.index(transitions[key2])

                        #ha a celallapotpar mar meg van jelolve
                        if marked[dest1][dest2]:
                            marked[i][j] = True
                            marked[j][i] = True
                            changed = True
                            break

        #osszevonhato allapotok csoportositasa
        groups = []

        for i in range(n):
            found = False

            for group in groups:
                can_join = True

                for j in group:
                    if marked[i][j]:
                        can_join = False
                        break

                if can_join:
                    group.append(i)
                    found = True
                    break

            if not found:
                groups.append([i])

        #uj allapotnevek letrehozasa
        state_names = {}
        new_states = []

        for group in groups:
            smallest = active_states[group[0]]
            new_name = 's' + smallest[1:]

            new_states.append(new_name)

            for index in group:
                state_names[active_states[index]] = new_name

        #uj kezdoallapot
        new_start_state = state_names[start_state]

        #uj vegallapotok
        new_final_states = []

        for group in groups:
            for index in group:
                state = active_states[index]

                if state in final_states:
                    new_final_states.append(state_names[state])
                    break

        #uj atmenetek
        new_transitions = set()

        for group in groups:
            representative = active_states[group[0]]
            from_name = state_names[representative]

            for symbol in alphabet:
                key = (representative, symbol)

                if key in transitions:
                    destination = transitions[key]
                    to_name = state_names[destination]

                    new_transitions.add((from_name, symbol, to_name))

        #atmenetek rendezese
        new_transitions = sorted(
            new_transitions,
            key=lambda x: (
                new_states.index(x[0]),
                sorted(alphabet).index(x[1]),
                new_states.index(x[2])
            )
        )

        #kiiras
        with open(args.output, 'w') as file:
            file.write(' '.join(new_states) + '\n')
            file.write(' '.join(sorted(alphabet)) + '\n')
            file.write(new_start_state + '\n')
            file.write(' '.join(new_final_states) + '\n')

            for from_state, symbol, to_state in new_transitions:
                file.write(from_state + ' ' + symbol + ' ' + to_state + '\n')
