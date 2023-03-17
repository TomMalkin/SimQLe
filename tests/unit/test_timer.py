from simqle.timer import Timer
import time


def test_timer_init(mocker):

    mocker.patch.object(Timer, "get_current_time", return_value=3)

    test_timer = Timer()

    assert test_timer.start_time == 3


def test_get_current_time(mocker):

    mock_time = mocker.patch("time.time")

    class MockTimer(Timer):
        def __init__(self):
            self.start_time = 3

    test_timer = MockTimer()

    test_timer.get_current_time()

    mock_time.assert_called_once()


def test_get_elapsed_time(mocker):

    mock_time = mocker.patch("time.time", return_value=5)

    class MockTimer(Timer):
        def __init__(self):
            self.start_time = 3

    test_timer = MockTimer()

    elapsed_time = test_timer.get_elapsed_time()

    assert elapsed_time == 2
    mock_time.assert_called_once()

