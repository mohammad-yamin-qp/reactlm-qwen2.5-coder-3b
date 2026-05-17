"""Aggregate all curriculum seed modules for split_dataset."""

from styling_examples import STYLING_EXAMPLES
from styling_scss_examples import SCSS_EXAMPLES
from quality_examples import QUALITY_EXAMPLES

from seeds.extra_seeds import EXTRA_SEEDS
from seeds.folder_structure_examples import FOLDER_STRUCTURE_EXAMPLES
from seeds.generated_curriculum import GENERATED_CURRICULUM

ALL_CURRICULUM_SEEDS: list[dict] = (
    EXTRA_SEEDS
    + GENERATED_CURRICULUM
    + FOLDER_STRUCTURE_EXAMPLES
    + STYLING_EXAMPLES
    + SCSS_EXAMPLES
    + QUALITY_EXAMPLES
)

__all__ = [
    "ALL_CURRICULUM_SEEDS",
    "EXTRA_SEEDS",
    "FOLDER_STRUCTURE_EXAMPLES",
    "GENERATED_CURRICULUM",
]
