import shutil
import pandas as pd
from pathlib import Path


def _parse(filters):
    set_out, set_in = set(), set()

    if filters is None:
        return set_out, set_in

    for f in filters.split(","):
        is_in = True
        if f.startswith("-"):
            is_in, f = False, f[1:]

        if f.endswith(".csv"):
            dat = pd.read_csv(f)["file_name"].tolist()
            dat = [Path(file_name).name for file_name in dat]
        elif f.endswith("/"):
            dat = [file_name.name for file_name in Path(f).glob("**/*.*")]

        if is_in:
            set_in.update(dat)
        else:
            set_out.update(dat)

    return set_out, set_in


def difference(a, b=None, out=None, suffixes=None, flatten=False):
    a = Path(a)

    if out is None:
        out = f"{str(a)}_SUB"
    out = Path(out)

    shutil.rmtree(out, ignore_errors=True)

    data = list(a.glob("**/*.*"))
    data = {f.name: f for f in sorted(data)}

    src_list = list(data.values())

    if b is not None:
        rm_list = set([f.name for f in Path(b).glob("**/*.*")])
        src_list = [f for f in src_list if f.name not in rm_list]

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


def refactor(in_dir, out_dir=None, filters=None, trans=None, level=3):
    in_dir = Path(in_dir)

    if out_dir is None:
        out_dir = f"{str(in_dir)}_NEW"
    out_dir = Path(out_dir)

    shutil.rmtree(out_dir, ignore_errors=True)

    data = list(in_dir.glob("**/*.*"))
    data = {f.name: f for f in sorted(data)}

    src_list = list(data.values())

    set_out, set_in = _parse(filters)
    if set_in:
        src_list = [f for f in src_list if f.name in set_in]
    if set_out:
        src_list = [f for f in src_list if f.name not in set_out]

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
