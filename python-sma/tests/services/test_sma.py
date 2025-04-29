from src.services.sma_service import SMAService


def test_moving_average():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    window_size = 3
    expected_result = [None, None, 2.0, 3.0, 4.0]
    moving_avarage_result = SMAService.calculate_simple_moving_average(data, window_size)
    assert moving_avarage_result == expected_result
