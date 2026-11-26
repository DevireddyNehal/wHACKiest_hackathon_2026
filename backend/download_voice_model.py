"""Download the small English Vosk model used for local voice recognition."""

from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile


MODEL_NAME = "vosk-model-small-en-us-0.15"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"
MODEL_DIR = Path(__file__).resolve().parent / "models"


def main() -> None:
    destination = MODEL_DIR / MODEL_NAME
    if destination.is_dir():
        print(f"Voice model already installed at {destination}")
        return

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as temporary_directory:
        archive_path = Path(temporary_directory) / f"{MODEL_NAME}.zip"
        print("Downloading the offline speech model (about 40 MB)…")
        urlretrieve(MODEL_URL, archive_path)

        with ZipFile(archive_path) as archive:
            root = MODEL_DIR.resolve()
            for member in archive.infolist():
                extracted_path = (root / member.filename).resolve()
                if extracted_path != root and root not in extracted_path.parents:
                    raise ValueError("The model archive contains an invalid path.")
            archive.extractall(root)

    if not destination.is_dir():
        raise RuntimeError(f"Model archive did not contain {MODEL_NAME}.")
    print(f"Offline speech model installed at {destination}")


if __name__ == "__main__":
    main()
