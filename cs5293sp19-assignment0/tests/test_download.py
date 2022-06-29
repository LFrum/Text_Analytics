import pytest

import assignment0
from assignment0 import main


def test_download_sanity():
    assert main.download() is not None


def test_download_size():
    assert len(main.download()) == 135131
