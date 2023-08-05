import shutil
from pathlib import Path


def difference(a, b, out=None, suffixes=None, flatten=False):
    a, b = Path(a), Path(b)

    if out is None:
        out = f"{str(a)}_SUB"
    out = Path(out)

    shutil.rmtree(out, ignore_errors=True)

    rm_list = set([f.name for f in b.glob("**/*.*")])

    src_list = [f for f in a.glob("**/*.*") if f.name not in rm_list]

    if isinstance(suffixes, str):
        suffixes = set(suffixes.split(","))
        src_list = [f for f in src_list if f.suffix in suffixes]

    if flatten:
        dst_list = [out / f.name for f in src_list]
    else:
        dst_list = [out / f.relative_to(a) for f in src_list]

    for f in sorted(set([f.parent for f in dst_list])):
        f.mkdir(parents=True, exist_ok=True)

    for src, dst in zip(src_list, dst_list):
        shutil.copyfile(src, dst)

    return f"copy {len(src_list)} file to {out}"


def refactor(in_dir, out_dir=None, trans=None, level=3):
    in_dir = Path(in_dir)

    if out_dir is None:
        out_dir = f"{str(in_dir)}_NEW"
    out_dir = Path(out_dir)

    shutil.rmtree(out_dir, ignore_errors=True)

    data = list(in_dir.glob("**/*.*"))
    data = {f.name: f for f in sorted(data)}

    src_list = list(data.values())

    def _to(f):
        f = f.relative_to(in_dir)

        if trans is not None:
            for old, new in trans.items():
                f = Path(str(f).replace(old, new))

        return out_dir / Path(*f.parts[-level:])

    dst_list = [_to(f) for f in src_list]

    for f in sorted(set([f.parent for f in dst_list])):
        f.mkdir(parents=True, exist_ok=True)

    for src, dst in zip(src_list, dst_list):
        shutil.copyfile(src, dst)

    return f"copy {len(src_list)} file to {out_dir}"
