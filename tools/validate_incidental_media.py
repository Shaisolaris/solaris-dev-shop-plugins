#!/usr/bin/env python3
"""Read-only structural checks for native NVIDIA incidental PNG/GIF records.

This never changes a vendor report, marks a partial scan complete, suppresses a
finding, or certifies rendered meaning. Raw YARA/integrity checks remain required.
"""
import hashlib
from pathlib import Path
import struct
import zlib
from PIL import Image


def png_structure(data):
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('PNG signature mismatch')
    offset = 8
    chunks = []
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG chunk')
        size = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + size
        if end > len(data) or not all(65 <= x <= 90 or 97 <= x <= 122 for x in kind):
            raise ValueError('Invalid PNG chunk bounds/type')
        payload = data[offset + 8:offset + 8 + size]
        expected = struct.unpack('>I', data[offset + 8 + size:end])[0]
        if zlib.crc32(kind + payload) & 0xffffffff != expected:
            raise ValueError('PNG CRC mismatch')
        if not chunks and (kind != b'IHDR' or size != 13):
            raise ValueError('PNG must begin with one IHDR')
        if kind == b'IHDR' and chunks:
            raise ValueError('Repeated PNG header')
        chunks.append(kind.decode('ascii'))
        offset = end
        if kind == b'IEND':
            if size != 0 or offset != len(data) or 'IDAT' not in chunks:
                raise ValueError('Invalid PNG end or trailing bytes')
            return chunks
    raise ValueError('Missing PNG end')


def gif_structure(data):
    if data[:6] not in (b'GIF87a', b'GIF89a') or len(data) < 14:
        raise ValueError('GIF signature/header mismatch')
    packed = data[10]
    offset = 13 + (3 * 2 ** ((packed & 7) + 1) if packed & 128 else 0)
    images = 0
    def subblocks(start):
        while start < len(data):
            size = data[start]
            start += 1
            if not size:
                return start
            start += size
            if start > len(data):
                raise ValueError('Truncated GIF subblock')
        raise ValueError('Missing GIF subblock terminator')
    while offset < len(data):
        marker = data[offset]
        offset += 1
        if marker == 0x3b:
            if offset != len(data) or not images:
                raise ValueError('Invalid GIF trailer or trailing bytes')
            return images
        if marker == 0x21:
            if offset >= len(data):
                raise ValueError('Truncated GIF extension label')
            offset = subblocks(offset + 1)
        elif marker == 0x2c:
            if offset + 9 > len(data):
                raise ValueError('Truncated GIF image descriptor')
            packed = data[offset + 8]
            offset += 9 + (3 * 2 ** ((packed & 7) + 1) if packed & 128 else 0)
            if offset >= len(data) or not 2 <= data[offset] <= 8:
                raise ValueError('Invalid GIF LZW size')
            offset = subblocks(offset + 1)
            images += 1
        else:
            raise ValueError('Unknown GIF block marker')
    raise ValueError('Missing GIF trailer')


def validate_image(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_mode & 0o111:
        raise ValueError('Only regular non-executable image assets qualify')
    data = path.read_bytes()
    extension = path.suffix.lower()
    if extension == '.png':
        structure = {'chunks': png_structure(data)}
        expected_format = 'PNG'
    elif extension == '.gif':
        structure = {'imageBlocks': gif_structure(data)}
        expected_format = 'GIF'
    else:
        raise ValueError('This contract covers only PNG and GIF')
    with Image.open(path) as image:
        if image.format != expected_format:
            raise ValueError('Image format disagrees with suffix')
        image.verify()
    with Image.open(path) as image:
        frames = getattr(image, 'n_frames', 1)
        size = image.size
        for index in range(frames):
            image.seek(index)
            image.load()
    if extension == '.gif' and structure['imageBlocks'] != frames:
        raise ValueError('GIF frame count disagrees with decoded frames')
    if path.read_bytes() != data:
        raise ValueError('Image changed during validation')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
            'format': expected_format, 'size': size, 'framesDecoded': frames,
            'sourceBytesUnchanged': True, 'nonExecutable': True, **structure}


def native_media_contract(report, root, files):
    """Honor only the vendor's complete incidental-media non-applicability case."""
    completeness = report.get('analysis_completeness', {})
    entries = completeness.get('scope_exclusions', [])
    if not entries:
        return {}
    if completeness.get('is_complete') is not True or completeness.get('ledger_exceptions'):
        raise ValueError('Media validation never changes partial native completion')
    statuses = {x['analyzer_id']: x for x in completeness.get('analyzer_statuses', [])}
    for name in ('artifact_integrity', 'static_yara'):
        status = statuses.get(name, {})
        if (status.get('status') != 'completed' or status.get('completed', -1) < len(files)
                or status.get('planned_work') != status.get('completed')
                or any(status.get(key) != 0 for key in ('partial', 'skipped', 'failed', 'unaccounted'))):
            raise ValueError('Full native binary integrity and raw-byte YARA are mandatory')
    validated = {}
    for entry in entries:
        name = entry.get('path')
        if (name not in files or entry.get('outcome') != 'out_of_scope' or entry.get('fatal')
                or (entry.get('phase'), entry.get('reason_code')) not in {
                    ('cache', 'binary_text_projection'), ('static', 'binary_content')}):
            raise ValueError('Unexpected exclusion; no source exclusion is accepted')
        if name not in validated:
            validated[name] = validate_image(Path(root) / name)
        if validated[name]['sha256'] != files[name]['sha256'] or files[name]['executable']:
            raise ValueError('Media differs from the exact immutable package inventory')
    return validated
