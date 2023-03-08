from functools import wraps
from typing import Callable


def async_aws_lambda_task_decorator(async_before_task_runner: Callable,
                                    async_after_task_runner: Callable,
                                    before_task_runner_args: dict,
                                    after_task_runner_args: dict):
    def _execute_lambda_task(async_lambda_task_fn: Callable):
        @wraps(async_lambda_task_fn)
        async def wrapper(*args, **kwargs):
            before_task_runner_result = await async_before_task_runner(before_task_runner_args)
            lambda_task_result = await async_lambda_task_fn(*args, **kwargs)
            after_task_runner_result = await async_after_task_runner(after_task_runner_args)
            return before_task_runner_result, lambda_task_result, after_task_runner_result

        return wrapper

    return _execute_lambda_task


def aws_lambda_task_decorator(before_task_runner: Callable,
                              after_task_runner: Callable,
                              before_task_runner_args: dict,
                              after_task_runner_args: dict):
    def _execute_lambda_task(lambda_task_fn: Callable):
        @wraps(lambda_task_fn)
        def wrapper(*args, **kwargs):
            before_task_runner_result = before_task_runner(before_task_runner_args)
            lambda_task_result = lambda_task_fn(*args, **kwargs)
            after_task_runner_result = after_task_runner(after_task_runner_args)
            return before_task_runner_result, lambda_task_result, after_task_runner_result

        return wrapper

    return _execute_lambda_task
