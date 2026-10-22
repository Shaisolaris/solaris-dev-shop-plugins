#!/usr/bin/env python3
"""Apply a bounded listing correction to the immutable 0.63.0 release ZIP.

Keeps the release version, all canonical implementation bytes and all executable
modes. Writes a separate submission ZIP and a complete member-hash receipt.
Does not install, upload, publish or replace the released artifact.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import zipfile

BASE_SHA256 = "93266811c90c8aa7661853fa5f173c841c93d1555a8ac4a14c20ff86820a2a08"
SUBTITLE = "61 specialist workflows"
TERMS = "https://github.com/Shaisolaris/solaris-dev-shop-plugins/blob/v0.63.0/LICENSE"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def prepare(base, output):
    base, output = Path(base).resolve(), Path(output).resolve()
    raw = base.read_bytes()
    if digest(raw) != BASE_SHA256:
        raise ValueError("base is not the independently checked 0.63.0 release ZIP")
    if output.exists():
        raise ValueError("output directory already exists; use a fresh owned directory")
    with zipfile.ZipFile(base) as archive:
        infos = archive.infolist()
        source = {entry.filename: archive.read(entry) for entry in infos}
    if len(source) != len(infos):
        raise ValueError("duplicate ZIP member")
    metadata = json.loads(source["plugin.json"])
    provenance = json.loads(source["SOLARIS-BUILD-SOURCE.json"])
    if metadata["version"] != "0.63.0" or provenance["source_version"] != "0.63":
        raise ValueError("unexpected source/package version")
    interface = metadata["extensions"]["com.openai"]["interface"]
    interface["shortDescription"] = SUBTITLE
    interface["termsOfServiceURL"] = TERMS
    script_hash = digest(Path(__file__).read_bytes())
    provenance["submission_metadata_overlay"] = {
        "base_zip_sha256": BASE_SHA256,
        "script_sha256": script_hash,
        "listing_fields": ["shortDescription", "termsOfServiceURL"],
        "canonical_implementation_changed": False,
        "version_changed": False,
    }
    corrected = dict(source)
    corrected["plugin.json"] = json_bytes(metadata)
    corrected["SOLARIS-BUILD-SOURCE.json"] = json_bytes(provenance)
    output.mkdir(parents=True)
    package = output / base.name
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for info in infos:
            archive.writestr(copy.copy(info), corrected[info.filename], compresslevel=9)
    changed = sorted(name for name in source if source[name] != corrected[name])
    receipt = {
        "base_zip_sha256": BASE_SHA256,
        "submission_zip_sha256": digest(package.read_bytes()),
        "script_sha256": script_hash,
        "source_commit": provenance["source_commit"],
        "version": metadata["version"],
        "changed_members": changed,
        "canonical_implementation_changed": False,
        "members": {i.filename: {"sha256": digest(corrected[i.filename]),
                                 "external_attr": i.external_attr}
                    for i in infos},
        "provider_approval": False,
    }
    (output / "SUBMISSION-MANIFEST.json").write_bytes(json_bytes(receipt))
    print(json.dumps({"zip": str(package), "sha256": receipt["submission_zip_sha256"],
                      "changed_members": changed, "members": len(source)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-zip", required=True)
    parser.add_argument("--output-dir", required=True)
    options = parser.parse_args()
    prepare(options.base_zip, options.output_dir)
