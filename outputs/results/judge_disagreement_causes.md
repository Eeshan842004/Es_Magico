# Where the two judges disagree, and why

105 criterion-level disagreements on 180 shared summaries.

| cause | count |
|---|---|
| Rubric ambiguous: implied step or inference | 42 |
| Rubric ambiguous: part of a compound fact missing | 32 |
| gpt-oss wrong: the claim is supported | 11 |
| Gemini too lenient: missed a real problem | 9 |
| Golden expectation flawed (T38 status) | 6 |
| gpt-oss out of scope: graded PII under J6 | 5 |

| summary | criterion | failed by | cause | that judge's reason |
|---|---|---|---|---|
| T03 v1 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Includes an invented claim that no troubleshooting has been done yet, which is not supported by the conversation. |
| T03 v1 run 2 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Contains an invented claim about the purpose of the call (to resolve the broken bulb issue) not supported by the conversation. |
| T03 v2 run 2 | J6 | gpt-oss | gpt-oss out of scope: graded PII under J6 | The summary includes the customer's phone number and email address, which are PII and should not be disclosed. |
| T03 v2 run 4 | J6 | gpt-oss | gpt-oss out of scope: graded PII under J6 | Includes the customer's phone number, which is prohibited PII per the must_not_include list. |
| T04 v1 run 0 | J6 | gpt-oss | gpt-oss out of scope: graded PII under J6 | The summary includes the full delivery address, which is personal identifying information and should not be disclosed. |
| T04 v2 run 0 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Includes an invented next‑step claim not supported by the dialogue. |
| T04 v2 run 0 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | Invents a next step (confirm shipment) despite the case being resolved; no next step was stated. |
| T04 v2 run 0 | J6 | gpt-oss | gpt-oss out of scope: graded PII under J6 | Exposes full customer address (PII), violating safety/privacy expectations. |
| T04 v2 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains an invented claim that the order is ready for dispatch, which is not supported by the conversation. |
| T04 v2 run 1 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | The summary invents a next step ('ready for dispatch') that was not mentioned; for a resolved case it should state no action needed without adding new information. |
| T04 v2 run 1 | J6 | gpt-oss | gpt-oss out of scope: graded PII under J6 | The summary includes the full delivery address, exposing personal data that should not be shared. |
| T05 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered – the summary mentions the reversal reference but does not explicitly state that the agent confirmed the duplicate charge. |
| T05 v2 run 3 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary adds a next step (follow up on 20 Nov) that was not mentioned in the conversation. |
| T05 v2 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Missing or partial critical facts: M2 lacks explicit agent confirmation of duplicate charge (only reversal mentioned), M4 does not state the customer's intent to dispute if not refunded by the 20th. |
| T05 v2 run 3 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | The next step is invented and not supported by the conversation; no actionable step was defined. |
| T06 v2 run 0 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Summary adds a next step that was not mentioned in the conversation, constituting an invented claim. |
| T06 v2 run 0 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | Next step is invented and not derived from the conversation; also vague about who should act. |
| T06 v2 run 3 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary adds a next‑step claim that is not mentioned in the conversation. |
| T07 v1 run 4 | J4 | gpt-oss | gpt-oss wrong: the claim is supported | The summary does not specify a clear actionable next step or who is responsible (e.g., monitor delivery, follow‑up). |
| T08 v1 run 0 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Missing critical detail that the agent could not transfer the call (M2). The summary mentions the manager flag but omits the inability to transfer. |
| T08 v1 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Missing the critical detail that the agent could not transfer the call (M2). |
| T08 v1 run 4 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Contains an invented detail about the customer failing to reach support by phone, which is not in the conversation. |
| T08 v1 run 4 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered: the summary omits that the agent could not transfer the call to a manager. |
| T08 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered; the summary omits that the agent could not transfer the call while flagging to the duty manager. |
| T09 v1 run 2 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Includes an invented detail about the timing of the customer's monitoring (tonight) which is not supported by the conversation. |
| T09 v1 run 2 | J2 | gpt-oss | gpt-oss wrong: the claim is supported | M2 requires that the summary note the customer will check tomorrow; the summary says "will monitor tonight," so the critical timing detail is missing/incorrect. |
| T09 v1 run 2 | J4 | gpt-oss | gpt-oss wrong: the claim is supported | The next step is inaccurately described as monitoring tonight, inventing a timeline not present in the conversation. |
| T09 v1 run 4 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains an unsupported claim about a replacement already being arranged. |
| T09 v2 run 4 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | The summary omits that the agent suggested a firmware update (M2). |
| T10 v1 run 2 | J6 | gpt-oss | Rubric ambiguous: implied step or inference | States the customer profile is flagged for potential return abuse as a fact without attribution, which blames the customer. |
| T10 v2 run 0 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical fact M2 (warranty applies only if faulty) is missing from the summary. |
| T10 v2 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary includes an invented next step ('Close ticket unless customer follows up') not present in the conversation. |
| T10 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Missing warranty condition that it applies only if faulty (M2 incomplete). |
| T10 v2 run 1 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | Invents a next step ('Close ticket unless customer follows up') which was not stated in the conversation; for a resolved case no action should be added. |
| T10 v2 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered; the warranty‑only‑if‑faulty detail is missing. |
| T10 v2 run 2 | J6 | gpt-oss | Rubric ambiguous: implied step or inference | Discloses internal flag ("account flagged for 4 returns in 90 days") as a fact, which violates the must_not_include rule and internal‑note confidentiality. |
| T14 v1 run 0 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains an invented claim about the technical team investigating and following up, which is not supported by the conversation. |
| T14 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M3 is only partially covered: the summary mentions hub disconnections and firmware 2.3.1 passed to tech, but omits the critical detail that the hub disconnects "every few hours". |
| T14 v2 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 missing the 2‑day timeframe and M3 missing the "every few hours" frequency, both critical details. |
| T15 v2 run 0 | J1 | Gemini | Rubric ambiguous: implied step or inference | The summary includes an invented next step ('confirm tracking') that is not supported by the conversation. |
| T15 v2 run 0 | J4 | Gemini | Rubric ambiguous: implied step or inference | The next step includes an invented action ('confirm tracking') that was not discussed in the conversation. |
| T15 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered – the summary mentions the refund was denied due to prior use but omits that the box was opened, which is part of the required critical detail. |
| T15 v2 run 4 | J1 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a specific next step ('confirm tracking') that is not supported by the conversation text. |
| T15 v2 run 4 | J4 | Gemini | Rubric ambiguous: implied step or inference | The summary includes an invented next step ('confirm tracking') that was not discussed in the conversation. |
| T17 v1 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Summary claims the agent logged a note about the service centre delay, which is not mentioned in the conversation. |
| T17 v2 run 2 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains an unsupported claim: 'monitor swap completion' is not supported by the conversation. |
| T17 v2 run 2 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | Summary invents a next step ('monitor swap completion') that was not stated in the conversation. |
| T23 v1 run 2 | J2 | gpt-oss | Gemini too lenient: missed a real problem | M2 is only partially covered: the summary notes the unplug instruction but omits the safety instruction to keep the device away from flammable items, a critical safety detail. |
| T23 v1 run 4 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Missing the safety instruction to keep the unplugged plug away from flammable items, which is part of the critical fact M2. |
| T23 v2 run 2 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Critical fact M2 (safety flag and instruction to keep away from flammable items) is missing. |
| T28 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is missing – the summary does not state that the caller is the husband asking on behalf of his wife. M2 and M3 are present. |
| T28 v2 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical facts M1 and M2 are missing or only partially covered; the summary omits the caller's relationship (husband) and the explicit reason for refusal. |
| T28 v2 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is only partially covered; the summary does not state that the caller is the husband asking on behalf of his wife. |
| T28 v2 run 4 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 and M2 are only partially present; the summary omits that the caller is the husband and does not explicitly state the agent's refusal. |
| T29 v1 run 1 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Missing the agent's statement that they cannot promise the last 4 units by the 21st and that expediting is not guaranteed (M4). |
| T29 v2 run 2 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Critical fact M4 is incomplete: the summary does not convey that the agent cannot promise the last 4 will arrive by the 21st and that expediting is not guaranteed. |
| T29 v2 run 4 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains a claim not supported by the conversation: the customer’s request was for all 12 hubs by the 21st, not only the final 4 units by that date. |
| T30 v1 run 0 | J4 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a next step/condition ('subject to supervisor review/policy verification') that was not stated in the conversation. |
| T30 v1 run 0 | J6 | gpt-oss | Rubric ambiguous: implied step or inference | Adds speculative information about supervisor review/policy verification, which goes beyond the evidence in the conversation. |
| T30 v1 run 4 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary adds a claim about the next step (company must receive the speaker and process the double refund) which is not stated in the conversation. |
| T30 v2 run 0 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical fact M1 is missing; the summary does not convey the customer's ask. |
| T30 v2 run 0 | J3 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a current state of 'awaiting item receipt and policy escalation' which is not present in the conversation. |
| T30 v2 run 0 | J4 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a next step to 'Review unauthorized double-refund promise and process refund per company policy upon return' which was never discussed. |
| T30 v2 run 0 | J6 | Gemini | Rubric ambiguous: implied step or inference | The summary judges the agent and speculates beyond the evidence by stating the agent 'unauthorizedly' promised a double refund. |
| T30 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is only partially covered; the customer's original question is omitted. |
| T30 v2 run 1 | J6 | gpt-oss | Rubric ambiguous: implied step or inference | The summary speculates that the double‑refund promise is "unauthorized," which is not stated in the conversation. |
| T30 v2 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is missing: the summary does not mention the customer's question about a double refund or the agent's affirmative answer. |
| T30 v2 run 3 | J4 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a next step (reviewing the unauthorized promise and following up about standard policy) that was not discussed or established in the conversation. |
| T30 v2 run 3 | J6 | Gemini | Rubric ambiguous: implied step or inference | The summary judges the agent by calling their action 'unauthorized' and speculates beyond the evidence provided in the conversation. |
| T30 v2 run 4 | J4 | Gemini | Rubric ambiguous: implied step or inference | The next step provided (verifying the receipt, reviewing with a supervisor, and processing the refund) is entirely invented and not based on the conversation. |
| T32 v1 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Contains an invented claim about the customer reporting back, which is not supported by the conversation. |
| T32 v1 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Missing critical fact M2: the summary does not mention that the customer attached a screenshot and a log. |
| T32 v1 run 3 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | Includes an invented future action (customer will report back) not present in the conversation. |
| T34 v2 run 1 | J1 | Gemini | Rubric ambiguous: implied step or inference | The summary invents a next step ('Confirm customer completed the reset') that was not discussed or agreed upon in the conversation. |
| T34 v2 run 1 | J3 | gpt-oss | Rubric ambiguous: implied step or inference | The summary does not state that the case is resolved, while the expected final status is resolved. |
| T35 v1 run 0 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Contains an unsupported claim about assurance of no future support issues, which is not present in the conversation. |
| T35 v1 run 0 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical facts M1 is missing and M2 is only partially covered (refund refusal not mentioned). |
| T35 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 (customer wants the correct adapter and a personal written apology) is only partially conveyed; the summary does not explicitly state the customer's request, only the actions taken. |
| T35 v2 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered: the summary notes the correct adapter dispatch and apology but does not explicitly state the customer's request for the correct adapter (and explicitly not a refund). |
| T35 v2 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical fact M2 is only partially conveyed; the summary does not explicitly state that the customer wants the correct adapter and a personal written apology. |
| T36 v1 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | The summary does not explicitly state that the replacement for order LM-51620 has shipped (M1); it only mentions providing the tracking number. |
| T36 v1 run 3 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Contains an invented claim about no further action required, which is not supported by the conversation. |
| T36 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | Critical fact M1 (replacement shipment) is not mentioned in the summary. |
| T37 v1 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary claims the customer wants a replacement, which is not stated in the conversation. |
| T37 v2 run 0 | J1 | gpt-oss | Gemini too lenient: missed a real problem | Summary claims a replacement is approved, which is not supported; conversation only says the customer is eligible for a replacement once a photo is received. |
| T37 v2 run 0 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Critical fact M3 (eligibility vs approval) is incorrect/missing. |
| T37 v2 run 0 | J3 | gpt-oss | Gemini too lenient: missed a real problem | Summary states replacement approved, whereas the actual status is pending_customer awaiting the photo. |
| T37 v2 run 1 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M3 is only partially covered; the summary omits that eligibility is based on the previous agent's internal note. |
| T38 v1 run 0 | J4 | Gemini | Golden expectation flawed (T38 status) | Because the expected status is resolved, the summary fails by assigning a next step ('The next agent needs to process the return and issue the refund') instead of stating no action is needed. |
| T38 v1 run 1 | J4 | Gemini | Golden expectation flawed (T38 status) | The expected status is resolved, but the summary invents a next step for the next agent ('Next, process the partial return for the bulb pack and issue the ₹849 refund'). |
| T38 v1 run 3 | J4 | Gemini | Golden expectation flawed (T38 status) | Because the expected status is 'resolved', the summary fails by assigning a next step (processing the return and refund) to the next agent. |
| T38 v1 run 4 | J4 | Gemini | Golden expectation flawed (T38 status) | The expected status is resolved, but the summary invents a next step by stating 'Next, the agent needs to process the partial return and issue the ₹849 refund.' |
| T38 v2 run 0 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary includes a claim about the next step ('Process partial refund and issue bulb pack return') that was not stated in the conversation. |
| T38 v2 run 0 | J4 | gpt-oss | Golden expectation flawed (T38 status) | For a resolved case the summary invents a next step, whereas it should state no further action is needed. |
| T38 v2 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is only partially conveyed; the summary omits that the plug remains with the order. |
| T38 v2 run 3 | J3 | gpt-oss | Golden expectation flawed (T38 status) | Summary says a next step is required (process refund), which conflicts with the expected final status of 'resolved'. |
| T39 v1 run 3 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is only partially covered; the summary does not explicitly state that the customer did NOT receive the replacement hub. |
| T39 v2 run 0 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | The summary adds an invented detail about confirming "whether to honor both" the refund and hub, which is not supported by the conversation. |
| T39 v2 run 0 | J2 | gpt-oss | Gemini too lenient: missed a real problem | Critical facts M1 and M2 are missing; only M3 is present. |
| T39 v2 run 3 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | Contains an unsupported claim that the case was escalated to a supervisor, which is not directly mentioned in the conversation. |
| T40 v2 run 1 | J1 | gpt-oss | Rubric ambiguous: implied step or inference | The summary adds a next‑step suggestion "monitor delivery if needed" which was never mentioned in the conversation. |
| T40 v2 run 1 | J4 | gpt-oss | Rubric ambiguous: implied step or inference | For a resolved case the summary should state no further action; it invents a next step "monitor delivery if needed". |
| syn_01 v2 run 0 | J1 | gpt-oss | gpt-oss wrong: the claim is supported | The summary claims the case is waiting for the customer to send photos, but the customer already said "Sending now." This is not supported by the conversation. |
| syn_01 v2 run 0 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M1 is present and correct. M2 is only partially covered: the summary mentions arranging a replacement after receiving photos but does not state that the agent asked for photos or that the customer is sending them. Critical completeness therefore fails. |
| syn_01 v2 run 2 | J2 | gpt-oss | Rubric ambiguous: part of a compound fact missing | M2 is only partially covered: the summary notes waiting for photos and arranging replacement, but does not explicitly state that the agent asked for the photos. |
