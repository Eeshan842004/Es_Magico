# Golden set: why these 30, why not the other 16

Source: the 45 starter conversations (catalog: `data/conversation_catalog.csv`) + **1 synthetic** (`syn_01`, ours). Selection is **stratified by failure mode, not random**. Slices follow the work plan section 6 and the prompt-diff hypotheses (`prompt_diff.md`).

| Slice | IDs | Earns its place because |
|---|---|---|
| baseline | T36, T19 | Both versions should pass; catches catastrophic breakage; resolved cases test H6 (invented next step) |
| unresolved + next step | T16, T37, T32, T28 | Core use case: next agent must know what to do. Includes contradiction (T16), internal note + handover (T37), attachments the agent can't open (T32), privacy refusal (T28) |
| promise made | T02, T29, T05, T22 | H1: dropping a commitment is the highest-risk omission. T29 is a *conditional* promise; T22 adds a legal threat |
| critical specifics | T40, T38, T27 | Amounts, arithmetic, IDs from a voice transcript. H5 |
| changed mind / contradiction | T15, T39, T06 | Latest state must win: refund approved then retracted (T15), refund issued in error (T39), courier vs customer (T06, Hinglish) |
| multi-issue / long | T14, T17, T35 | H3 over-compression. The data has only 3 multi-issue and 2 truly long threads; all are included |
| angry / escalated | T08 | Profanity, manager demand (R6). T22 also covers a legal threat |
| PII | T03, T04, T34 | R5 lists phone, email, address, card, OTP. Each type has a case: phone+email (T03), address (T04), OTP (T34), card last-4 (T05) |
| trivial / nothing to hand off | T11 | Does the model invent an issue to fill a template? |
| injection | T09, syn_01 | Real poem-style injection + a synthetic one that plants false facts |
| non-English | T07 | Pure Hindi; spec silent on language |
| safety | T23 | R7: must say so clearly |
| internal note | T10 | G12 accusation in an internal note |
| unauthorised promise | T30 | Agent promised a double refund; summary must not launder it into policy |

Counts: 29 real + 1 synthetic = 30. One conversation can cover several slices; each has one primary slice (`primary_slice` in the YAML) and all tags are recorded.

## The 16 not chosen
| ID | Why left out |
|---|---|
| T01 | Near-duplicate of T05/T25 (refund + timeframe); T05 is richer |
| T12 | Same family as T11 ("nothing to hand off"); T11 kept |
| T13 | Spam closed; same family as T11 |
| T18 | Small talk + date; specifics covered by T40/T29; a real loss for the "noise" test (T35 covers noise) |
| T20 | FAQ with prices; low-risk baseline duplicate |
| T21 | Praise only; same family as T11 |
| T24 | Hinglish delivery date; non-English covered by T06 and T07 |
| T25 | Slang/emoji refund; similar to T05 |
| T26 | Email signature/boilerplate noise + phone number in the signature. Good test, left out for count; listed as missing |
| T31 | Backdated invoice; low-risk, similar to T43 |
| T33 | Emoji chat solved; baseline duplicate |
| T41 | Insults + review threat; angry slice covered by T08/T22 |
| T42 | Email PII (data deletion); email PII is covered by T03 |
| T43 | GSTIN billing update; business ID, not PII under G3 |
| T44 | Repeat issue + replacement; similar to T02/T39 |
| T45 | FAQ answered; baseline duplicate |

## What is missing from the golden set (also in NOTES.md)
No multi-day threads, no real attachments, only 1 voice transcript, 1 injection from the starter (+1 ours), tiny per-slice n (1-4), single domain (smart-home support), single language family for non-English, no email-boilerplate case (T26 left out), no case where an agent error is corrected by a *different* agent, all synthetic data.
