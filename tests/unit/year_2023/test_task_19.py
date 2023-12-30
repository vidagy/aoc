from aoc.year_2023.task_19 import (
    Workflow,
    build_workflow_graph,
    calculate_possibilities,
)

INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}""".split()


def test_task_19():
    workflow_list = [Workflow.create(line) for line in INPUT]
    workflows = {w.workflow_id: w for w in workflow_list}
    workflow_graph = build_workflow_graph(workflows)
    assert calculate_possibilities(workflow_graph, workflows) == 167409079868000
