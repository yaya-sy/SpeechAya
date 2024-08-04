from pathlib import Path
from itertools import tee
from argparse import ArgumentParser
from tqdm import tqdm
import datasets


def build_dataframe(tsv_path: str, root_path: str):
    with open(tsv_path, "r") as tsv:
        next(tsv)  # ignore header
        tsv, for_total = tee(tsv, 2)
        total = sum(1 for _ in for_total)
        for line in tqdm(tsv, total=total):
            columns = line.split("\t")
            _, path, sentence, *_ = columns
            path = root_path / Path(path).with_suffix(".wav")
            if not path.exists():
                continue
            yield {"audio": str(path), "text": sentence}


def build_hf_datasets(tsv_path: str, root_path: str):
    features = datasets.Features(
        {
            "audio": datasets.features.Audio(sampling_rate=16_000),
            "text": datasets.Value("string"),
        }
    )
    dataset = datasets.Dataset.from_generator(
        build_dataframe,
        features=features,
        gen_kwargs={"tsv_path": tsv_path, "root_path": root_path},
    ).cast_column("audio", datasets.Audio())
    return dataset


def parse_args():
    parser = ArgumentParser(
        description="A script for generating huggingface dataset from CommonVoice."
    )
    parser.add_argument(
        "-r",
        "--root-path",
        type=str,
        help="Root path where the audios are stored.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--tsv-path",
        type=str,
        help="Path to the CommonVoice .tsv file.",
        required=True,
    )

    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    dataset = build_hf_datasets(tsv_path=args.tsv_path, root_path=args.root_path)
    dataset.push_to_hub(repo_id="yaya-sy/commonvoice-fr")


if __name__ == "__main__":
    main()
