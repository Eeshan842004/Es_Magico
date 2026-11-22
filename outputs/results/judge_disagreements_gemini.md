# Judge vs reference-label disagreements

11 items with at least one disagreement (of 60 labelled).

| cause | count |
|---|---|
| judge too lenient: missed a real problem | 5 |
| expectation too strict: the missing detail isn't needed by the next agent | 3 |
| expectation flawed: the case is not actually finished | 2 |
| rubric ambiguous: counted under a different criterion, or inference vs statement | 2 |
| judge too strict: harmless inference or hedge | 1 |
Each block = one item where the judge and the label differ on at least one criterion.
The cause of each disagreement is in `labels/disagreement_causes.json`. It was decided after reading each case, and no label was changed afterwards.

## H03 (heldout) conv T23 version v2: differs on J2, overall

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: My Lumo smart plug smells like burning and the casing is hot!!
AGENT: Please unplug it immediately and keep it away from flammable items.
CUSTOMER: Done. It's got a black mark on the socket.
AGENT: Thank you. This is a safety issue, so I'm escalating to our product safety team. They'll contact you today, and we'll replace the unit and collect the old one for inspection.
CUSTOMER: Ok. Please hurry, I'm worried about my wiring.
```
</details>

**Summary:** Issue: Lumo smart plug overheating with burning smell and scorch mark on socket.
Status: Customer unplugged device; concerned about home wiring.
Next step: Product safety team to contact customer today for urgent replacement and defective unit collection.

- **J2**: label=PASS, judge=FAIL. Judge reason: M2 is only partially covered; the summary omits the critical safety instruction to keep the device away from flammable items and does not explicitly state it was flagged as a safety issue.
- **overall**: label=PASS, judge=FAIL. Judge reason: (roll-up)
- Label note: No 'keep away from flammable items', but safety escalation and unplugging are there. Strict expectation.
- cause (J2): expectation too strict: the missing detail isn't needed by the next agent

## H08 (heldout) conv T38 version v1: differs on J3, J4, overall

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: I bought a plug (₹2,499) and a bulb pack (₹899) on the same order, LM-48001. I want to return the bulbs only.
AGENT: Sure. Bulb pack refund is ₹899, minus a ₹50 restocking fee, so ₹849.
CUSTOMER: Why a fee?
AGENT: It applies to opened packs under our policy.
CUSTOMER: Ok, go ahead.
```
</details>

**Summary:** The customer wants to return only the ₹899 bulb pack from order LM-48001, keeping the ₹2,499 plug. So far, the previous agent explained that a ₹50 restocking fee applies to opened packs and calculated the net refund at ₹849, which the customer agreed to. Next, process the partial return for the bulb pack and issue the ₹849 refund.

- **J3**: label=PASS, judge=FAIL. Judge reason: The summary treats the case as open and pending action by instructing the next agent to process the return, which contradicts the expected 'resolved' status.
- **J4**: label=PASS, judge=FAIL. Judge reason: The expected status is resolved, but the summary invents a next step for the next agent ('Next, process the partial return for the bulb pack and issue the ₹849 refund').
- **overall**: label=PASS, judge=FAIL. Judge reason: (roll-up)
- Label note: Next step is process refund; the case is arguably open, so the 'resolved' expectation looks wrong.
- cause (J3): expectation flawed: the case is not actually finished
- cause (J4): expectation flawed: the case is not actually finished

## H12 (heldout) conv T39 version v2: differs on J2, overall

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: I did NOT receive the replacement hub. I never asked for a refund, I asked for a replacement.
AGENT: I'm sorry for the confusion. I see a refund was issued in error. I'll arrange the replacement and reverse nothing on your side.
CUSTOMER: So I keep the refund AND get the hub?
AGENT: Let me confirm with my supervisor and come back to you tomorrow.
CUSTOMER: Fine.
```
</details>

**Summary:** Issue: Customer received an erroneous refund instead of a replacement hub.
Status: Refund issued in error; customer asked if they keep both the refund and replacement.
Next step: Confirm with supervisor whether to honor both and follow up with the customer tomorrow.

- **J2**: label=FAIL, judge=PASS. Judge reason: The summary includes all critical facts, including the erroneous refund, the customer's question about keeping both, and the next step to check with a supervisor.
- **overall**: label=FAIL, judge=PASS. Judge reason: (roll-up)
- Label note: Never says the agent will arrange the replacement (M2); the commitment is dropped.
- cause (J2): judge too lenient: missed a real problem

## H18 (heldout) conv T29 version v2: differs on J2, overall

<details><summary>conversation</summary>

```
[email]
CUSTOMER: We ordered 12 Lumo Hubs for our office, order LM-52210. Only 3 have been delivered.
AGENT: Checking. The other 9 are dispatched in two shipments: 5 arrive 20 Nov and 4 arrive 23 Nov.
CUSTOMER: We need all 12 by the 21st for an installation.
AGENT: I can't promise the last 4 by the 21st. I can ask the courier to expedite them, no guarantee.
CUSTOMER: Please do, and let me know by tomorrow noon.
```
</details>

**Summary:** Issue: Customer needs all 12 Lumo Hubs from order LM-52210 by Nov 21 for installation, but 4 arrive Nov 23.
Status: 3 delivered, 5 arriving Nov 20, 4 scheduled Nov 23.
Next step: Request courier expedite for the final 4 units and update customer by tomorrow noon.

- **J2**: label=FAIL, judge=PASS. Judge reason: All critical facts are included. M4 is partially conveyed but captures the necessary action without falsely implying a commitment, which satisfies the requirement.
- **overall**: label=FAIL, judge=PASS. Judge reason: (roll-up)
- Label note: Drops 'no guarantee' on expediting the last 4 hubs (M4).
- cause (J2): judge too lenient: missed a real problem

## H19 (heldout) conv T17 version v1: differs on J2, J5, overall

<details><summary>conversation</summary>

```
[email]
CUSTOMER: Writing about warranty claim WC-3391 for my Lumo Hub bought 14 March 2025. It stopped responding at the start of October and I posted it to your service centre on 28 Oct as instructed.
AGENT: Thanks, I see the claim. The unit failed the first check on 2 Nov.
CUSTOMER: Right, I sent it on 28 Oct. Why did it take until 2 Nov to even check? I was told 7 days for the whole process.
AGENT: The service centre had a backlog. Sorry about that.
CUSTOMER: A backlog is not my problem. I work from home and the hub runs my office lights, my heating schedule and the door sensor.
AGENT: Understood. I'll push the service centre for a faster decision.
CUSTOMER: Please do. Also, I want it on record that I called on 5 Nov and was told someone would call me back. Nobody did.
AGENT: I can see the call log, and I'm sorry no one followed up. I've added a note to your claim.
CUSTOMER: Thank you. What happens now?
AGENT: Update: the service centre confirms repair is not possible, so we will replace the unit under warranty.
CUSTOMER: Good. When do I get it? And do I have to pay anything?
AGENT: There is no charge. We need to collect the old unit first. Is a pickup on 22 Nov between 10 and 1 okay?
CUSTOMER: I'm out on the 22nd morning, I have a client meeting.
AGENT: Then 22 Nov afternoon, 2 to 5?
CUSTOMER: That works.
AGENT: Booked. The courier will bring the replacement and take the old unit in the same visit.
CUSTOMER: Great. Please make sure they bring a pickup slip, last time the courier had none and I had no proof.
AGENT: Noted, I'll add that to the booking.
CUSTOMER: One more thing. My previous hub had a custom automation setup. Will the new unit keep my automations?
AGENT: Automations are stored in your Lumo account, so they'll reappear once you log in with the new hub. You may need to re-pair your devices.
CUSTOMER: Ok, I'll allow an hour for that.
AGENT: Is there anything else I can help with?
CUSTOMER: No, that's all. Thanks for sorting this out in the end.
```
</details>

**Summary:** **What the customer wants:**
The customer is following up on a delayed warranty claim (WC-3391) for a non-responsive Lumo Hub. They wanted an update on the repair process, a formal note regarding a missed callback on 5 November, confirmation that they would not be charged for a replacement, a pickup slip upon courier collection, and confirmation that their custom automations would transfer to the new unit.

**What has been done so far:**
* The agent logged a note on the claim regarding the service centre delay and the missed 5 November callback.
* The service centre confirmed the unit cannot be repaired and approved a free warranty replacement.
* A courier swap (delivering the replacement and collecting the old unit) has been booked for 22 November between 2:00 PM and 5:00 PM, with a note added to ensure the courier provides a pickup slip.
* The agent confirmed that custom automations are saved to the customer's Lumo account, though devices will need to be re-paired.

**What happens next:**
The courier will complete the unit swap on the afternoon of 22 November and provide a pickup slip. Once the customer logs into their account on the new hub, they will re-pair their devices to restore their setup. No further action is required unless an issue arises with the delivery.

- **J2**: label=PASS, judge=FAIL. Judge reason: Critical fact M1 is only partially included because it is missing the purchase date (14 March 2025) and the date the unit was sent (28 Oct).
- **J5**: label=FAIL, judge=PASS. Judge reason: The summary is well-structured, concise, and easy for the next agent to read without unnecessary filler.
- **overall**: label=PASS, judge=FAIL. Judge reason: (roll-up)
- Label note: About 190 words that retell the whole chat; the key point is buried.
- cause (J2): expectation too strict: the missing detail isn't needed by the next agent
- cause (J5): judge too lenient: missed a real problem

## H24 (heldout) conv T07 version v2: differs on J4

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: मेरा बल्ब काम नहीं कर रहा है। दो दिन पहले ही खरीदा था।
AGENT: असुविधा के लिए खेद है। क्या आप बल्ब की फोटो भेज सकते हैं?
CUSTOMER: फोटो भेज दी है।
AGENT: धन्यवाद। हम नया बल्ब भेज रहे हैं, 4 दिन में मिल जाएगा।
```
</details>

**Summary:** Issue: Bulb purchased 2 days ago is not working.
Status: Photo verified; replacement bulb dispatched with a 4-day delivery estimate.
Next step: Monitor delivery and confirm customer receipt after 4 days.

- **J4**: label=PASS, judge=FAIL. Judge reason: The summary invents a next step ('Monitor delivery and confirm customer receipt after 4 days') that was never discussed or promised in the conversation.
- Label note: 'Photo verified': the agent only said thank you and that a bulb is being sent.
- cause (J4): judge too strict: harmless inference or hedge

## H27 (heldout) conv T29 version v1: differs on J2, overall

<details><summary>conversation</summary>

```
[email]
CUSTOMER: We ordered 12 Lumo Hubs for our office, order LM-52210. Only 3 have been delivered.
AGENT: Checking. The other 9 are dispatched in two shipments: 5 arrive 20 Nov and 4 arrive 23 Nov.
CUSTOMER: We need all 12 by the 21st for an installation.
AGENT: I can't promise the last 4 by the 21st. I can ask the courier to expedite them, no guarantee.
CUSTOMER: Please do, and let me know by tomorrow noon.
```
</details>

**Summary:** The customer ordered 12 Lumo Hubs (order LM-52210) and needs all of them delivered by November 21 for an installation, as only 3 have arrived so far. So far, the agent checked the order status and confirmed the remaining 9 units are split into two shipments arriving on November 20 (5 units) and November 23 (4 units). Next, the agent needs to contact the courier to request expedited delivery for the final 4 units and update the customer by tomorrow at noon.

- **J2**: label=FAIL, judge=PASS. Judge reason: All critical facts are included. M4 is partially included (omits the explicit 'no guarantee' phrasing), but does not miss any numbers, dates, deadlines, IDs, or commitments (it accurately states it is a 'request').
- **overall**: label=FAIL, judge=PASS. Judge reason: (roll-up)
- Label note: Drops 'cannot promise the last 4 by the 21st / no guarantee' (M4).
- cause (J2): judge too lenient: missed a real problem

## H29 (heldout) conv T37 version v2: differs on J1, overall

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: Hi, I spoke to someone yesterday about my broken lamp, order LM-49812.
AGENT: Hello, I'm Rohan, taking over from Meera. I can see Meera asked you for a photo of the base. Have you got one?
AGENT: Internal: Meera noted customer is eligible for replacement once photo received.
CUSTOMER: I haven't sent it yet.
```
</details>

**Summary:** Issue: Broken lamp on order LM-49812.
Status: Replacement approved pending photo of the lamp base; customer has not sent it yet.
Next step: Collect the base photo from the customer and process the replacement.

- **J1**: label=FAIL, judge=PASS. Judge reason: All claims in the summary are supported by the conversation. 'Replacement approved pending photo' is a reasonable paraphrase of 'eligible for replacement once photo received'.
- **overall**: label=FAIL, judge=PASS. Judge reason: (roll-up)
- Label note: 'Replacement approved' overstates the note, which says eligible once the photo arrives.
- cause (J1): rubric ambiguous: counted under a different criterion, or inference vs statement

## H38 (heldout) conv T17 version v2: differs on J2, overall

<details><summary>conversation</summary>

```
[email]
CUSTOMER: Writing about warranty claim WC-3391 for my Lumo Hub bought 14 March 2025. It stopped responding at the start of October and I posted it to your service centre on 28 Oct as instructed.
AGENT: Thanks, I see the claim. The unit failed the first check on 2 Nov.
CUSTOMER: Right, I sent it on 28 Oct. Why did it take until 2 Nov to even check? I was told 7 days for the whole process.
AGENT: The service centre had a backlog. Sorry about that.
CUSTOMER: A backlog is not my problem. I work from home and the hub runs my office lights, my heating schedule and the door sensor.
AGENT: Understood. I'll push the service centre for a faster decision.
CUSTOMER: Please do. Also, I want it on record that I called on 5 Nov and was told someone would call me back. Nobody did.
AGENT: I can see the call log, and I'm sorry no one followed up. I've added a note to your claim.
CUSTOMER: Thank you. What happens now?
AGENT: Update: the service centre confirms repair is not possible, so we will replace the unit under warranty.
CUSTOMER: Good. When do I get it? And do I have to pay anything?
AGENT: There is no charge. We need to collect the old unit first. Is a pickup on 22 Nov between 10 and 1 okay?
CUSTOMER: I'm out on the 22nd morning, I have a client meeting.
AGENT: Then 22 Nov afternoon, 2 to 5?
CUSTOMER: That works.
AGENT: Booked. The courier will bring the replacement and take the old unit in the same visit.
CUSTOMER: Great. Please make sure they bring a pickup slip, last time the courier had none and I had no proof.
AGENT: Noted, I'll add that to the booking.
CUSTOMER: One more thing. My previous hub had a custom automation setup. Will the new unit keep my automations?
AGENT: Automations are stored in your Lumo account, so they'll reappear once you log in with the new hub. You may need to re-pair your devices.
CUSTOMER: Ok, I'll allow an hour for that.
AGENT: Is there anything else I can help with?
CUSTOMER: No, that's all. Thanks for sorting this out in the end.
```
</details>

**Summary:** Issue: Unresponsive Lumo Hub under warranty claim WC-3391 (delayed service centre processing and missed callback).
Status: Free warranty replacement approved; courier swap booked for 22 Nov (2–5 PM) with pickup slip requested.
Next step: Ensure courier brings pickup slip and monitor replacement delivery/collection on 22 Nov.

- **J2**: label=PASS, judge=FAIL. Judge reason: The summary fails to include the critical purchase date (14 March 2025) and the date the unit was sent to the service centre (28 Oct) as required by M1.
- **overall**: label=PASS, judge=FAIL. Judge reason: (roll-up)
- Label note: Purchase date and 28 Oct omitted; not needed by the next agent, strict expectation.
- cause (J2): expectation too strict: the missing detail isn't needed by the next agent

## H42 (heldout) conv T30 version v2: differs on J6

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: If I return the speaker will you refund me double for the trouble?
AGENT: Yes, absolutely, we'll refund double.
CUSTOMER: Great, return initiated then.
AGENT: Great, I'll note it down.
```
</details>

**Summary:** Issue: Customer returning speaker; previous agent promised a double refund.
Status: Return initiated; unauthorized 200% refund commitment made.
Next step: Verify return receipt, review unauthorized double-refund promise with supervisor/policy, and process appropriate refund.

- **J6**: label=FAIL, judge=PASS. Judge reason: The summary is professional and does not contain any insults, profanity, or unsafe content.
- Label note: 'Unauthorized 200% refund' and a supervisor review were never said; it also judges the agent.
- cause (J6): judge too lenient: missed a real problem

## H52 (heldout) conv T32 version v2: differs on J1

<details><summary>conversation</summary>

```
[chat]
CUSTOMER: The hub is not connecting, here's a screenshot: screenshot_2291.png and the app log log_20251118.txt
AGENT: I can't open attachments in this chat. Could you describe the error?
CUSTOMER: It says 'Error 4012 device unreachable'.
AGENT: That error means the hub lost its connection. Please restart your router and try again.
CUSTOMER: Will try now.
```
</details>

**Summary:** Issue: Hub offline with "Error 4012 device unreachable" (`screenshot_2291.png`, `log_20251118.txt`).
Status: Customer restarting router to test reconnection.
Next step: Confirm reconnection; request attachments if unresolved.

- **J1**: label=PASS, judge=FAIL. Judge reason: The summary invents a next step ('request attachments if unresolved') that is not supported by the conversation.
- Label note: Doesn't say the agent could not open the attachments; 'request attachments' is a made-up step.
- cause (J1): rubric ambiguous: counted under a different criterion, or inference vs statement
