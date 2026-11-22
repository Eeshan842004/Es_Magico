# Spec rules (extracted from `starter/summariser/README.md`, "What the product owner asked for")

That README section is the whole spec ("That is the whole spec."). Each bullet is one rule. Tags: **code** = checkable by code, **judge** = needs the LLM judge, **ambiguous** = the spec is vague (see `spec_gaps.md` for our decision).

| ID | Rule (spec wording) | Tag | How we test it |
|---|---|---|---|
| R1 | "A short summary the next agent can read in a few seconds." | **ambiguous** (no number) | Length check C3 with limits we set ourselves (G1); usefulness J5 |
| R2 | "A single short paragraph. No lists, headings or markdown." | **code** | Format check C2: one paragraph, no line breaks, no bullets/numbering/`#`/`**`/`Label:` headings |
| R3 | "It says what the customer wants and where the case stands now." | **judge** | J3 current state; J2 critical completeness; J4 next step (gap G4) |
| R4 | "It only says things that are in the conversation. No guessing." | **judge** + partial code | J1 faithfulness; code check C8 (numbers/IDs not in the conversation) |
| R5 | "Must not expose personal data such as phone numbers, email addresses, full addresses, card numbers or one-time passwords." | **code** | C4 PII regexes (+ Luhn for cards); golden `must_not_include` literals |
| R5b | "Order numbers, amounts and dates are fine and useful." | **code** (an allow-list) | C4 must NOT flag these (false-alarm control); C7 requires them when critical |
| R6 | "Neutral tone. It does not repeat insults or profanity." | **code** + judge | C6 profanity word list; J6 tone |
| R7 | "If there is a safety problem, it says so clearly." | **judge** | Golden case T23 must-include; J2 |

## What the spec does NOT contain (all decided in `spec_gaps.md`)
Length number, language, promises/commitments, customer sentiment, prompt injection, internal notes, resolved/no-next-step cases, "nothing to hand off" cases, changed-mind cases, attachments, third-party callers, voice transcripts, what counts as "essential" detail.

## Where the two prompts stand against the spec (preview, detail in `prompt_diff.md`)
- Neither prompt mentions R2, R4, R5, R6, R7.
- v2 explicitly asks for three labelled lines. R2 says "single short paragraph, no headings". **v2 contradicts the spec by design.**
- v2 says numbers/dates "only when essential"; R5b says they are "useful". Another conflict.
