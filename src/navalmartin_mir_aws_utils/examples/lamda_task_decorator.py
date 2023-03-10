import asyncio
from navalmartin_mir_aws_utils.tasks_lambdas import aws_lambda_task_decorator


def before_task_runner(args: dict):
    print(f"Running before_task_runner with arguments {args}")
    return "Finished before task runner"


def after_task_runner(args: dict):
    print(f"Running after_task_runner with arguments {args}")
    return "Finished after task runner"


@aws_lambda_task_decorator(before_task_runner=before_task_runner,
                           after_task_runner=after_task_runner)
def task(args: dict):
    print(f"Running task with arguments {args}")
    return "None"


if __name__ == '__main__':

    result = task({})
    print(result)