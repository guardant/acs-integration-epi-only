from Tramstops_API.buffer_exchange import buffer_exchange
from Tramstops_API.mbd_setup import mbd_setup
from Tramstops_API.mbd_wash import mbd_wash
from Tramstops_API.mbd_cleanup import mbd_cleanup
import os
import sys
import pytest

import comtypes.client

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

def test_buffer_exchange_for_one_batch(logger,number_of_batches="1"):
    logger.info("Test Started")
    buffer_exchange_workflow = buffer_exchange(logger)
    buffer_exchange_workflow.buffer_exchange_workflow(logger,number_of_batches)

def test_buffer_exchange_for_two_batches(logger,number_of_batches="2"):
    logger.info("Test Started")
    buffer_exchange_workflow = buffer_exchange(logger)
    buffer_exchange_workflow.buffer_exchange_workflow(logger,number_of_batches)

def test_mbd_setup_for_one_batch(logger,number_of_batches="1"):
    logger.info("Test Started")
    mbd_setup_workflow = mbd_setup(logger)
    mbd_setup_workflow.mbd_setup_workflow(logger,number_of_batches)

def test_mbd_setup_for_two_batch(logger,number_of_batches="2"):
    logger.info("Test Started")
    mbd_setup_workflow = mbd_setup(logger)
    mbd_setup_workflow.mbd_setup_workflow(logger,number_of_batches)

def test_mbd_wash_for_one_batch(logger,number_of_batches="1"):
    logger.info("Test Started")
    mbd_wash_workflow = mbd_wash(logger)
    mbd_wash_workflow.mbd_wash_workflow(logger,number_of_batches)

def test_mbd_wash_for_two_batch(logger,number_of_batches="2"):
    logger.info("Test Started")
    mbd_wash_workflow = mbd_wash(logger)
    mbd_wash_workflow.mbd_wash_workflow(logger,number_of_batches)

# def test_mbd_cleanup_for_one_batch(logger,number_of_batches="1"):
#     logger.info("Test Started")
#     mbd_cleanup_workflow = mbd_cleanup(logger)
#     mbd_cleanup_workflow.mbd_cleanup_workflow(logger,number_of_batches)



