"""Parser module to parse gear config.json."""
import os
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str, str]:
    """Parses gear config file and returns relevant inputs and config.

    Args:
        gear_context (GearToolkitContext): Context

    Returns:
            - debug
            - path to nifti file
            - nifti file name
    """

    debug = gear_context.config.get("debug")
    nifti_file_path = os.path.dirname(gear_context.get_input_path("input-file"))
    nifti_file_name = gear_context.get_input_filename("input-file")

    return debug, nifti_file_path, nifti_file_name
