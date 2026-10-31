import { useEffect, useRef, useState } from 'react';
import { request } from './api.js';
import type { MetadataBatch } from '../shared/metadata.js';

type Plan = { knownIds: number; manifestSha256: string; thisPostSha256: string; canScanKnownIds: boolean };

export default function MetadataScanner() {
  const [plan, setPlan] = useState<Plan | null>(null);
  const [cursor, setCursor] = useState('0');
  const [packets, setPackets] = useState<MetadataBatch[]>([]);
  const [running, setRunning] = useState(false);
  const [message, setMessage] = useState('');
  const active = useRef(false);
  const inFlight = useRef(false);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const mounted = useRef(true);
  useEffect(() => () => { mounted.current = false; active.current = false; if (timer.current) clearTimeout(timer.current); }, []);
  const stop = () => { active.current = false; if (timer.current) clearTimeout(timer.current); timer.current = null; if (!inFlight.current) setRunning(false); setMessage('Pausing after the current request. Save the captured packets and resume cursor before closing this view.'); };

  const run = async (mode: MetadataBatch['mode'], automatic: boolean) => {
    if (!plan || running) return;
    let position = mode === 'this-post' ? 0 : Number(cursor);
    if (!Number.isInteger(position) || position < 0) { setMessage('Use the next_cursor from your last saved packet.'); return; }
    active.current = true; setRunning(true); setMessage('Reading metadata…');
    const tick = async () => {
      if (!active.current || !mounted.current) return;
      inFlight.current = true;
      try {
        const packet = await request<MetadataBatch>('/api/metadata/batch', {
          mode, cursor: position, manifest_sha256: mode === 'known-n2n' ? plan.manifestSha256 : plan.thisPostSha256,
        });
        if (!mounted.current) return;
        inFlight.current = false;
        setPackets(old => [...old, packet]);
        position = packet.next_cursor;
        if (mode === 'known-n2n') setCursor(String(position));
        const retry = packet.records.some(record => record.lookup_status === 'retry');
        setMessage(retry ? 'A transient failure stopped the scan at this cursor. Save the packet and retry later.' :
          packet.pass_finished ? 'This queue pass finished. Inspect unavailable and suppressed records before integrating metadata.' : `Next cursor: ${position} of ${packet.known_ids}. Save your packets before leaving.`);
        if (active.current && automatic && !packet.pass_finished && !retry) {
          timer.current = setTimeout(() => { void tick(); }, (packet.retry_after_seconds + 1) * 1000);
        } else { active.current = false; setRunning(false); }
      } catch (error) {
        inFlight.current = false;
        if (mounted.current) { active.current = false; setRunning(false); setMessage(error instanceof Error ? error.message : 'Metadata lookup failed. The current cursor has not advanced.'); }
      }
    };
    void tick();
  };

  const exportText = JSON.stringify({ schema: 'akashicnet.devvit.metadata-capture.v1', packets }, null, 2);
  return <section className="panel composer" aria-labelledby="metadata-scanner-title">
    <p className="eyebrow">MODERATOR METADATA WORKSPACE</p>
    <h2 id="metadata-scanner-title">Capture the N2N metadata trail</h2>
    <p>Read the known archive IDs in small batches. Titles, flair, dates, submitted links and engagement snapshots carry a retrieval date. No post text, comments or author identities are collected.</p>
    {!plan && <button onClick={() => { void request<Plan>('/api/metadata/plan').then(setPlan).catch(error => setMessage(String(error))); }}>Inspect the scan queue</button>}
    {plan && <>
      <p><strong>{plan.knownIds.toLocaleString('en-GB')} known N2N IDs.</strong> This queue does not establish complete subreddit history.</p>
      {!plan.canScanKnownIds && <p className="boundary">In this test community, only the current companion post can be checked. The N2N queue is unavailable here.</p>}
      <label>Resume cursor from your last saved N2N packet<input type="number" min="0" max={plan.knownIds} value={cursor} disabled={running} onChange={event => setCursor(event.target.value)} /></label>
      <div className="actions">
        <button disabled={running} onClick={() => void run('this-post', false)}>Check this test post</button>
        {plan.canScanKnownIds && <><button disabled={running} onClick={() => void run('known-n2n', false)}>Capture next 5</button><button className="primary" disabled={running} onClick={() => void run('known-n2n', true)}>Start / resume known-ID scan</button></>}
        {running && <button onClick={stop}>Pause after current request</button>}
      </div>
      <p className="muted">The scan continues only while this view stays open. Captured packets stay in memory in this view; copy them before closing or reloading. The app does not send them to AkashicNET or store post content on its server. Starting a scan creates no posts.</p>
    </>}
    {message && <p role="status">{message}</p>}
    {packets.length > 0 && <details><summary>Save captured JSON and resume cursor · {packets.reduce((sum, packet) => sum + packet.records.length, 0)} observations in this view</summary>
      <p>Review before external integration. These packets are dated observations, with no automatic evidence or reuse-rights approval. External storage needs a deletion and refresh process.</p>
      <label>Captured JSON<textarea readOnly rows={12} value={exportText} onFocus={event => event.currentTarget.select()} /></label>
      <button onClick={() => { void navigator.clipboard.writeText(exportText).then(() => setMessage('Captured JSON copied.')).catch(() => setMessage('Select the JSON text above and use your device’s Copy command.')); }}>Copy captured JSON</button>
    </details>}
  </section>;
}
