import filecmp
import numpy as np
import pytest

from dr_files.utilities import (
    dr_to_csv,
    dr_to_tdms,
    dr_to_values,
    dr_to_wav,
    DrWriter,
    value_converter,
    float_value_converter,
)


def test_values():
    _, signals = dr_to_values("./fixtures/demo.dr")
    assert pytest.approx(np.mean(signals[0] ** 2), 0.001) == 2.324


def test_wav():
    dr_to_wav("./fixtures/demo.dr", "/tmp/dr.wav")
    assert filecmp.cmp("./fixtures/demo.wav", "/tmp/dr.wav", shallow=True)


def test_tdms():
    dr_to_tdms("./fixtures/demo.dr", "/tmp/dr.tdms")
    assert filecmp.cmp("./fixtures/demo.tdms", "/tmp/dr.tdms", shallow=True)


def test_csv():
    dr_to_csv("./fixtures/demo.dr", "/tmp/dr.csv")
    assert filecmp.cmp("./fixtures/demo.csv", "/tmp/dr.csv", shallow=True)


def test_dr_writer():
    test_header = {
        "sample_rate": 1,
        "channels": [
            {
                "reference": 1,
                "sensitivity": 1000.0,
                "db_reference": 0,
                "pregain": 0,
                "offset": 0,
            },
            {
                "reference": 1,
                "sensitivity": 1000.0,
                "db_reference": 0,
                "pregain": 0,
                "offset": 0,
            },
        ],
    }

    test_data = []
    for i in range(100):
        row = []
        for j in range(2):
            row.append((j + 1) * (i + 10))
        test_data.append(row)

    with open("/tmp/test.dr", "wb") as stream:
        writer = DrWriter(stream)

        writer.write_header(test_header)

        for row in test_data:
            writer.write_row(row)

    dr_to_csv("/tmp/test.dr", "/tmp/test.csv")
    assert filecmp.cmp("./fixtures/fixed_test_writer.csv", "/tmp/test.csv")


def test_dr_writer_row_error():
    with pytest.raises(ValueError):
        test_header = {
            "sample_rate": 1,
            "channels": [
                {
                    "reference": 1,
                    "sensitivity": 1000.0,
                    "db_reference": 0,
                    "pregain": 0,
                    "offset": 0,
                }
            ],
        }

        test_data = []
        for i in range(100):
            row = []
            for j in range(2):
                row.append((j + 1) * (i + 10))
            test_data.append(row)

        with open("/tmp/test.dr", "wb") as stream:
            writer = DrWriter(stream)

            writer.write_header(test_header)

            for row in test_data:
                writer.write_row(row)


def test_value_convertion_simple():
    test_header = {
        "sample_rate": 1,
        "channels": [
            {
                "reference": 1,
                "sensitivity": 4000.0,
                "db_reference": 0.0,
                "pregain": 0.0,
                "offset": 4,
            }
        ],
    }

    with open("/tmp/test.dr", "wb") as stream:
        writer = DrWriter(stream)

        writer.write_header(test_header)

    header, _ = dr_to_values("/tmp/test.dr")
    convert = list(map(value_converter, header.channels))
    reverse = list(map(float_value_converter, header.channels))

    init_value = 5.55566
    rev_value = reverse[0 % len(reverse)](init_value)
    conv_value = convert[0 % len(convert)](rev_value)
    assert init_value == pytest.approx(conv_value)


def test_value_convertion_complex():
    test_header = {
        "sample_rate": 1,
        "channels": [
            {
                "reference": 3,
                "sensitivity": 5000.0,
                "db_reference": 4.2554,
                "pregain": 5,
                "offset": 10,
            }
        ],
    }

    with open("/tmp/test.dr", "wb") as stream:
        writer = DrWriter(stream)

        writer.write_header(test_header)

    header, _ = dr_to_values("/tmp/test.dr")
    convert = list(map(value_converter, header.channels))
    reverse = list(map(float_value_converter, header.channels))

    init_value = 5.55566
    rev_value = reverse[0 % len(reverse)](init_value)
    conv_value = convert[0 % len(convert)](rev_value)
    assert init_value == pytest.approx(conv_value)
