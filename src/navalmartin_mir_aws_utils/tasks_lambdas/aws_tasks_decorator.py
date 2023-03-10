from functools import wraps
from typing import Callable


def async_aws_lambda_task_decorator(async_before_task_runner: Callable,
                                    async_after_task_runner: Callable):
    def _execute_lambda_task(async_lambda_task_fn: Callable):
        @wraps(async_lambda_task_fn)
        async def wrapper(*args, **kwargs):
            if async_before_task_runner is not None:
                before_task_runner_result = await async_before_task_runner(*args, **kwargs)

            lambda_task_result = await async_lambda_task_fn(*args, **kwargs)

            if async_after_task_runner is not None:
                after_task_runner_result = await async_after_task_runner(*args, **kwargs)
            return lambda_task_result

        return wrapper

    return _execute_lambda_task


def aws_lambda_task_decorator(before_task_runner: Callable,
                              after_task_runner: Callable):
    def _execute_lambda_task(lambda_task_fn: Callable):
        @wraps(lambda_task_fn)
        def wrapper(*args, **kwargs):
            if before_task_runner is not None:
                before_task_runner_result = before_task_runner(*args, **kwargs)
            lambda_task_result = lambda_task_fn(*args, **kwargs)

            if after_task_runner is not None:
                after_task_runner_result = after_task_runner(*args, **kwargs)
            return lambda_task_result

        return wrapper

    return _execute_lambda_task
