import itertools
import multiprocessing

from remake.task import Task
from remake.remake_base import Remake
from remake.task_query_set import TaskQuerySet
from remake.util import format_path


class RemakeMetaclass(type):
    """Provides the machinery for actually creating `TaskRule` classes.

    Uses the information provided by a `TaskRule` to create instances of the task rule, and add them the
    `TaskRule` .tasks list."""
    def __new__(mcs, clsname, bases, attrs):
        if clsname not in ['TaskRule']:
            remake = Remake.current_remake[multiprocessing.current_process().name]
            if 'TaskRule' in [b.__name__ for b in bases]:
                assert 'rule_inputs' in attrs or 'inputs' in attrs
                assert 'rule_outputs' in attrs or 'outputs' in attrs
                attrs['tasks'] = TaskQuerySet(task_ctrl=remake.task_ctrl)
                attrs['task_ctrl'] = remake.task_ctrl
                attrs['next_rules'] = set()
                attrs['prev_rules'] = set()
                var_matrix = {}
        else:
            pass

        newcls = super(RemakeMetaclass, mcs).__new__(
            mcs, clsname, bases, attrs)

        if clsname not in ['TaskRule']:
            if 'TaskRule' in [b.__name__ for b in bases]:
                remake.rules.append(newcls)
                if not var_matrix:
                    var_matrix = attrs.get('var_matrix', None)
                depends_on = attrs.get('depends_on', tuple())
                if var_matrix:
                    for loop_vars in itertools.product(*var_matrix.values()):
                        fmt_dict = {k: v for k, v in zip(var_matrix.keys(), loop_vars)}
                        # This is a little gnarly.
                        # See: https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable
                        # Method has not been bound yet, but you can call it using its __func__ attr.
                        # N.B. both are possible, if e.g. a second rule uses a first rule's method.
                        if hasattr(attrs['rule_inputs'], '__func__'):
                            inputs = attrs['rule_inputs'].__func__(**fmt_dict)
                        elif callable(attrs['rule_inputs']):
                            inputs = attrs['rule_inputs'](**fmt_dict)
                        else:
                            inputs = {k.format(**fmt_dict): format_path(v, **fmt_dict)
                                      for k, v in attrs['rule_inputs'].items()}
                        if hasattr(attrs['rule_outputs'], '__func__'):
                            outputs = attrs['rule_outputs'].__func__(**fmt_dict)
                        elif callable(attrs['rule_outputs']):
                            outputs = attrs['rule_outputs'](**fmt_dict)
                        else:
                            outputs = {k.format(**fmt_dict): format_path(v, **fmt_dict)
                                       for k, v in attrs['rule_outputs'].items()}
                        task = newcls(remake.task_ctrl, attrs['rule_run'], inputs, outputs,
                                      depends_on=depends_on)
                        for k, v in zip(var_matrix.keys(), loop_vars):
                            setattr(task, k, v)
                        newcls.tasks.append(task)
                        remake.task_ctrl.add(task)
                else:
                    task = newcls(remake.task_ctrl, attrs['rule_run'],
                                  attrs['rule_inputs'], attrs['rule_outputs'],
                                  depends_on=depends_on)
                    newcls.tasks.append(task)
                    remake.task_ctrl.add(task)

                remake.tasks.extend(newcls.tasks)
        return newcls


class TaskRule(Task, metaclass=RemakeMetaclass):
    """Core class. Defines a set of tasks in a remakefile.

    Each class must have class-level properties: rule_inputs, rule_outputs, and each must have a method: rule_run.
    Each output file must be unique within a remakefile.
    In the rule_run method, the inputs and outputs are available through e.g. the self.inputs property.

    >>> demo = Remake()
    >>> class TaskSet(TaskRule):
    ...     rule_inputs = {'in': 'infile'}
    ...     rule_outputs = {'out': 'outfile'}
    ...     def rule_run(self):
    ...         self.outputs['out'].write_text(self.inputs['in'].read_text())
    >>> len(TaskSet.tasks)
    1

    Each class can also optionally define a var_matrix, and dependency functions/classes. `var_matrix` should be
    a dict with string keys, and a list of items for each key. There will be as many tasks created as the
    `itertools.product` between the lists for each key. The values will be substituted in to the inputs/outputs.

    >>> def fn():
    ...     print('in fn')
    >>> class TaskSet2(TaskRule):
    ...     rule_inputs = {'in': 'infile'}
    ...     rule_outputs = {'out_{i}{j}': 'outfile_{i}{j}'}
    ...     var_matrix = {'i': [1, 2], 'j': [3, 4]}
    ...     dependencies = [fn]
    ...     def rule_run(self):
    ...         fn()
    ...         self.outputs[f'out_{self.i}'].write_text(str(self.i) + self.inputs['in'].read_text())
    >>> len(TaskSet2.tasks)
    4

    Note, all tasks created by these `TaskRule` are added to the `Remake` object:

    >>> len(demo.tasks)
    5

    When the remakefile is run (`$ remake run` on the command line), all the tasks will be triggered according to their
    ordering. If any of the rule_run methods is changed, then those tasks will be rerun, and if their output is
    is different subsequent tasks will be rerun.
    """
    pass


# TODO: Ideas for new TaskRules:
# class CommandTaskRule(TaskRule):
#    command = ...
# class ScriptTaskRule(TaskRule):
#    script = ...

