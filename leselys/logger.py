# coding: utf-8
import logging


def get_stream_logger(name='leselys'):
    stream_logger = logging.getLogger(name)
    ch = logging.StreamHandler()
    stream_logger.setLevel(logging.INFO)
    ch.setLevel(logging.INFO)
    stream_logger.addHandler(ch)
    stream_logger.disabled = True
    return stream_logger

stream_logger = get_stream_logger()
