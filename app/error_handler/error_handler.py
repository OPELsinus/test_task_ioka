import traceback
from functools import wraps

from app.error_handler.error_messages import RequestErrorMessages


def try_execute_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as err:
            error = None
            print("ERRORBEK", err, type(err))
            if str(err) == RequestErrorMessages.AccountAlreadyExists:
                error = err
            if str(err) == RequestErrorMessages.ReceiverAccountDoesntExist:
                print("Here1")
                error = err
            if str(err) == RequestErrorMessages.SenderAccountDoesntExist:
                error = err
            if error is None:
                error = traceback.format_exc()

            return {"success": False, "error_text": str(error)}

    return wrapper
