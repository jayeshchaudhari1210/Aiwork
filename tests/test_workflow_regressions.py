from aiwork import Flow, Task, Orchestrator


def test_missing_dependency_marks_workflow_failed():
    flow = Flow('missing')
    flow.add_task(Task('consumer', lambda ctx: {}), depends_on=['absent'])
    executor = Orchestrator()
    result = executor.execute(flow)
    state = executor.state_manager.get_workflow_state(result['workflow_id'])
    assert state['status'] == 'FAILED'


def test_returned_subflow_executes_tasks_in_dependency_order():
    child = Flow('child')
    child.add_task(Task('first', lambda ctx: {'value': 4}))
    child.add_task(Task('second', lambda ctx: {'value': ctx['outputs']['first']['value'] + 1}), depends_on=['first'])
    parent = Flow('parent')
    parent.add_task(Task('spawn', lambda ctx: child))
    result = Orchestrator().execute(parent)
    assert result['outputs']['second']['value'] == 5


def test_invalid_dynamic_tasks_marks_workflow_failed():
    flow = Flow('invalid')
    flow.add_task(Task('bad', lambda ctx: {'next_tasks': ['not a task']}))
    executor = Orchestrator()
    result = executor.execute(flow)
    assert executor.state_manager.get_workflow_state(result['workflow_id'])['status'] == 'FAILED'
