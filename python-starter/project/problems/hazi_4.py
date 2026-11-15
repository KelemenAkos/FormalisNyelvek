import re
from project.problem import Problem

class Regexes(Problem):

    def initialize_parser(self, parser):
        parser.add_argument('--rgx', type=int)

    def is_chosen_problem(self, args):
        return args.rgx is not None

    def run(self, args):
        with open(args.input, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()

        # altalanos android logcat sor minta (2-5. feladatokhoz is hasznos)
        # csoportok: 1: datum+ido, 2: PID, 3: TID, 4: szint, 5: tag, 6: message
        log_pattern = re.compile(
            r'^([0-9-]+ [0-9:.]+)\s+([0-9]+)\s+([0-9]+)\s+([IDVEFAW])\s+(.+?):\s*(.*)$'
        )

        results = []

        # 1. feladat: szamlalasok kulonbozo regexek alapjan
        if args.rgx == 1:
            patterns = [
                # 1. 10. honap 15-en jott letre
                re.compile(r'^10-15\s+'),
                # 2. 10. honap 15-en 10 ora 18 perc es 51 masodperckor jott letre
                re.compile(r'^10-15\s+10:18:51\.'),
                # 3. 51 masodperckor jott letre (mindegy a perc)
                re.compile(r'^[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:51\.'),
                # 4. lowmemorykiller taget tartalmazo sor
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+[IDVEFAW]\s+lowmemorykiller\s*:'),
                # 5. 10:18:51-kor keletkezo 221-es process id-ju sor
                re.compile(r'^[0-9-]+\s+10:18:51\.[0-9]+\s+221\s+'),
                # 6. osszes hibat tartalmazo sor (E)
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+E\s+'),
                # 7. osszes warning (W) amit a PackageManager kuld
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+W\s+PackageManager\s*:'),
                # 8. osszes ExoPlayer-es debug (D) info
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+D\s+ExoPlayer[^:]*:'),
                # 9. osszes java allomany poziciot tartalmazo hiba es warning (E/W ... .java:)
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+[EW]\s+.*\.[jJ][aA][vV][aA]:[0-9]+'),
                # 10. tartalmazza a Thread szot a message reszben (nem a tagben)
                re.compile(r'^[0-9-]+\s+[0-9:.]+\s+[0-9]+\s+[0-9]+\s+[IDVEFAW]\s+[^:]+:\s*.*\bThread\b')
            ]

            for pattern in patterns:
                count = 0
                for line in lines:
                    if pattern.search(line):
                        count += 1
                results.append(str(count))

        # 2. feladat: osszes hiba (E) szarmazasi helye (.java fajlnev)
        elif args.rgx == 2:
            java_pattern = re.compile(r'\(([A-Za-z0-9_$-]+\.java):[0-9]+\)')

            for line in lines:
                match = log_pattern.match(line)
                if match and match.group(4) == 'E':
                    message = match.group(6)
                    found_files = java_pattern.findall(message)
                    for filename in found_files:
                        results.append(filename)

        # 3. feladat: osszes kulonbozo process id elofordulasi sorrendben
        elif args.rgx == 3:
            seen_pids = set()

            for line in lines:
                match = log_pattern.match(line)
                if match:
                    pid = match.group(2)
                    if pid not in seen_pids:
                        seen_pids.add(pid)
                        results.append(pid)

        # 4. feladat: legtobb errort tartalmazo process
        elif args.rgx == 4:
            error_counts = {}
            pid_order = []

            for line in lines:
                match = log_pattern.match(line)
                if match and match.group(4) == 'E':
                    pid = match.group(2)
                    if pid not in error_counts:
                        error_counts[pid] = 0
                        pid_order.append(pid)
                    error_counts[pid] += 1

            if error_counts:
                max_pid = pid_order[0]
                max_count = error_counts[max_pid]

                for pid in pid_order:
                    if error_counts[pid] > max_count:
                        max_pid = pid
                        max_count = error_counts[pid]

                results.append(f"PID={max_pid} ({max_count} errors)")

        # 5. feladat: fo szalon tortent hibak (E) szama (PID == TID)
        elif args.rgx == 5:
            main_thread_errors = 0

            for line in lines:
                match = log_pattern.match(line)
                if match and match.group(4) == 'E':
                    pid = match.group(2)
                    tid = match.group(3)
                    if pid == tid:
                        main_thread_errors += 1

            results.append(str(main_thread_errors))

        else:
            raise ValueError("Ismeretlen feladat sorszam!")

        # kiiras
        with open(args.output, 'w', encoding='utf-8') as file:
            for res in results:
                file.write(res + '\n')