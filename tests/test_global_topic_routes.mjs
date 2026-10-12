import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { isPublicTopic } from '../website/app/topics/public-eligibility.mjs';
const seed = JSON.parse(readFileSync(new URL('../data/global_metadata_discovery_v01.seed.json', import.meta.url)));
const clearance = { decision: 'CLEARED', reviewed_on: '2026-09-30', decision_ref: 'test-fixture-only', privacy_checked: true, rights_checked: true, cultural_sovereignty_checked: true };
const record = () => ({ ...structuredClone(seed.topics[0]), public_clearance: { ...clearance } });

test('all uncleared seed records are withheld', () => {
  assert.equal(seed.topics.filter(isPublicTopic).length, 0);
});
test('clearance is explicit for every status, independent of evidence review', () => {
  for (const status of ['stub', 'discovery', 'reviewed', 'public']) {
    const topic = record();
    topic.status = status;
    topic.review = { human_reviewed: true, last_reviewed: '2026-09-30', notes: 'Fixture' };
    assert.equal(isPublicTopic(topic), true);
    for (const field of Object.keys(clearance)) {
      const altered = structuredClone(topic);
      delete altered.public_clearance[field];
      assert.equal(isPublicTopic(altered), false, `${status}: missing ${field}`);
    }
    delete topic.public_clearance;
    assert.equal(isPublicTopic(topic), false);
  }
});
test('HOLD, false checks, invalid dates and unknown rights cannot route', () => {
  for (const [key, value] of [['decision', 'HOLD'], ['decision_ref', ' '], ['reviewed_on', 'invalid'], ['reviewed_on', '2026-02-30'], ['privacy_checked', false], ['rights_checked', false], ['cultural_sovereignty_checked', false]]) {
    const topic = record(); topic.public_clearance[key] = value;
    assert.equal(isPublicTopic(topic), false, key);
  }
  const topic = record(); topic.rights.mode = 'unknown';
  assert.equal(isPublicTopic(topic), false);
});
test('clearance cannot bypass review or rights promotion', () => {
  for (const status of ['reviewed', 'public']) {
    const topic = record(); topic.status = status;
    assert.equal(isPublicTopic(topic), false);
    topic.review = { human_reviewed: true, last_reviewed: '2026-09-30', notes: 'Fixture' };
    assert.equal(isPublicTopic(topic), true);
    topic.sources = [];
    assert.equal(isPublicTopic(topic), false);
  }
  const topic = record(); topic.status = 'public'; topic.rights.mode = 'metadata-only';
  topic.review = { human_reviewed: true, last_reviewed: '2026-09-30', notes: 'Fixture' };
  assert.equal(isPublicTopic(topic), false);
});
