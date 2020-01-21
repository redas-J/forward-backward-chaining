class Rule:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 = False

    def follows(self, facts):

        for fact in self.left:
            if fact not in facts:
                return fact
        return None

    def __str__(self):
        return ",".join(self.left) + "->" + self.right


class ForwardChaining:

    def __init__(self, file_name):
        self.iteration = 0
        self.output = ""
        self.output_file_name = None

        self.output += "PART 1. Data\n"
        rules, facts, goal = self.read_data(file_name)
        self.print_data(rules, facts, goal)

        self.output += "PART 2. Execution\n"
        result, road = self.forward_chaining(rules, facts, goal)

        self.output += "PART 3. Results\n"
        self.print_results(result, road, goal)

        self.write_output(file_name)
        print("Result saved in file: %s." % self.output_file_name)

    def forward_chaining(self, rules, facts, goal):
        ir = len(facts)
        iteration = 0
        road = []

        while goal not in facts:
            rule_applied = False
            iteration += 1
            self.output += "%i".rjust(4, " ") % iteration + " ITERATION\n"

            for rule in rules:
                self.output += "    R%i:%s " % ((rules.index(rule) + 1), str(rule))

                if rule.flag1:
                    self.output += "skipping, because flag1 is raised.\n"
                    continue

                if rule.flag2:
                    self.output += "skipping, because flag2 is raised.\n"
                    continue

                if rule.right in facts:
                    self.output += "not applied, because %s is among facts. Raising flag2.\n" % rule.right
                    rule.flag2 = True
                    continue

                missing = rule.follows(facts)

                if missing is None:
                    rule_applied = True
                    rule.flag1 = True
                    facts.append(rule.right)
                    road.append("R" + str(rules.index(rule) + 1))
                    self.output += "applied. Raising flag1. Facts %s ir %s.\n" % (
                        ", ".join(facts[:ir]), ", ".join(facts[ir:]))
                    break
                else:
                    self.output += "not applied, because fact is missing: %s\n" % missing
            self.output += "\n"

            if not rule_applied:
                return False, []

        return True, road

    def read_data(self, file_name):
        rules = []
        facts = []
        goal = None

        file = open(file_name, "r")
        read_state = 0

        for line in file:
            line = line.replace("\n", "")

            if line == "":
                read_state += 1
                continue
            if line[0] == '#':
                continue

            line = line.split(" ")

            if read_state == 0:
                right = line[0]
                left = line[1:]
                rules.append(Rule(left, right))

            if read_state == 1:
                facts = line

            if read_state == 2:
                goal = line[0]

            if read_state > 2:
                self.output += "Incorrect data file."
                return [], [], None

        return rules, facts, goal

    def print_data(self, rules, facts, goal):

        self.output += "  1) Productions\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Facts %s.\n" % ", ".join(facts)
        self.output += "\n  3) Goal %s\n\n" % goal

    def print_results(self, result, road, goal):

        if result:
            if len(road) == 0:
                self.output += "  1) Goal %s among facts.\n" % goal
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Goal %s derived.\n" % goal
                self.output += "  2) Road: %s.\n" % ", ".join(road)
        else:
            self.output += "  1) Goal %s unreachable.\n" % goal

    def write_output(self, file_name):
        self.output_file_name = "out/FC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)
