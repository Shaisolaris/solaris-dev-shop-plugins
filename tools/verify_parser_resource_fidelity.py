#!/usr/bin/env python3
"""Compare public frozen source with the parser-compatibility candidate.

Only local Git objects and source files are read. No workflow, fixture payload,
network, package manager or marketplace action is executed by this verifier.
"""
import argparse
import ast
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess

BASE = '8c5d1e21b8f4568e73cb58f81ff7ca27ca0d867f'
ENV = {'PATH': '/usr/bin:/bin', 'GIT_CONFIG_NOSYSTEM': '1',
       'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_SYSTEM': '/dev/null'}
DATA = 'employees/design/ui-ux-designer/design-intelligence/data/'
TABLES = ('charts.csv', 'products.csv', 'stacks/flutter.csv', 'stacks/nextjs.csv',
          'stacks/svelte.csv', 'stacks/threejs.csv', 'stacks/vue.csv')


def git(repository, *arguments):
    return subprocess.check_output(['/usr/bin/git', '-C', str(repository), *arguments], env=ENV)


def original(repository, name):
    return git(repository, 'show', BASE + ':' + name)


def table(raw):
    return list(csv.reader(io.StringIO(raw.decode('utf-8'), newline='')))


def compare_table(name, before, after):
    if len(before) != len(after) or [len(x) for x in before] != [len(x) for x in after]:
        raise ValueError('Table rows or legacy widths changed: ' + name)
    changed = []
    for row, values in enumerate(before):
        for column, value in enumerate(values):
            replacement = after[row][column]
            if replacement == value:
                continue
            permitted = (
                name == 'stacks/nextjs.csv' and value == 'Export GET POST PUT DELETE'
                and replacement == 'Provide named GET, POST, PUT and DELETE HTTP handlers.'
            ) or (
                name == 'stacks/svelte.csv' and value == '{items.map(i => `<div>${i}</div>`)}'
                and replacement == '{items.map(i => "<div>".concat(i, "</div>"))}'
            )
            if not permitted:
                raise ValueError('Unreviewed table cell changed: ' + name + ':' + str((row, column)))
            changed.append({'row': row, 'column': column, 'before': value, 'after': replacement})
    return changed


def masked_reference(source):
    lines = source.splitlines(keepends=True)
    result = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith('● Neon Pulse:'):
            result.append('NEON_PULSE_REFERENCE\n')
            if '```typescript' not in line:
                index += 1
                if lines[index].strip() != '```typescript':
                    raise ValueError('Unexpected Neon Pulse reference structure')
                index += 1
                while lines[index].strip() != '```':
                    index += 1
        elif 'No Harsh Shadows:' in line:
            result.append('SHADOW_GUIDANCE\n')
        else:
            result.append(line)
        index += 1
    return ''.join(result)


def methods(source):
    result = {}
    for item in ast.walk(ast.parse(source)):
        if isinstance(item, ast.ClassDef):
            for method in item.body:
                if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name.startswith('test_'):
                    result[item.name + '.' + method.name] = [ast.dump(x, include_attributes=False)
                                                            for x in method.decorator_list]
    return result


def assertion_shapes(source):
    return [ast.dump(node, include_attributes=False) for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name) and node.func.value.id == 'self'
            and node.func.attr.startswith('assert')]


def verify(repository):
    records = []
    for name in TABLES:
        before = table(original(repository, DATA + name))
        after = table((repository / (DATA + name)).read_bytes())
        changed = compare_table(name, before, after)
        records.append({'table': name, 'rowsIncludingHeader': len(before),
                        'allOtherCellsAndRowWidthsIdentical': True, 'reviewedCellChanges': changed})
        # The integrity checker itself must reject missing rows and unapproved data changes.
        for bad in (after[:-1], [row[:] for row in after]):
            if len(bad) == len(after):
                bad[0][0] += '-unapproved-control'
            try:
                compare_table(name, before, bad)
            except ValueError:
                pass
            else:
                raise ValueError('Table integrity negative control was not detected')
    for name in ('design', 'draft'):
        before = original(repository, DATA + name + '.csv').decode()
        after = (repository / (DATA + name + '.md')).read_text()
        if masked_reference(before) != masked_reference(after):
            raise ValueError('Design reference content was lost outside the two reviewed edits')
        for literal in ('shadowOffset: { width: 0, height: 0 }', 'shadowRadius: pulseAnim',
                        'shadowColor: colors.accent', 'shadowOpacity: 0.6'):
            if literal not in before or literal not in after:
                raise ValueError('A design reference property was lost')
        records.append({'reference': name, 'allOtherContentByteIdentical': True})
    source = original(repository, 'employees/quality-security/code-reviewer/SKILL.md').decode()
    start = source.index('```\n## 🚨 Blockers')
    end = source.index('\n```', start) + 4
    expected = source[start:end][4:-4].rstrip() + '\n'
    if (repository / 'employees/quality-security/code-reviewer/examples/review-report.md').read_text() != expected:
        raise ValueError('The original complete review example was not retained')
    source = original(repository, 'employees/specialized/wordpress-master/diagnostics/reporting/SKILL.md').decode()
    start = source.index('> "Missing CSRF protection')
    expected = source[start:source.index('\n\n## Severity Definitions', start)] + '\n'
    if (repository / 'employees/specialized/wordpress-master/diagnostics/reporting/examples/csrf-finding.md').read_text() != expected:
        raise ValueError('The original complete CSRF example was not retained')
    names = git(repository, 'ls-tree', '-r', '--name-only', BASE).decode().splitlines()
    contracts = [name for name in names if name.endswith('/capability.contract.json')]
    for name in contracts:
        if original(repository, name) != (repository / name).read_bytes():
            raise ValueError('A capability or permission contract changed: ' + name)
    test_count = 0
    for name in names:
        if name.startswith('tests/test_') and name.endswith('.py'):
            before = methods(original(repository, name).decode())
            after = methods((repository / name).read_text())
            if not before.keys() <= after.keys() or any(before[key] != after[key] for key in before):
                raise ValueError('An original test case or skip policy changed: ' + name)
            test_count += len(before)
    name = 'tests/test_g03_capability.py'
    if assertion_shapes(original(repository, name).decode()) != assertion_shapes((repository / name).read_text()):
        raise ValueError('An original SQLite recovery assertion changed')
    return {'base': BASE, 'tables': records, 'allCapabilityContractsUnchanged': len(contracts),
            'originalDeclaredTestMethodsRetained': test_count, 'originalG03AssertionsUnchanged': True,
            'tableNegativeControlsPassed': True, 'sourceOrWorkflowCodeExecuted': False,
            'nvidiaClearance': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--core', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.core.resolve()), indent=2))
