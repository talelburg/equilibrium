import json

from equilibrium.parsers.parsing_manager import ParsingManager


@ParsingManager.parses("pose")
def parse_pose(snapshot, data_dir_path):
    data = {
        "translation": {
            "x": snapshot.pose.translation.x,
            "y": snapshot.pose.translation.y,
            "z": snapshot.pose.translation.z,
        },
        "rotation": {
            "x": snapshot.pose.rotation.x,
            "y": snapshot.pose.rotation.y,
            "z": snapshot.pose.rotation.z,
            "w": snapshot.pose.rotation.w,
        },
    }
    result_path = data_dir_path / "pose.json"
    with open(result_path, "w") as f:
        json.dump(data, f, indent=4)
    return result_path
