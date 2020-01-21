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
        return "%s->%s" % (",".join(self.left), self.right)


class BackwardChaining:
    def __init__(self, file_name):
        self.output = ""
        self.output_file_name = None
        self.iteration = 0
        self.current_goals = []
        self.found_facts = []
        self.road = []

        self.output += "PART 1. Data\n"
        self.rules, self.target_facts, self.goal = self.read_data(file_name)
        self.print_data(self.rules, self.target_facts, self.goal)

        self.output += "PART 2. Execution\n"
        result = self.do_backward_chaining(self.goal)

        self.output += "\n" + "PART 3. Results\n"
        self.print_result(result)

        self.write_output(file_name)

    def do_backward_chaining(self, goal, indent=""):

        if goal in self.target_facts:
            self.print_step(goal, indent,
                            "Fact (given), because facts %s. Returning, success." % ", ".join(self.target_facts))
            return True

        if goal in self.current_goals:
            self.print_step(goal, indent, "Cycle. Returning, FAIL")
            return False

        if goal in self.found_facts:
            self.print_step(goal, indent, "Fact (was given), because facts %s and %s. Returning, success." % (
                ", ".join(self.target_facts), ", ".join(self.found_facts)))
            return True

        results_count = len(self.road)

        for rule in self.rules:
            if rule.right == goal:

                is_satisfied = False
                self.print_step(goal, indent, "Found %s. New goals %s." % (
                    "R" + str(self.rules.index(rule) + 1) + ":" + str(rule), ", ".join(rule.left)))

                for new_goal in rule.left:
                    self.current_goals.append(goal)
                    is_satisfied = self.do_backward_chaining(new_goal, indent + "-")
                    self.current_goals.pop()

                    if self.goal in self.found_facts:
                        # self.output += ("statisfied")
                        return True

                if is_satisfied:
                    self.road.append("R" + str(self.rules.index(rule) + 1))
                    self.found_facts.append(rule.right)
                    self.print_step(goal, indent, "Fact (now given). Facts %s and %s. Returning, success." % (
                        ", ".join(self.target_facts), ", ".join(self.found_facts)))
                    return True

            while len(self.road) > results_count:
                self.road.pop()

        self.print_step(goal, indent, "No productions for deduction. Returning, FAIL.")
        return False

    def print_step(self, goal, indent, msg):
        self.iteration += 1
        self.output += str(self.iteration).rjust(3, " ") + ") %sGoal %s. " % (indent, goal) + msg + "\n"

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
            line = line.split(" ")

            if line[0] == '#':
                continue

            if read_state == 0:
                right = line[0]
                left = line[1:]
                rules.append(Rule(left, right))

            if read_state == 1:
                facts = line

            if read_state == 2:
                goal = line[0]

        return rules, facts, goal

    def print_data(self, rules, facts, goal):
        self.output += "  1) Productions\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Facts\n    %s.\n\n" % ", ".join(facts)
        self.output += "  3) Goal\n    %s.\n\n" % goal

    def print_result(self, result):
        if result is not False:

            if len(self.road) == 0:
                self.output += "  1) Goal %s among facts.\n" % self.goal
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Goal %s derived.\n" % self.goal
                self.output += "  2) Road: %s.\n" % ", ".join(self.road)
        else:
            self.output += "  1) Goal %s unreachable.\n" % self.goal

    def write_output(self, file_name):
        self.output_file_name = "out/BC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)
