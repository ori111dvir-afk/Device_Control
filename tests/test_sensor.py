import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import sensor


class SensorTest(unittest.TestCase):
    def test_read_value_returns_float_for_valid_data(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as temp_file:
            temp_file.write("42.5\n")
            temp_file.write("0.0\n")
            temp_file.write("100.0\n")
            temp_path = temp_file.name

        try:
            sensor_obj = sensor.Sensor(temp_path)
            res = sensor_obj.read_value()
            self.assertEqual(res.value, 42.5)
            self.assertEqual(res.status, "ok")

            res = sensor_obj.read_value()
            self.assertEqual(res.value, 0.0)
            self.assertEqual(res.status, "ok")

            res = sensor_obj.read_value()
            self.assertEqual(res.value, 100.0)
            self.assertEqual(res.status, "ok")

            res = sensor_obj.read_value()
            self.assertIsNone(res.value)
            self.assertEqual(res.status, "invalid-value", "EOF should return invalid-value status")
        finally:
            sensor_obj.close()
            Path(temp_path).unlink(missing_ok=True)

    def test_read_value_returns_none_for_invalid_float(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as temp_file:
            temp_file.write("not-a-number\n")
            temp_path = temp_file.name

        try:
            sensor_obj = sensor.Sensor(temp_path)
            res = sensor_obj.read_value()
            self.assertIsNone(res.value)
            self.assertEqual(res.status, "invalid-value")
        finally:
            sensor_obj.close()
            Path(temp_path).unlink(missing_ok=True)

    def test_read_value_returns_none_for_out_of_range_values(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as temp_file:
            temp_file.write("-1.0\n")
            temp_file.write("101.0\n")
            temp_path = temp_file.name

        try:
            sensor_obj = sensor.Sensor(temp_path)
            res = sensor_obj.read_value()
            self.assertIsNone(res.value)
            self.assertEqual(res.status, "out-of-range")

            res = sensor_obj.read_value()
            self.assertIsNone(res.value)
            self.assertEqual(res.status, "out-of-range")
        finally:
            sensor_obj.close()
            Path(temp_path).unlink(missing_ok=True)

    def test_read_value_returns_none_when_file_cannot_be_opened(self):
        sensor_obj = sensor.Sensor("nonexistent_sensor_file.dat")
        self.assertIsNone(sensor_obj.file)
        res = sensor_obj.read_value()
        self.assertIsNone(res.value)
        self.assertEqual(res.status, "invalid-value")
        sensor_obj.close()

    def test_close_closes_open_file(self):
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False) as temp_file:
            temp_file.write("15.0\n")
            temp_path = temp_file.name

        try:
            sensor_obj = sensor.Sensor(temp_path)
            sensor_obj.close()
            self.assertIsNone(sensor_obj.file)
            res = sensor_obj.read_value()
            self.assertIsNone(res.value)
            self.assertEqual(res.status, "invalid-value")
        finally:
            Path(temp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
