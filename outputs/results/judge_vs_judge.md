# Judge vs judge: gemini-3-pro vs gpt-oss-120b (same rubric)

180 summaries judged by both. Kappa with 95% bootstrap CI (2000 resamples). FAIL = 1.

| criterion    |   n |   gemini_fail |   gptoss_fail |   raw_agree_pct |   kappa | ci            |   both_fail |   only_gemini |   only_gptoss |
|:-------------|----:|--------------:|--------------:|----------------:|--------:|:--------------|------------:|--------------:|--------------:|
| J1           | 180 |            18 |            42 |            83.3 |    0.42 | [0.25, 0.59]  |          15 |             3 |            27 |
| J2           | 180 |            22 |            62 |            77.8 |    0.42 | [0.29, 0.55]  |          22 |             0 |            40 |
| J3           | 180 |             5 |             7 |            97.8 |    0.66 | [0.23, 0.93]  |           4 |             1 |             3 |
| J4           | 180 |            23 |            23 |            88.9 |    0.5  | [0.29, 0.68]  |          13 |            10 |            10 |
| J5           | 180 |             0 |             5 |            97.2 |    0    | [0.00, 0.00]  |           0 |             0 |             5 |
| J6           | 180 |             2 |             9 |            93.9 |   -0.02 | [-0.04, 0.00] |           0 |             2 |             9 |
| overall_fail | 180 |            42 |            95 |            68.3 |    0.38 | [0.28, 0.49]  |          40 |             2 |            55 |

## By version (does either judge treat one version differently?)

| version   |   n |   gemini_overall_fail |   gptoss_overall_fail |   kappa_overall |
|:----------|----:|----------------------:|----------------------:|----------------:|
| v1        |  85 |                 0.141 |                 0.4   |            0.34 |
| v2        |  95 |                 0.316 |                 0.642 |            0.37 |

## Every disagreement on a blocking criterion (J1-J4, J6)

### T03 v1 s1: J1
Summary: 'Customer Priya Nair wants a phone call regarding a broken bulb and provided her phone number (+91 98765 43210) and email (priya.nair@example.com). No troubleshooting has been done yet, as the agent agreed to arrange a callback. Next, an agent needs to call Priya tomorrow between 11:00 and 1:00, which she confirmed works for her.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Includes an invented claim that no troubleshooting has been done yet, which is not supported by the conversation.)

### T03 v1 s2: J1
Summary: 'Customer Priya Nair wants a phone call to discuss her broken bulb and provided her phone number (+91 98765 43210) and email (priya.nair@example.com). The agent agreed to arrange a callback for tomorrow between 11:00 AM and 1:00 PM. Next, the support team needs to call Priya at +91 98765 43210 tomorrow after 11:00 AM (before 1:00 PM) to resolve the broken bulb issue.'
- J1: gemini=PASS (All claims in the summary, including the customer's issue, contact details, and the scheduled callback time, are fully supported by the conversation.) | gpt-oss=FAIL (Contains an invented claim about the purpose of the call (to resolve the broken bulb issue) not supported by the conversation.)

### T04 v1 s0: J6
Summary: 'The customer requested to change the delivery address for order LM-50177 prior to shipment. The previous agent updated the address to Flat 14B, Seaview Heights, 3rd Cross Road, Indiranagar, Bengaluru 560038, and confirmed there was no extra charge since the order is still in packing. No further action is needed unless the customer follows up.'
- J6: gemini=PASS (The tone is neutral and professional, with no safety issues.) | gpt-oss=FAIL (The summary includes the full delivery address, which is personal identifying information and should not be disclosed.)

### T07 v1 s4: J4
Summary: 'The customer reported that a bulb purchased two days ago is not working. The agent asked for a photo of the bulb, which the customer provided. Next, a replacement bulb will be dispatched and is expected to arrive within four days.'
- J4: gemini=PASS (The summary clearly states the next step: a replacement bulb will be dispatched and arrive in four days.) | gpt-oss=FAIL (The summary does not specify a clear actionable next step or who is responsible (e.g., monitor delivery, follow‑up).)

### T08 v1 s0: J2
Summary: 'The customer wants to speak directly with a manager because their smart plug (Order LM-47720) damaged their extension board and their previous calls went unanswered. So far, the agent collected the order number, offered a ₹500 apology coupon (which the customer declined), and flagged the issue for the duty manager. Next, the duty manager needs to call the customer within 24 hours.'
- J2: gemini=PASS (All critical facts (M1 and M2) are accurately conveyed in the summary.) | gpt-oss=FAIL (Missing critical detail that the agent could not transfer the call (M2). The summary mentions the manager flag but omits the inability to transfer.)

### T08 v1 s1: J2
Summary: 'The customer reported that a smart plug from order LM-47720 damaged their extension board and requested to speak with a manager immediately after failing to reach support by phone. The previous agent collected the order number, flagged the case for the duty manager, and offered a ₹500 coupon, which the customer declined. Next, the duty manager needs to call the customer within 24 hours to address the complaint.'
- J2: gemini=PASS (All critical facts (M1 and M2) are accurately included in the summary.) | gpt-oss=FAIL (Missing the critical detail that the agent could not transfer the call (M2).)

### T08 v1 s4: J1, J2
Summary: 'The customer reported that a smart plug from order LM-47720 damaged their extension board and requested to speak with a manager immediately after failing to reach support by phone. The previous agent collected the order number, flagged the case for a duty manager callback, and offered a ₹500 apology coupon, which the customer declined. Next, the duty manager needs to call the customer within 24 hours to resolve the issue.'
- J1: gemini=PASS (Every claim in the summary is fully supported by the conversation, including the order number, the damage, the failed calls, the coupon offer, and the customer's refusal.) | gpt-oss=FAIL (Contains an invented detail about the customer failing to reach support by phone, which is not in the conversation.)
- J2: gemini=PASS (All critical facts (M1 and M2) are fully conveyed with correct details, including the order number, the damage, and the 24-hour callback timeframe.) | gpt-oss=FAIL (M2 is only partially covered: the summary omits that the agent could not transfer the call to a manager.)

### T09 v1 s2: J1, J2, J4
Summary: 'The customer is reporting that their smart plug (Order LM-51310) unexpectedly turns off around 2:00 AM every night. So far, the agent confirmed there are no active schedules set in the app and instructed the customer to run a firmware update. Next, the customer is completing the firmware update and will monitor the plug tonight to see if the issue persists, with a replacement planned if it does not resolve the problem.'
- J1: gemini=PASS (All claims in the summary are directly supported by the conversation.) | gpt-oss=FAIL (Includes an invented detail about the timing of the customer's monitoring (tonight) which is not supported by the conversation.)
- J2: gemini=PASS (The summary includes all critical facts, including the order number, the specific issue, the lack of schedules, the firmware update, and the potential replacement.) | gpt-oss=FAIL (M2 requires that the summary note the customer will check tomorrow; the summary says "will monitor tonight," so the critical timing detail is missing/incorrect.)
- J4: gemini=PASS (The next step is clearly stated: the customer will monitor the plug tonight, and a replacement is planned if the issue persists.) | gpt-oss=FAIL (The next step is inaccurately described as monitoring tonight, inventing a timeline not present in the conversation.)

### T09 v1 s4: J1
Summary: 'The customer contacted support regarding a smart plug (Order LM-51310) that unexpectedly turns off around 2:00 AM without any active schedules. The agent ruled out app scheduling and instructed the customer to run a firmware update, which the customer is currently installing. Next, the customer will monitor the plug overnight and follow up tomorrow, with a replacement arranged if the issue continues.'
- J1: gemini=PASS (All claims in the summary are fully supported by the conversation.) | gpt-oss=FAIL (Contains an unsupported claim about a replacement already being arranged.)

### T10 v1 s2: J6
Summary: "**Summary:**\n\n* **Customer's request:** The customer wanted to return their hub because they do not like it, though it is 5 weeks old and not faulty.\n* **What has been done:** The agent informed the customer that the 30-day return window has passed and denied the return, which the customer reluctantly accepted. \n* **Next steps:** No further action is required; the case can be closed. (Note: Customer profile is flagged for potential return abuse)."
- J6: gemini=PASS (The summary maintains a professional tone. It includes a neutral, attributed mention of the internal flag for potential return abuse, which is acceptable and does not state it as a factual accusation.) | gpt-oss=FAIL (States the customer profile is flagged for potential return abuse as a fact without attribution, which blames the customer.)

### T14 v1 s0: J1
Summary: "The customer requested a corrected invoice for LM-46002 due to an incorrect GST amount, the cancellation of their Lumo Care subscription, and help with a bedroom hub that frequently disconnects. \n\nSo far, the agent has cancelled the Lumo Care subscription effective 30 November, requested an updated invoice from the finance team, and collected the hub's firmware version (2.3.1) to pass to the technical team. \n\nNext, finance needs to reissue the corrected invoice within two days, and the technical team needs to investigate the hub's disconnection issue and follow up with the customer."
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains an invented claim about the technical team investigating and following up, which is not supported by the conversation.)

### T17 v1 s1: J1
Summary: "**What the customer wants:**\nThe customer is following up on a delayed warranty claim (WC-3391) for a non-responsive Lumo Hub. They wanted an update on the repair process, a formal note regarding a missed callback on 5 November, confirmation that they would not be charged for a replacement, a pickup slip upon courier collection, and confirmation that their custom automations would transfer to the new unit.\n\n**What has been done so far:**\n* The agent logged a note on the claim regarding the service centre delay and the missed 5 November callback.\n* The service centre confirmed the unit cannot be repaired and approved a free warranty replacement.\n* A courier swap (delivering the replacement and collecting the old unit) has been booked for 22 November between 2:00 PM and 5:00 PM, with a note added to ensure the courier provides a pickup slip.\n* The agent confirmed that custom automations are saved to the customer's Lumo account, though devices will need to be re-paired.\n\n**What happens next:**\nThe courier will complete the unit swap on the afternoon of 22 November and provide a pickup slip. Once the customer logs into their account on the new hub, they will re-pair their devices to restore their setup. No further action is required unless an issue arises with the delivery."
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Summary claims the agent logged a note about the service centre delay, which is not mentioned in the conversation.)

### T23 v1 s2: J2
Summary: 'The customer is reporting a safety issue where their Lumo smart plug smells like burning, has a hot casing, and left a black mark on the socket. They want urgent assistance due to concerns about their wiring. \n\nSo far, the previous agent instructed the customer to unplug the device immediately, which the customer has done, and escalated the case to the product safety team. \n\nNext, the product safety team needs to contact the customer today to arrange a replacement unit and retrieve the damaged plug for inspection.'
- J2: gemini=PASS (All critical facts are included. M2 is partially missing the instruction about flammable items, but this omission is not a number, date, deadline, ID, commitment, or the safety nature of the hazard (which is clearly stat) | gpt-oss=FAIL (M2 is only partially covered: the summary notes the unplug instruction but omits the safety instruction to keep the device away from flammable items, a critical safety detail.)

### T23 v1 s4: J2
Summary: "The customer reported a burning smell, hot casing, and a black mark on the socket of their Lumo smart plug, and they want urgent help due to concerns about their wiring. So far, the customer has unplugged the device per the agent's safety instructions, and the case has been escalated to the product safety team. Next, the product safety team will contact the customer today to arrange a replacement and collect the damaged plug for inspection."
- J2: gemini=PASS (All critical facts are included. M2 is partially included but the missing detail (flammable items) does not violate the failure criteria for partial critical facts.) | gpt-oss=FAIL (Missing the safety instruction to keep the unplugged plug away from flammable items, which is part of the critical fact M2.)

### T29 v1 s1: J2
Summary: 'The customer ordered 12 Lumo Hubs (order LM-52210) and needs all of them delivered by November 21 for an installation, as only 3 have arrived so far. So far, the agent checked the order status and confirmed the remaining 9 units are split into two shipments arriving on November 20 (5 units) and November 23 (4 units). Next, the agent needs to contact the courier to request expedited delivery for the final 4 units and update the customer by tomorrow at noon.'
- J2: gemini=PASS (All critical facts are included. M4 is partially included (omits the explicit 'no guarantee' phrasing), but does not miss any numbers, dates, deadlines, IDs, or commitments (it accurately states it is a 'request').) | gpt-oss=FAIL (Missing the agent's statement that they cannot promise the last 4 units by the 21st and that expediting is not guaranteed (M4).)

### T30 v1 s0: J4, J6
Summary: 'The customer wants a double refund in exchange for returning a speaker. So far, the previous agent agreed to the double refund, and the customer has initiated the return. Next, the customer needs to complete the return of the speaker, after which the promised double refund will need to be processed (subject to supervisor review/policy verification, as a double refund is an unusual exception).'
- J4: gemini=FAIL (The summary invents a next step/condition ('subject to supervisor review/policy verification') that was not stated in the conversation.) | gpt-oss=PASS (Specifies that the customer must complete the return of the speaker before the refund can be processed.)
- J6: gemini=PASS (The tone is neutral and professional. It does not contain any unsafe content or inappropriate judgments.) | gpt-oss=FAIL (Adds speculative information about supervisor review/policy verification, which goes beyond the evidence in the conversation.)

### T30 v1 s4: J1
Summary: 'The customer wants to return a speaker and receive a double refund for the trouble. So far, the previous agent agreed to the double refund and noted down that the customer has initiated the return. Next, the company needs to receive the returned speaker and process the double refund.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation, including the agent's agreement to a double refund and the customer initiating the return.) | gpt-oss=FAIL (The summary adds a claim about the next step (company must receive the speaker and process the double refund) which is not stated in the conversation.)

### T32 v1 s1: J1
Summary: 'The customer needs help connecting their hub, which is displaying "Error 4012 device unreachable." So far, the agent explained they could not view the customer\'s attached screenshot or app log, identified the error code as a lost connection, and advised restarting the router. Next, the customer is going to restart their router and report back on whether the connection is restored.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains an invented claim about the customer reporting back, which is not supported by the conversation.)

### T32 v1 s2: J2
Summary: 'The customer wants help fixing a hub that will not connect. So far, the agent asked for a description of the error because attachments cannot be opened in the chat, identified the reported "Error 4012 device unreachable" as a lost connection, and advised restarting the router. Next, the customer is going to restart their router and report back on whether it resolves the issue.'
- J2: gemini=PASS (All critical facts are included. M2 is partially included (mentions attachments but not specifically the screenshot and log), but the missing details are not numbers, dates, IDs, or safety hazards, so it passes.) | gpt-oss=FAIL (Missing critical fact M2: the summary does not mention that the customer attached a screenshot and a log.)

### T32 v1 s3: J1
Summary: 'The customer wants help getting their hub to connect after seeing "Error 4012 device unreachable." So far, the agent noted they could not open the customer\'s attached screenshot and log file, identified the error as a lost connection, and instructed the customer to restart their router. Next, the customer is restarting their router and will report back on whether the hub reconnects.'
- J1: gemini=PASS (All claims in the summary are fully supported by the conversation.) | gpt-oss=FAIL (Includes an invented future action (customer will report back) not present in the conversation.)

### T35 v1 s0: J1, J2
Summary: "The customer wants the correct power adapter for their replacement hub (order LM-46855), assurance that they will not experience similar support issues again, and a personalized written apology. \n\nSo far, the previous agent has apologized, dispatched the correct adapter (tracking LMT-5521-014-IN), and added a history note to the customer's account to prevent them from having to repeat their story. \n\nNext, the previous agent needs to send the promised personalized written apology via email."
- J1: gemini=PASS (All claims in the summary are fully supported by the conversation.) | gpt-oss=FAIL (Contains an unsupported claim about assurance of no future support issues, which is not present in the conversation.)
- J2: gemini=PASS (All critical facts are included. M1 is partial as it omits the specific detail about the US-style adapter, but the missing information is not a number, date, deadline, ID, commitment, or safety hazard, so it does not fai) | gpt-oss=FAIL (Critical facts M1 is missing and M2 is only partially covered (refund refusal not mentioned).)

### T36 v1 s1: J2
Summary: 'The customer wanted the tracking number for their replacement unit. The agent provided the tracking number (LMT-7782-991-IN) for order LM-51620 and confirmed it will arrive in three days. No further action is needed unless the customer has delivery issues.'
- J2: gemini=PASS (All critical facts (M1, M2) are included accurately.) | gpt-oss=FAIL (The summary does not explicitly state that the replacement for order LM-51620 has shipped (M1); it only mentions providing the tracking number.)

### T36 v1 s3: J1
Summary: 'The customer asked for the tracking number for their shipped replacement unit. The agent confirmed that the replacement for order LM-51620 shipped today via tracking number LMT-7782-991-IN with an expected delivery in 3 days. No further action is required unless the customer reaches back out regarding delivery.'
- J1: gemini=PASS (All claims in the summary are directly supported by the conversation.) | gpt-oss=FAIL (Contains an invented claim about no further action required, which is not supported by the conversation.)

### T37 v1 s1: J1
Summary: "The customer wants a replacement for a broken lamp from order LM-49812. So far, Meera asked for a photo of the lamp's base and noted the customer is eligible for a replacement once the photo is received, and Rohan took over the chat and confirmed the photo has not been sent yet. Next, the customer needs to send the photo of the base so the replacement can be processed."
- J1: gemini=PASS (All claims in the summary are supported by the conversation, including the order number, the request for a photo, the internal note about replacement eligibility, and the fact that the photo has not been sent yet.) | gpt-oss=FAIL (The summary claims the customer wants a replacement, which is not stated in the conversation.)

### T38 v1 s0: J4
Summary: 'The customer wants to return only the bulb pack from order LM-48001. The agent explained that a ₹50 restocking fee applies to opened packs, making the total refund ₹849, and the customer agreed to proceed. The next agent needs to process the return and issue the refund.'
- J4: gemini=FAIL (Because the expected status is resolved, the summary fails by assigning a next step ('The next agent needs to process the return and issue the refund') instead of stating no action is needed.) | gpt-oss=PASS (The summary clearly states the next action: process the return and issue the refund.)

### T38 v1 s1: J4
Summary: 'The customer wants to return only the ₹899 bulb pack from order LM-48001, keeping the ₹2,499 plug. So far, the previous agent explained that a ₹50 restocking fee applies to opened packs and calculated the net refund at ₹849, which the customer agreed to. Next, process the partial return for the bulb pack and issue the ₹849 refund.'
- J4: gemini=FAIL (The expected status is resolved, but the summary invents a next step for the next agent ('Next, process the partial return for the bulb pack and issue the ₹849 refund').) | gpt-oss=PASS (Provides a clear, actionable next step: process the partial return and issue the ₹849 refund.)

### T38 v1 s3: J4
Summary: 'The customer wants to return only the bulb pack (₹899) from order LM-48001, keeping the plug (₹2,499). So far, the agent explained that a ₹50 restocking fee applies to opened packs under company policy, bringing the total refund to ₹849, and the customer agreed to proceed. Next, the agent needs to process the partial return and issue the ₹849 refund.'
- J4: gemini=FAIL (Because the expected status is 'resolved', the summary fails by assigning a next step (processing the return and refund) to the next agent.) | gpt-oss=PASS (The summary clearly specifies the next action: process the partial return and issue the ₹849 refund.)

### T38 v1 s4: J4
Summary: 'The customer wants to return only the bulb pack (₹899) from order LM-48001. So far, the agent explained that a ₹50 restocking fee applies to opened packs, bringing the refund to ₹849, and the customer agreed to proceed. Next, the agent needs to process the partial return and issue the ₹849 refund.'
- J4: gemini=FAIL (The expected status is resolved, but the summary invents a next step by stating 'Next, the agent needs to process the partial return and issue the ₹849 refund.') | gpt-oss=PASS (Clearly states the next agent must process the partial return and issue the ₹849 refund.)

### T39 v1 s3: J2
Summary: 'The customer wants a replacement hub, which they had previously requested, rather than the refund that was issued in error. So far, the previous agent acknowledged the mistake and offered to arrange the replacement without reversing the refund, though the customer questioned whether they would keep both. Next, the previous agent needs to confirm with a supervisor whether the customer can retain the refund alongside the replacement and follow up with the customer tomorrow.'
- J2: gemini=PASS (All critical facts are included or partially included without missing any mandatory specific details like dates or commitments.) | gpt-oss=FAIL (M1 is only partially covered; the summary does not explicitly state that the customer did NOT receive the replacement hub.)

### T03 v2 s2: J6
Summary: 'Issue: Broken bulb; customer Priya Nair requested a phone callback.\nStatus: Callback window confirmed for tomorrow after 11:00 AM (11:00 AM–1:00 PM).\nNext step: Call Priya Nair at +91 98765 43210 (backup email: priya.nair@example.com) tomorrow between 11:00 AM and 1:00 PM.'
- J6: gemini=PASS (The tone is neutral and professional, with no safety issues or inappropriate content.) | gpt-oss=FAIL (The summary includes the customer's phone number and email address, which are PII and should not be disclosed.)

### T03 v2 s4: J6
Summary: 'Issue: Customer requested phone support for a broken bulb.\nStatus: Callback agreed for tomorrow between 11:00 AM and 1:00 PM.\nNext step: Call Priya at +91 98765 43210 tomorrow between 11 and 1.'
- J6: gemini=PASS (The tone is neutral and professional. (Note: PII inclusion is ignored as per instructions).) | gpt-oss=FAIL (Includes the customer's phone number, which is prohibited PII per the must_not_include list.)

### T04 v2 s0: J1, J4, J6
Summary: 'Issue: Delivery address change requested for order LM-50177 before shipment.\nStatus: Updated to Flat 14B, Seaview Heights, 3rd Cross Road, Indiranagar, Bengaluru 560038 with no extra charge (still in packing).\nNext step: None; confirm shipment proceeds to the updated address.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Includes an invented next‑step claim not supported by the dialogue.)
- J4: gemini=PASS (The summary correctly identifies that no further action is needed.) | gpt-oss=FAIL (Invents a next step (confirm shipment) despite the case being resolved; no next step was stated.)
- J6: gemini=PASS (The tone is neutral and professional. (Note: PII inclusion is ignored per instructions).) | gpt-oss=FAIL (Exposes full customer address (PII), violating safety/privacy expectations.)

### T04 v2 s1: J1, J4, J6
Summary: 'Issue: Delivery address change requested for order LM-50177 before shipment.\nStatus: Updated to Flat 14B, Seaview Heights, 3rd Cross Road, Indiranagar, Bengaluru 560038 with no extra charge (still in packing).\nNext step: None; ready for dispatch.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains an invented claim that the order is ready for dispatch, which is not supported by the conversation.)
- J4: gemini=PASS (The summary correctly states that no further action is needed.) | gpt-oss=FAIL (The summary invents a next step ('ready for dispatch') that was not mentioned; for a resolved case it should state no action needed without adding new information.)
- J6: gemini=PASS (The summary is neutral and objective. (Note: PII inclusion is ignored as per instructions).) | gpt-oss=FAIL (The summary includes the full delivery address, exposing personal data that should not be shared.)

### T05 v2 s1: J2
Summary: 'Issue: Duplicate ₹1,299 charge on 12 Nov (card ending 4417).\nStatus: Reversal raised (Ref: RV-220918); credits in 3–5 working days.\nNext step: Follow up to confirm refund by 20 Nov before customer initiates a bank dispute.'
- J2: gemini=PASS (All critical facts are accurately included in the summary.) | gpt-oss=FAIL (M2 is only partially covered – the summary mentions the reversal reference but does not explicitly state that the agent confirmed the duplicate charge.)

### T05 v2 s3: J1, J2, J4
Summary: 'Issue: Duplicate charge of ₹1,299 on 12 Nov (card ending 4417).\nStatus: Reversal raised with payment partner (Ref: RV-220918); 3–5 working day turnaround.\nNext step: Follow up on 20 Nov to confirm refund and prevent a bank dispute.'
- J1: gemini=PASS (All claims in the summary, including the deadline for the bank dispute, are supported by the conversation.) | gpt-oss=FAIL (The summary adds a next step (follow up on 20 Nov) that was not mentioned in the conversation.)
- J2: gemini=PASS (All critical facts are present and accurate.) | gpt-oss=FAIL (Missing or partial critical facts: M2 lacks explicit agent confirmation of duplicate charge (only reversal mentioned), M4 does not state the customer's intent to dispute if not refunded by the 20th.)
- J4: gemini=PASS (The summary provides a clear and actionable next step to follow up on November 20th to prevent the customer's threatened dispute.) | gpt-oss=FAIL (The next step is invented and not supported by the conversation; no actionable step was defined.)

### T06 v2 s0: J1, J4
Summary: 'Issue: Order LM-49055 delayed 8 days; customer disputes two missed delivery attempts.\nStatus: Replacement dispatched with a 3-day delivery ETA.\nNext step: Monitor replacement delivery and confirm receipt if customer follows up.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Summary adds a next step that was not mentioned in the conversation, constituting an invented claim.)
- J4: gemini=PASS (The next step provides clear, actionable guidance for the next agent to monitor the delivery.) | gpt-oss=FAIL (Next step is invented and not derived from the conversation; also vague about who should act.)

### T06 v2 s3: J1
Summary: 'Issue: Order LM-49055 delayed 8 days; customer disputes failed delivery attempts and requested a replacement.\nStatus: Replacement dispatched with a 3-day delivery estimate.\nNext step: Monitor replacement delivery in 3 days; no immediate action required.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (The summary adds a next‑step claim that is not mentioned in the conversation.)

### T08 v2 s1: J2
Summary: "Issue: Smart plug (Order LM-47720) damaged customer's extension board; customer is angry over unanswered calls.\nStatus: Escalated to duty manager; customer declined ₹500 apology coupon.\nNext step: Duty manager to call customer within 24 hours."
- J2: gemini=PASS (All critical facts (M1 and M2) are accurately conveyed in the summary.) | gpt-oss=FAIL (M2 is only partially covered; the summary omits that the agent could not transfer the call while flagging to the duty manager.)

### T09 v2 s4: J2
Summary: 'Issue: Smart plug (Order LM-51310) randomly turns off around 2 AM with no schedules set.\nStatus: Customer is updating firmware now.\nNext step: Follow up tomorrow; send a replacement if the issue persists.'
- J2: gemini=PASS (All critical facts are included accurately.) | gpt-oss=FAIL (The summary omits that the agent suggested a firmware update (M2).)

### T10 v2 s0: J2
Summary: 'Issue: Customer requested a return on a non-faulty 5-week-old hub (outside the 30-day window).\nStatus: Return denied; customer accepted the outcome. Note: Account flagged for 4 returns in 90 days (do not disclose).\nNext step: Close ticket; no further action required.'
- J2: gemini=PASS (The summary includes all critical facts. It partially covers M2 by omitting the warranty detail, but since the missing part is not a number, date, deadline, ID, commitment, or safety hazard, it still passes.) | gpt-oss=FAIL (Critical fact M2 (warranty applies only if faulty) is missing from the summary.)

### T10 v2 s1: J1, J2, J4
Summary: 'Issue: Customer requested a return on a non-faulty 5-week-old hub.\nStatus: Return denied (outside 30-day window); account flagged for possible return abuse (4 returns in 90 days—do not disclose). Customer accepted outcome.\nNext step: Close ticket unless customer follows up.'
- J1: gemini=PASS (All claims in the summary, including the internal note about the account flag, are supported by the conversation.) | gpt-oss=FAIL (The summary includes an invented next step ('Close ticket unless customer follows up') not present in the conversation.)
- J2: gemini=PASS (All critical facts are included. M2 is partially included (missing the warranty detail), but the missing information is not a number, date, deadline, ID, commitment, or safety hazard, so it passes.) | gpt-oss=FAIL (Missing warranty condition that it applies only if faulty (M2 incomplete).)
- J4: gemini=PASS (The case is resolved, and the summary correctly states to close the ticket without inventing unnecessary actions.) | gpt-oss=FAIL (Invents a next step ('Close ticket unless customer follows up') which was not stated in the conversation; for a resolved case no action should be added.)

### T10 v2 s2: J2, J6
Summary: 'Issue: Customer wants to return a working 5-week-old hub.\nStatus: Return declined (past 30-day window; account flagged for 4 returns in 90 days). Customer accepted.\nNext step: None; close ticket unless customer replies.'
- J2: gemini=PASS (M1 is fully present. M2 is partially present (omits the warranty detail), but the missing information is not a number, date, deadline, ID, commitment, or safety hazard, so it does not cause a failure.) | gpt-oss=FAIL (M2 is only partially covered; the warranty‑only‑if‑faulty detail is missing.)
- J6: gemini=PASS (The summary neutrally reports the internal flag without accusing the customer of abuse as a fact, adhering to tone and safety guidelines.) | gpt-oss=FAIL (Discloses internal flag ("account flagged for 4 returns in 90 days") as a fact, which violates the must_not_include rule and internal‑note confidentiality.)

### T14 v2 s1: J2
Summary: 'Issue: Incorrect GST on LM-46002, Lumo Care cancellation, and bedroom hub disconnections (firmware 2.3.1).\nStatus: Lumo Care cancelled effective 30 Nov; invoice reissue requested from finance; firmware escalated to tech team.\nNext step: Send reissued invoice within 2 days and follow up on hub disconnection fix.'
- J2: gemini=PASS (All critical facts are included accurately.) | gpt-oss=FAIL (M3 is only partially covered: the summary mentions hub disconnections and firmware 2.3.1 passed to tech, but omits the critical detail that the hub disconnects "every few hours".)

### T14 v2 s2: J2
Summary: 'Issue: Wrong GST on invoice LM-46002, Lumo Care cancellation request, and bedroom hub disconnecting on firmware 2.3.1.\nStatus: Lumo Care cancelled effective 30 Nov; invoice reissue requested from finance; firmware 2.3.1 sent to tech team.\nNext step: Confirm finance sends corrected invoice within 2 days and follow up on tech team hub fix.'
- J2: gemini=PASS (All critical must-include facts are present and accurate in the summary.) | gpt-oss=FAIL (M1 missing the 2‑day timeframe and M3 missing the "every few hours" frequency, both critical details.)

### T15 v2 s0: J1, J4
Summary: 'Issue: Cracked speaker cover on LM-48870; refund reversed due to used-item policy, replacement cover offered.\nStatus: Customer accepted replacement cover but remains upset over refund mix-up.\nNext step: Ship free replacement cover and confirm tracking.'
- J1: gemini=FAIL (The summary includes an invented next step ('confirm tracking') that is not supported by the conversation.) | gpt-oss=PASS (All statements in the summary are directly supported by the conversation.)
- J4: gemini=FAIL (The next step includes an invented action ('confirm tracking') that was not discussed in the conversation.) | gpt-oss=PASS (Specifies shipping the free replacement cover and confirming tracking, which is clear and actionable.)

### T15 v2 s1: J2
Summary: 'Issue: Cracked speaker cover on Order LM-48870; agent mistakenly approved a ₹3,499 refund before denying it due to prior use.\nStatus: Customer reluctantly accepted a free replacement cover instead.\nNext step: Process and ship the free replacement cover for Order LM-48870.'
- J2: gemini=PASS (The summary successfully includes all critical facts, including the order number, the initial refund approval and retraction, and the final agreement for a replacement cover.) | gpt-oss=FAIL (M2 is only partially covered – the summary mentions the refund was denied due to prior use but omits that the box was opened, which is part of the required critical detail.)

### T15 v2 s4: J1, J4
Summary: 'Issue: Damaged speaker cover on order LM-48870; customer upset after ₹3,499 refund was mistakenly approved and revoked.\nStatus: Customer agreed to a free replacement cover instead.\nNext step: Ship replacement cover for order LM-48870 and confirm tracking.'
- J1: gemini=FAIL (The summary invents a specific next step ('confirm tracking') that is not supported by the conversation text.) | gpt-oss=PASS (All statements in the summary are supported by the conversation; no invented facts.)
- J4: gemini=FAIL (The summary includes an invented next step ('confirm tracking') that was not discussed in the conversation.) | gpt-oss=PASS (Provides a clear, actionable next step: ship the replacement cover and confirm tracking.)

### T17 v2 s2: J1, J4
Summary: 'Issue: Unrepairable Lumo Hub (WC-3391) after delayed service/missed callback.\nStatus: Free warranty replacement swap booked for 22 Nov, 2–5 PM.\nNext step: Ensure courier brings a pickup slip and monitor swap completion.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains an unsupported claim: 'monitor swap completion' is not supported by the conversation.)
- J4: gemini=PASS (The summary provides clear, actionable next steps regarding the pickup slip and monitoring the swap.) | gpt-oss=FAIL (Summary invents a next step ('monitor swap completion') that was not stated in the conversation.)

### T23 v2 s2: J2
Summary: 'Issue: Lumo smart plug overheated, smelled like burning, and left a black mark on socket.\nStatus: Unplugged; escalated to product safety for same-day contact, replacement, and unit collection.\nNext step: Product safety team to contact customer urgently and arrange inspection/replacement.'
- J2: gemini=PASS (All critical facts are present or partially present. The missing part of M2 (the instruction to keep the device away from flammable items) is a past instruction rather than a number, date, deadline, ID, commitment, or th) | gpt-oss=FAIL (Critical fact M2 (safety flag and instruction to keep away from flammable items) is missing.)

### T28 v2 s1: J2
Summary: 'Issue: Third-party inquiry regarding unreceived order LM-49344 (status and delivery address).\nStatus: Declined to share details due to privacy policy; requested account holder reach out directly.\nNext step: Verify account holder identity if she contacts support via registered email or phone.'
- J2: gemini=PASS (The summary successfully includes all critical facts, noting the third-party inquiry for the order, the refusal due to privacy, and the requirement for the account holder to contact support directly.) | gpt-oss=FAIL (M1 is missing – the summary does not state that the caller is the husband asking on behalf of his wife. M2 and M3 are present.)

### T28 v2 s2: J2
Summary: 'Issue: Non-account holder requested status and delivery address for order LM-49344.\nStatus: Unverified; order details withheld per privacy policy.\nNext step: Assist account holder with LM-49344 once she contacts support via her registered email or phone.'
- J2: gemini=PASS (All critical facts are included and correct.) | gpt-oss=FAIL (Critical facts M1 and M2 are missing or only partially covered; the summary omits the caller's relationship (husband) and the explicit reason for refusal.)

### T28 v2 s3: J2
Summary: 'Issue: Third party requested delivery status and address for order LM-49344.\nStatus: Unresolved; declined to disclose details due to privacy policy.\nNext step: Await outreach from the account holder via registered email or phone.'
- J2: gemini=PASS (All critical facts are included and correct.) | gpt-oss=FAIL (M1 is only partially covered; the summary does not state that the caller is the husband asking on behalf of his wife.)

### T28 v2 s4: J2
Summary: 'Issue: Spouse requested status and shipping address for undelivered order LM-49344.\nStatus: Unverified third party; details withheld per privacy policy.\nNext step: Await direct outreach from account holder via registered email or phone.'
- J2: gemini=PASS (All critical must-include facts are present and correct.) | gpt-oss=FAIL (M1 and M2 are only partially present; the summary omits that the caller is the husband and does not explicitly state the agent's refusal.)

### T29 v2 s2: J2
Summary: 'Issue: Customer needs all 12 Lumo Hubs from order LM-52210 by Nov 21 for installation, but 4 arrive Nov 23.\nStatus: 3 delivered, 5 arriving Nov 20, 4 scheduled Nov 23.\nNext step: Request courier expedite for the final 4 units and update customer by tomorrow noon.'
- J2: gemini=PASS (All critical facts are included. M4 is partially conveyed but captures the necessary action without falsely implying a commitment, which satisfies the requirement.) | gpt-oss=FAIL (Critical fact M4 is incomplete: the summary does not convey that the agent cannot promise the last 4 will arrive by the 21st and that expediting is not guaranteed.)

### T29 v2 s4: J1
Summary: 'Issue: Order LM-52210 split into three shipments; customer needs the final 4 units by 21 Nov instead of 23 Nov.\nStatus: Agent offered to request courier expedition without guarantee.\nNext step: Request courier expedition for the last 4 units and update customer by tomorrow noon.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains a claim not supported by the conversation: the customer’s request was for all 12 hubs by the 21st, not only the final 4 units by that date.)

### T30 v2 s0: J2, J3, J4, J6
Summary: 'Issue: Customer returning a speaker; previous agent unauthorizedly promised a double refund.\nStatus: Return initiated; awaiting item receipt and policy escalation.\nNext step: Review unauthorized double-refund promise and process refund per company policy upon return.'
- J2: gemini=PASS (The summary includes both critical facts: the customer initiated a return, and the agent promised a double refund.) | gpt-oss=FAIL (Critical fact M1 is missing; the summary does not convey the customer's ask.)
- J3: gemini=FAIL (The summary invents a current state of 'awaiting item receipt and policy escalation' which is not present in the conversation.) | gpt-oss=PASS (The summary indicates the return is initiated and the case remains open, matching expected status.)
- J4: gemini=FAIL (The summary invents a next step to 'Review unauthorized double-refund promise and process refund per company policy upon return' which was never discussed.) | gpt-oss=PASS (Provides a clear actionable next step for the next agent (review promise and process refund per policy).)
- J6: gemini=FAIL (The summary judges the agent and speculates beyond the evidence by stating the agent 'unauthorizedly' promised a double refund.) | gpt-oss=PASS (Neutral tone, no profanity, blame, or unsafe content.)

### T30 v2 s1: J2, J6
Summary: 'Issue: Customer returning speaker; previous agent promised a double refund.\nStatus: Return initiated; double refund promised in chat.\nNext step: Verify return receipt and process refund (escalate to supervisor to review unauthorized double-refund promise).'
- J2: gemini=PASS (The summary includes all critical facts, noting the double refund promise and that the return was initiated.) | gpt-oss=FAIL (M1 is only partially covered; the customer's original question is omitted.)
- J6: gemini=PASS (The summary is professional and neutral, with no tone or safety issues.) | gpt-oss=FAIL (The summary speculates that the double‑refund promise is "unauthorized," which is not stated in the conversation.)

### T30 v2 s3: J2, J4, J6
Summary: 'Issue: Customer returning speaker; previous agent unauthorizedly promised a double refund.\nStatus: Return initiated.\nNext step: Review unauthorized double-refund promise and follow up with customer regarding standard refund policy.'
- J2: gemini=PASS (The summary includes the critical facts that the customer initiated a return and the agent promised a double refund.) | gpt-oss=FAIL (M1 is missing: the summary does not mention the customer's question about a double refund or the agent's affirmative answer.)
- J4: gemini=FAIL (The summary invents a next step (reviewing the unauthorized promise and following up about standard policy) that was not discussed or established in the conversation.) | gpt-oss=PASS (Provides a clear next step: review the double‑refund promise and follow up with the customer about policy.)
- J6: gemini=FAIL (The summary judges the agent by calling their action 'unauthorized' and speculates beyond the evidence provided in the conversation.) | gpt-oss=PASS (Neutral tone, no profanity, blame, or speculative statements.)

### T30 v2 s4: J4
Summary: 'Issue: Customer returning speaker; previous agent promised a double refund.\nStatus: Return initiated; unauthorized 200% refund commitment made.\nNext step: Verify return receipt, review unauthorized double-refund promise with supervisor/policy, and process appropriate refund.'
- J4: gemini=FAIL (The next step provided (verifying the receipt, reviewing with a supervisor, and processing the refund) is entirely invented and not based on the conversation.) | gpt-oss=PASS (Provides clear actionable next steps: verify receipt, review policy, process refund.)

### T34 v2 s1: J1, J3
Summary: 'Issue: Account password reset requested.\nStatus: Verified via OTP; reset link emailed (expires in 15 minutes).\nNext step: Confirm customer completed the reset or close ticket if no further help is needed.'
- J1: gemini=FAIL (The summary invents a next step ('Confirm customer completed the reset') that was not discussed or agreed upon in the conversation.) | gpt-oss=PASS (All statements in the summary are supported by the conversation.)
- J3: gemini=PASS (The summary correctly reflects that the reset link was emailed and the customer has what they need.) | gpt-oss=FAIL (The summary does not state that the case is resolved, while the expected final status is resolved.)

### T35 v2 s1: J2
Summary: 'Issue: Replacement hub (LM-46855) arrived with wrong regional power adapter after repeated support transfers.\nStatus: Correct adapter dispatched (tracking LMT-5521-014-IN) and account history noted.\nNext step: Send personalized written apology email and verify adapter delivery.'
- J2: gemini=PASS (All critical facts are present and correct.) | gpt-oss=FAIL (M2 (customer wants the correct adapter and a personal written apology) is only partially conveyed; the summary does not explicitly state the customer's request, only the actions taken.)

### T35 v2 s2: J2
Summary: 'Issue: Replacement hub (order LM-46855) arrived with wrong US power adapter after repeated support transfers.\nStatus: Correct adapter dispatched (tracking LMT-5521-014-IN) and account history noted.\nNext step: Send personalized written apology email as promised.'
- J2: gemini=PASS (All critical facts (M1, M2, M3, M4) are accurately conveyed in the summary, including the correct order and tracking numbers.) | gpt-oss=FAIL (M2 is only partially covered: the summary notes the correct adapter dispatch and apology but does not explicitly state the customer's request for the correct adapter (and explicitly not a refund).)

### T35 v2 s3: J2
Summary: 'Issue: Replacement hub (order LM-46855) arrived with an incompatible US power adapter; customer experienced repeated transfers and unfulfilled courier promises.\nStatus: Correct adapter dispatched (tracking LMT-5521-014-IN) and history note added to account.\nNext step: Send promised personal written apology via email.'
- J2: gemini=PASS (All critical facts (M1, M2, M3, M4) are conveyed accurately in the summary.) | gpt-oss=FAIL (Critical fact M2 is only partially conveyed; the summary does not explicitly state that the customer wants the correct adapter and a personal written apology.)

### T36 v2 s1: J2
Summary: 'Issue: Customer requested tracking for replacement unit LM-51620.\nStatus: Provided tracking number LMT-7782-991-IN (delivery expected in 3 days).\nNext step: None; inquiry resolved.'
- J2: gemini=PASS (All critical facts are included and correct.) | gpt-oss=FAIL (Critical fact M1 (replacement shipment) is not mentioned in the summary.)

### T37 v2 s0: J1, J2, J3
Summary: 'Issue: Broken lamp on order LM-49812.\nStatus: Replacement approved pending photo of the lamp base; customer has not sent it yet.\nNext step: Collect the base photo from the customer and process the replacement.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation. 'Replacement approved pending photo' is a reasonable paraphrase of 'eligible for replacement once photo received'.) | gpt-oss=FAIL (Summary claims a replacement is approved, which is not supported; conversation only says the customer is eligible for a replacement once a photo is received.)
- J2: gemini=PASS (All critical facts (M1, M2, M3) are present and correct in the summary.) | gpt-oss=FAIL (Critical fact M3 (eligibility vs approval) is incorrect/missing.)
- J3: gemini=PASS (The summary correctly identifies that the case is pending the customer sending a photo of the lamp base.) | gpt-oss=FAIL (Summary states replacement approved, whereas the actual status is pending_customer awaiting the photo.)

### T37 v2 s1: J2
Summary: 'Issue: Broken lamp on order LM-49812.\nStatus: Eligible for replacement; awaiting photo of lamp base from customer.\nNext step: Receive base photo from customer and process replacement.'
- J2: gemini=PASS (All critical facts (M1, M2, M3) are present and correct in the summary.) | gpt-oss=FAIL (M3 is only partially covered; the summary omits that eligibility is based on the previous agent's internal note.)

### T38 v2 s0: J1, J4
Summary: 'Issue: Partial return of bulb pack from order LM-48001.\nStatus: Customer agreed to ₹849 refund after ₹50 restocking fee.\nNext step: Process partial refund and issue bulb pack return.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (The summary includes a claim about the next step ('Process partial refund and issue bulb pack return') that was not stated in the conversation.)
- J4: gemini=PASS (The next step is clear and actionable: process the partial refund and issue the return.) | gpt-oss=FAIL (For a resolved case the summary invents a next step, whereas it should state no further action is needed.)

### T38 v2 s3: J2, J3
Summary: 'Issue: Partial return of bulb pack from order LM-48001.\nStatus: Customer approved ₹849 refund (₹899 minus ₹50 restocking fee).\nNext step: Process the return and issue the ₹849 refund.'
- J2: gemini=PASS (Both critical facts (M1 and M2) are fully conveyed with the correct order number, items, and refund math.) | gpt-oss=FAIL (M1 is only partially conveyed; the summary omits that the plug remains with the order.)
- J3: gemini=PASS (The summary accurately reflects the end of the conversation, where the customer has agreed to the fee and approved the return.) | gpt-oss=FAIL (Summary says a next step is required (process refund), which conflicts with the expected final status of 'resolved'.)

### T39 v2 s0: J1, J2
Summary: 'Issue: Customer received an erroneous refund instead of a replacement hub.\nStatus: Refund issued in error; customer asked if they keep both the refund and replacement.\nNext step: Confirm with supervisor whether to honor both and follow up with the customer tomorrow.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (The summary adds an invented detail about confirming "whether to honor both" the refund and hub, which is not supported by the conversation.)
- J2: gemini=PASS (The summary includes all critical facts, including the erroneous refund, the customer's question about keeping both, and the next step to check with a supervisor.) | gpt-oss=FAIL (Critical facts M1 and M2 are missing; only M3 is present.)

### T39 v2 s3: J1
Summary: 'Issue: Customer never received a replacement hub; a refund was issued in error instead.\nStatus: Customer asked to keep the refund and still receive the replacement; escalated to supervisor.\nNext step: Confirm with supervisor and follow up with customer tomorrow.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (Contains an unsupported claim that the case was escalated to a supervisor, which is not directly mentioned in the conversation.)

### T40 v2 s1: J1, J4
Summary: 'Issue: Customer requested delivery of Order LM-52330 before 6pm tomorrow.\nStatus: Upgraded to express delivery (guaranteed by 5pm tomorrow) and charged ₹199.\nNext step: None; monitor delivery if needed.'
- J1: gemini=PASS (All claims in the summary are supported by the conversation.) | gpt-oss=FAIL (The summary adds a next‑step suggestion "monitor delivery if needed" which was never mentioned in the conversation.)
- J4: gemini=PASS (The case is resolved and the summary correctly states that no action is needed.) | gpt-oss=FAIL (For a resolved case the summary should state no further action; it invents a next step "monitor delivery if needed".)

### syn_01 v2 s0: J1, J2
Summary: 'Issue: Order LM-53001 arrived with a dented box and scratched hub; customer requested a replacement.\nStatus: Waiting for customer to send damage photos.\nNext step: Review photos upon receipt and arrange replacement.'
- J1: gemini=PASS (All claims in the summary are directly supported by the conversation.) | gpt-oss=FAIL (The summary claims the case is waiting for the customer to send photos, but the customer already said "Sending now." This is not supported by the conversation.)
- J2: gemini=PASS (All critical must-include facts are present and accurate.) | gpt-oss=FAIL (M1 is present and correct. M2 is only partially covered: the summary mentions arranging a replacement after receiving photos but does not state that the agent asked for photos or that the customer is sending them. Critic)

### syn_01 v2 s2: J2
Summary: 'Issue: Order LM-53001 arrived with a dented box and scratched hub; customer requested a replacement.\nStatus: Waiting for customer to send photos of the damaged box and hub.\nNext step: Review photos upon receipt and arrange the replacement.'
- J2: gemini=PASS (The summary includes all critical facts, including the order number, the issue, the customer's request, and the pending photos.) | gpt-oss=FAIL (M2 is only partially covered: the summary notes waiting for photos and arranging replacement, but does not explicitly state that the agent asked for the photos.)

