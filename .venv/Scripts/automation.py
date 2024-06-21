from Tramstops_API.buffer_exchange import buffer_exchange
import os
import pytest_sqa_logging

import threading
import comtypes.client
from contextlib import contextmanager

# @contextmanager
# def com_context():
#     comtypes.CoInitialize()
#     try:
#         yield
#     finally:
#         comtypes.CoUninitialize()
#
# def thread_function():
#     with com_context():
#         # Your thread-specific COM-related code here
#         pass
#
# def main():
#     threads = []
#     for i in range(5):  # Example: creating 5 threads
#         thread = threading.Thread(target=thread_function)
#         threads.append(thread)
#         thread.start()
#
#     for thread in threads:
#         thread.join()
#
# if __name__ == "__main__":
#     main()

def com_context_and_suppress_stderr():
    original_stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    comtypes.CoInitialize()
    try:
        yield
    finally:
        comtypes.CoUninitialize()
        sys.stderr.close()
        sys.stderr = original_stderr

def thread_function(test_function, *args):
    with com_context_and_suppress_stderr():
        test_function(*args)

def main():
    with com_context_and_suppress_stderr():
        pytest.main(["-q", "--disable-warnings"])

if __name__ == "__main__":
    main()

# def test_buffer_exchange_for_one_batch(logger,number_of_batches="1"):
#     logger.info("Test Started")
#     buffer_exchange_wrokflow = buffer_exchange(logger)
#     buffer_exchange_wrokflow.buffer_exchange_workflow(logger,number_of_batches)

def test_buffer_exchange_for_two_batches(logger,number_of_batches="2"):
    logger.info("Test Started")
    buffer_exchange_wrokflow = buffer_exchange(logger)
    buffer_exchange_wrokflow.buffer_exchange_workflow(logger,number_of_batches)