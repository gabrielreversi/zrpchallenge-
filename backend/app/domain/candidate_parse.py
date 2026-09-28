import re
from pathlib import PurePosixPath

_NAME_PATTERN = re.compile(
    r"Candidat[ao]\s+[A-Z]\s+\(([^)]+)\)\s*:",
    re.IGNORECASE,
)


def extract_candidate_name(cv_text: str, filename: str) -> str:
    match = _NAME_PATTERN.search(cv_text)
    if match:
        return match.group(1).strip()
    stem = PurePosixPath(filename).stem
    return stem or "Candidato"


def candidate_id_from_filename(filename: str) -> str:
    stem = PurePosixPath(filename).stem.strip()
    return stem or "candidate"
