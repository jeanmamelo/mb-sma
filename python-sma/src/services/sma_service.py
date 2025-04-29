class SMAService:
    @staticmethod
    def calculate_simple_moving_average(data: list[float], window_size: int) -> list[float]:
        result = []
        for i in range(len(data)):
            if i < window_size - 1:
                result.append(None)
            else:
                window = data[i - window_size + 1 : i + 1]
                result.append(sum(window) / window_size)
        return result
