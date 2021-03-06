import json
import pathlib
import datetime

import pytest
from click.testing import CliRunner

from equilibrium.parsers import run_parser
from equilibrium.parsers.__main__ import main

DATETIME = f"{datetime.datetime.fromtimestamp(1575446887.339):%Y-%m-%d_%H-%M-%S-%f}"
DATAPATH = (pathlib.Path(__file__).absolute().parent.parent.parent / f"data/42/{DATETIME}").resolve()
POSE = {
    'translation': {
        'x': 0.4873843491077423, 'y': 0.007090016733855009, 'z': -1.1306129693984985
    },
    'rotation': {
        'x': -0.10888676356214629, 'y': -0.26755994585035286, 'z': -0.021271118915446748, 'w': 0.9571326384559261
    }
}
FEELINGS = {'hunger': 0.0, 'thirst': 0.0, 'exhaustion': 0.0, 'happiness': 0.0}
COLOR_IMAGE = {
    'data': str(pathlib.Path(__file__).absolute().parent / "resources/color_image.jpg"),
    'height': 1080,
    'width': 1920
}
DEPTH_IMAGE = {
    'data': str(pathlib.Path(__file__).absolute().parent / "resources/depth_image.jpg"),
    'height': 172,
    'width': 224
}


@pytest.fixture
def data_dir(resources):
    if not DATAPATH.parent.exists():
        DATAPATH.parent.mkdir(parents=True)
    if not DATAPATH.exists():
        DATAPATH.symlink_to(resources, target_is_directory=True)
    yield
    if DATAPATH.is_symlink():
        DATAPATH.unlink()


@pytest.mark.parametrize("parser_name, expected_output", [
    ("pose", POSE),
    ("feelings", FEELINGS),
    ("color_image", COLOR_IMAGE),
    ("depth_image", DEPTH_IMAGE),
])
def test_api(parsed, parser_name, expected_output, data_dir):
    assert json.loads(run_parser(parser_name, json.dumps(parsed)))["result"][parser_name] == expected_output


@pytest.mark.parametrize("parser_name, expected_output", [
    ("pose", POSE),
    ("feelings", FEELINGS),
    ("color_image", COLOR_IMAGE),
    ("depth_image", DEPTH_IMAGE),
])
def test_cli(parsed, parser_name, expected_output, data_dir, tmp_path):
    p = tmp_path / "f'"
    with open(p, "w") as f:
        f.write(json.dumps(parsed))
    output = CliRunner().invoke(main, ["parse", parser_name, str(p)]).output
    result = eval(output)["result"][parser_name]
    assert result == expected_output
