
import logging
from src import logger as stock_logger


def test_log_info(caplog):
    with caplog.at_level(logging.INFO, logger="StockSenseAI"):
        stock_logger.log_info("Stock information")

    assert "Stock information" in caplog.text


def test_log_warning(caplog):
    with caplog.at_level(logging.WARNING, logger="StockSenseAI"):
        stock_logger.log_warning("Warning message")

    assert "Warning message" in caplog.text


def test_log_error(caplog):
    with caplog.at_level(logging.ERROR, logger="StockSenseAI"):
        stock_logger.log_error("Error message")

    assert "Error message" in caplog.text


def test_log_critical(caplog):
    with caplog.at_level(logging.CRITICAL, logger="StockSenseAI"):
        stock_logger.log_critical("Critical message")

    assert "Critical message" in caplog.text
