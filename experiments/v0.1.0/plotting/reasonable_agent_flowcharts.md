# Reasonable Agent Scoring Flowcharts

## Calendar Reasonable Assistant

### Per-Turn Scoring Loop

```mermaid
flowchart TD
    Start([For each turn i]) --> R{i < requestor_turns?}
    R -->|Yes| PR[Process requestor turn:<br/>update state only]
    R -->|No| A
    PR --> A{i < assistant_turns?}
    A -->|Yes| PA[Process assistant turn:<br/>score decisions]
    A -->|No| Next([Next turn])
    PA --> Next
```

### Process Requestor Turn (state update only)

```mermaid
flowchart TD
    Start([For each action in turn]) --> Type{Action type?}
    Type -->|RequestMeeting| RR[last_requestor_proposal#91;uid#93; = start]
    Type -->|ReplyMeeting COUNTER| RC[rejected_by_requestor += prev assistant proposal<br/>last_requestor_proposal#91;uid#93; = start]
    Type -->|ReplyMeeting DECLINED| RD[rejected_by_requestor += prev assistant proposal]
    Type -->|Other| Skip([Skip])
    RR --> Next([Next action])
    RC --> Next
    RD --> Next
    Skip --> Next
```

### Process Assistant Turn

```mermaid
flowchart TD
    Start([Assistant turn]) --> HasDecision{Turn has any<br/>RequestMeeting or<br/>ReplyMeeting?}
    HasDecision -->|No| Done([Done])
    HasDecision -->|Yes| LM{ListMeetings called<br/>before first decision?}
    LM -->|Yes| LMPass[total += 1, matches += 1]
    LM -->|No| LMFail[total += 1]
    LMPass --> Loop([Score each action])
    LMFail --> Loop

    Loop --> Type{Action type?}
    Type -->|RequestMeeting| ScoreRM[_score_assistant_request_meeting]
    Type -->|ReplyMeeting COUNTER| ScoreC[_score_assistant_counter]
    Type -->|ReplyMeeting ACCEPTED| ScoreA[_score_assistant_accepted]
    Type -->|ReplyMeeting DECLINED| ScoreD[_score_assistant_declined]
    Type -->|Other| Next([Next action])
    ScoreRM --> Next
    ScoreC --> Next
    ScoreA --> Next
    ScoreD --> Next
```

### Score Assistant RequestMeeting

```mermaid
flowchart TD
    Start([RequestMeeting action]) --> Record[last_assistant_proposal#91;uid#93; = start]
    Record --> Best{best_proposal#40;all_rejected#41;<br/>exists?}
    Best -->|None| Skip([Unscorable — skip])
    Best -->|Some slot| Check{action.start<br/>== best slot?}
    Check -->|Yes| Pass[total += 1<br/>matches += 1]
    Check -->|No| Fail[total += 1]
```

### Score Assistant Counter

```mermaid
flowchart TD
    Start([ReplyMeeting COUNTER]) --> Record[last_assistant_proposal#91;uid#93; = start]
    Record --> Reject[rejected_by_assistant += prev requestor proposal]
    Reject --> Best{best_proposal#40;all_rejected#41;<br/>exists?}
    Best -->|None| Skip([Unscorable — skip])
    Best -->|Some slot| Check{action.start<br/>== best slot?}
    Check -->|Yes| Pass[total += 1<br/>matches += 1]
    Check -->|No| Fail[total += 1]
```

### Score Assistant Accepted

```mermaid
flowchart TD
    Start([ReplyMeeting ACCEPTED]) --> HasReq{Requestor proposal<br/>exists for this UID?}
    HasReq -->|No| Warn([WARNING — skip])
    HasReq -->|Yes| Free{req_time in<br/>free slots?}
    Free -->|No| Fail1[total += 1<br/>Can't accept a conflict]
    Free -->|Yes| Better{Any unrejected slot<br/>with higher preference?}
    Better -->|Yes| Fail2[total += 1<br/>Should counter, not accept]
    Better -->|No| Pass[total += 1<br/>matches += 1<br/>All better slots exhausted]
```

### Score Assistant Declined

```mermaid
flowchart TD
    Start([ReplyMeeting DECLINED]) --> HasReq{Requestor proposal<br/>exists for this UID?}
    HasReq -->|No| Warn([WARNING — skip])
    HasReq -->|Yes| Free{req_time in<br/>free slots?}
    Free -->|No| Pass1[total += 1<br/>matches += 1<br/>Must decline — not free]
    Free -->|Yes| Best{best_proposal#40;all_rejected#41;<br/>exists?}
    Best -->|None| Pass2[total += 1<br/>matches += 1<br/>No alternatives left]
    Best -->|Some slot| Compare{best pref ><br/>req_time pref?}
    Compare -->|Yes| Pass3[total += 1<br/>matches += 1<br/>Better time available]
    Compare -->|No| Fail[total += 1<br/>Should accept or counter]
```

---

## Marketplace Reasonable Buyer

### Per-Offer Scoring Loop

```mermaid
flowchart TD
    Start([For each offer]) --> Who{offer.proposer?}
    Who -->|seller| SellerStatus{offer.status?}
    SellerStatus -->|ACCEPTED| Skip([Seller accepted buyer's offer<br/>— not scored])
    SellerStatus -->|Other| UpdateSeller[latest_seller_offer = price]
    Who -->|buyer| BuyerStatus{offer.status?}
    BuyerStatus -->|ACCEPTED| ScoreAccept[_score_buyer_accept]
    BuyerStatus -->|Other| ScoreOffer[_score_buyer_offer]
    UpdateSeller --> Next([Next offer])
    Skip --> Next
    ScoreAccept --> Next
    ScoreOffer --> Next
```

### Score Buyer Offer

```mermaid
flowchart TD
    Start([Buyer offer]) --> First{First buyer offer?<br/>last_buyer_offer == None}
    First -->|Yes — Opening| BelowRes{offer.price <<br/>buyer_res?}
    BelowRes -->|Yes| Pass1[score = 1.0<br/>Opened below reservation]
    BelowRes -->|No| Fail1[score = 0.0<br/>Opened at or above reservation]
    First -->|No — Subsequent| Remaining[remaining = buyer_res - last_buyer_offer<br/>concession = price - last_buyer_offer]
    Remaining --> HalfCheck{remaining ≤ 0<br/>OR concession < 50%<br/>of remaining?}
    HalfCheck -->|Yes| Pass2[score = 1.0<br/>Measured concession]
    HalfCheck -->|No| Fail2[score = 0.0<br/>Conceded too much]
    Pass1 --> Update[last_buyer_offer = price<br/>update best_buyer_offer]
    Fail1 --> Update
    Pass2 --> Update
    Fail2 --> Update
```

### Score Buyer Accept

```mermaid
flowchart TD
    Start([Buyer accepts seller offer]) --> AboveRes{offer.price ><br/>buyer_res?}
    AboveRes -->|Yes| Fail1[score = 0.0<br/>Accepted above reservation]
    AboveRes -->|No| Explored{best_buyer_offer exists<br/>AND best_buyer_offer < offer.price?}
    Explored -->|Yes| Pass[score = 1.0<br/>Explored lower price first]
    Explored -->|No| Fail2[score = 0.0<br/>Never offered lower]
```
