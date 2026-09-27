"""Build a disposable local overlay; do not edit the installed dependency."""

import argparse
import hashlib
import importlib.metadata
from pathlib import Path
import shutil


HASHES = {
    "factscorer.py": "69ee2bb09dcd86f16e77397d168ffec9100b313bbc84c646573fbc0d7f8a6526",
    "openai_lm.py": "382afabaf96f6ddf79cb1d2c427774f3bc1c4d38874068a9e136a67e68811b41",
    "atomic_facts.py": "16d095911fe3a372e34c9abd917f0223503cef586db172c6ab20e8436ccd6737",
}


def prepare(destination):
    dist = importlib.metadata.distribution("factscore")
    if dist.version != "0.2.0":
        raise ValueError("Only reviewed factscore==0.2.0 is supported")
    source = Path(dist.locate_file("factscore")).resolve()
    texts = {}
    for name, digest in HASHES.items():
        data = (source / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Unreviewed upstream content: {name}")
        texts[name] = data.decode("utf-8")
    destination = Path(destination).resolve()
    if destination.exists() or source in destination.parents:
        raise ValueError("Use a new overlay directory outside the installed package")

    lm = texts["openai_lm.py"]
    lm = lm.replace("import logging", "import logging\nfrom factscore.akashicnet_compat import ModelConfig, generate")
    lm = lm.replace("        self.model_name = model_name", "        self.compat = ModelConfig.from_role(model_name)\n        cache_file = self.compat.cache_path(cache_file)\n        self.model_name = model_name", 1)
    # Replace dispatch and obsolete unbounded API helpers, retaining key loading.
    lm = lm[:lm.index("        if self.model_name == \"ChatGPT\":")] + (
        "        # Preserve upstream per-role token budgets during compatibility review.\n"
        "        budget = max_sequence_length if self.model_name == 'ChatGPT' else 512\n"
        "        return generate(self.compat, prompt, budget, self.temp)\n")
    atomic = texts["atomic_facts.py"].replace(
        'nltk.download("punkt")', 'from factscore.akashicnet_compat import require_tokenizer')
    atomic = atomic.replace('        self.nlp = spacy.load(', '        require_tokenizer()\n        self.nlp = spacy.load(', 1)
    scorer = texts["factscorer.py"]
    start = scorer.index("    def print_cost_estimates(")
    end = scorer.index("    def get_score(", start)
    scorer = scorer[:start] + (
        "    def print_cost_estimates(self, total_words, task, model):\n"
        "        logging.warning('Compatibility mode: monetary cost estimate unavailable; '\n"
        "                        'verify selected model pricing separately.')\n\n"
    ) + scorer[end:]
    # No package imports: preparing the overlay cannot invoke upstream downloads.
    destination.mkdir(parents=True)
    target = destination / "factscore"
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (target / "openai_lm.py").write_text(lm, encoding="utf-8")
    (target / "atomic_facts.py").write_text(atomic, encoding="utf-8")
    (target / "factscorer.py").write_text(scorer, encoding="utf-8")
    shutil.copyfile(Path(__file__).with_name("factscore_compat.py"), target / "akashicnet_compat.py")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(prepare(args.destination))
