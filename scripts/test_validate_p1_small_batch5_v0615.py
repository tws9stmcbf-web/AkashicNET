#!/usr/bin/env python3
import copy
import json
from pathlib import Path

from validate_p1_small_batch5_v0615 import P, validate


def expect_fail(label, mutate):
    data = json.loads(P.read_text())
    mutate(data)
    try:
        validate(data)
    except ValueError:
        return
    raise SystemExit(f'FAIL: mutation unexpectedly passed: {label}')


def main():
    baseline = json.loads(P.read_text())
    if validate(copy.deepcopy(baseline)) is not True:
        raise SystemExit('FAIL: baseline did not pass')

    expect_fail('non-hex private batch digest', lambda d: d.__setitem__('private_batch_sha256', 'z' * 64))
    expect_fail('wrong acquisition route', lambda d: d.__setitem__('acquisition_route', 'DELAYED_LOCAL_PATH_HASHING'))
    expect_fail('denominator drift', lambda d: d.__setitem__('unresolved_after', 44))
    expect_fail('work promotion', lambda d: d.__setitem__('work_ids_promoted', 1))
    expect_fail('edition promotion', lambda d: d.__setitem__('edition_ids_promoted', 1))
    expect_fail('rights promotion', lambda d: d.__setitem__('rights_promoted', 1))
    expect_fail('scientific evidence promotion', lambda d: d.__setitem__('scientific_evidence_promoted', 1))
    expect_fail('object-level Drive ID leak', lambda d: d.__setitem__('drive_id', 'synthetic-private-id'))
    expect_fail('object-level digest leak', lambda d: d.__setitem__('object_sha256', '0' * 64))
    expect_fail('weakened guardrail', lambda d: d.__setitem__('guardrail', 'SHA-256 equality establishes physical byte identity only.'))

    print('PASS: P1 v0.6.15 validator fails closed on synthetic mutations')


if __name__ == '__main__':
    main()
