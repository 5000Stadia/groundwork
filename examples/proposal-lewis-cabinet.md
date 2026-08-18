# Lewis Cabinet — What we heard, and what we'd do about it

*An outsource manufacturer that produces cabinet parts and doors for cabinet shops.*

Lewis Cabinet’s biggest cost was delayed cash, followed closely by office work that consumed whole days. Orders shipped before invoices went out; overdue accounts surfaced only when wood bills were already due. Brady’s summary was blunt: “the cash flow was just a nightmare for him.” Meanwhile, faxed orders had to be typed into Excel, and calculating door parts became a full-time job.

The existing workarounds did work. The spreadsheet calculated parts, the neighbor could change formulas, and customers knew how to fax. The cost was the owner’s time, late collections, inventory guesswork, and dependence on whoever understood the file.

Start with O1: issue invoices when work ships, include a payment link, and surface overdue accounts immediately. Then prove O2 on one common product family before adding inventory purchasing and editable production rules.

We would not begin by turning this into software for every manufacturer; N1 shows how expensive that detour became. We also would not repeat the cold-turkey fax shutdown in N2. It ultimately worked, but it put the family’s livelihood at risk when a controlled customer pilot could prove the same point.

*Everything below carries a code (O = opportunity, N = not worth doing, Q = open question). Reply with the codes — "O2 yes, but N1 worries me" is a complete answer.*

---

## What we heard

In your words, ranked by how much they seem to cost you:

### 1. Cabinet shops received finished work long before Lewis Cabinet knew whether it would be paid

> “He’d send them out and a month later, he’d get around to invoicing them. And then two months after that, he’d realize, “Oh my gosh, these are past due and I have wood bills due.””

> “We’d get taken for $40,000 here, $20,000 there.”

Lewis Cabinet financed customers while carrying its own wood bills. The informal credit process preserved customer relationships, but it also let unpaid balances become serious losses before anyone acted.

### 2. Fax-to-Excel order entry consumed the owner’s working day

> “He’d get a fax in. He’d pick it up and he’d type it into an Excel.”

> “And it took forever. It was a full-time job for him. So, he was spending eight hours a day doing that.”

The spreadsheet was useful: it translated an order into required door parts. The cost was retyping every fax and keeping the owner occupied with calculations instead of production, customers, and cash.

### 3. Every order created a fresh wood-counting and purchasing exercise

> “So, it was then my job to go around and figure out how much wood we needed for that order that came in and how much do we have.”

> “We had no real system to do that.”

Someone had to compare each order with material on hand, account for waste, and prepare purchasing information. That manual check worked through employee knowledge, but it added office work and made timely buying depend on one person remembering every step.

### 4. Routine product changes required outside technical help

> “It was all hard-coded. We had to call the developer and say, “Here’s what we want to do.””

> “If you wanted a change, you had to call your neighbor and have him come over and work on it.”

Both the spreadsheet and first website could run the shop, but Lewis Cabinet could not safely change products, cut rules, or outputs itself. Every exception introduced waiting, explanation, and the risk that the person who understood the logic was unavailable.

## Opportunity map

### O1 — Invoice at shipment and make payment one click away

**Where this comes from:** Brady described orders going out, invoices waiting until the following month, and overdue accounts remaining unnoticed until wood bills were due.

> “It was all checks. It was all cash. It was all send an invoice in the mail and then send it back with a check.”

> “People just like getting an email that says, “You owe this much. Click here to pay it.” They click. They pay. Done.”

**Effort:** Small · **Confidence:** high — The delay and losses were explicit, and Lewis Cabinet later found that customers valued emailed payment links and card convenience.

**What it's worth:** Target the one-month delay before invoicing and prevent overdue accounts from sitting unnoticed for another two months. Earlier collection would reduce exposure to losses like the $40,000 and $20,000 accounts Brady recalled.
  
*Basis: Brady said invoicing occurred a month after shipment, overdue balances were noticed two months later, and Lewis Cabinet had been taken for $40,000 and $20,000. The target assumes an invoice can be created from shipment information on the day work leaves.*

**First slice:** For one customer group, create invoices on the day of shipment, email a payment link automatically, and place unpaid invoices on a simple aging list reviewed each morning.

### O2 — Let standard orders create their own production parts

**Where this comes from:** The first internal ordering website replaced fax re-entry and generated the parts needed to make the customer’s order.

> “At that moment when I turned around in my chair and I’m like, “I’m not inputting orders anymore. I have a full day.””

> “So, even though it wasn’t a drastic difference, just having all the data go directly into what–actually, sorry, I don’t mean to seem so clueless, but I don’t understand.”

**Effort:** Medium · **Confidence:** high — Lewis Cabinet actually made this change, and Brady reported that he was no longer inputting orders and had his day back.

**What it's worth:** Return up to eight hours per working day previously spent entering orders and calculating parts, while reducing mistakes caused by copying fax details into Excel.
  
*Basis: Brady said the manual process was a full-time job and consumed eight hours a day. The time impact assumes the pilot covers the standard orders responsible for most re-entry; exception orders would still receive manual review.*

**First slice:** Put one common door family into a customer order form that calculates price and required parts. Run the results beside the existing spreadsheet until both outputs agree, then invite a small group of repeat customers.

### O3 — Turn accepted orders into material requirements and draft purchase orders

**Where this comes from:** Once order calculations were available, Brady recognized that the same information could calculate required wood, waste, stock needs, and purchasing.

> “We got the order coming in. We’re doing calculations already, figure how much wood we need, figure out the waste yields and spit out the PO.”

> “So, we built that and again, turn around and we’re losing office employees.”

**Effort:** Medium · **Confidence:** high — The required quantities already come from order calculations, and Lewis Cabinet successfully used those calculations to produce purchase orders.

**What it's worth:** Remove recurring wood calculations and purchase-order preparation from the office queue, while giving the shop an earlier warning when accepted work exceeds available material.
  
*Basis: Brady identified material calculation and purchasing as the next manual job removed after order intake. He did not isolate the hours saved by this feature, so no separate labor figure is assumed.*

**First slice:** For the product family proven in O2, calculate required wood and expected waste, compare that requirement with a manually verified stock count, and produce a draft purchase order for human approval.

### O4 — Let the shop change products and cut rules without calling a developer

**Where this comes from:** The first website worked, but every product or output change was hard-coded and had to be sent back to the developer.

> “Your dad could not have any easy way to add a new kind of cabinet if he wanted to make it.”

> “It was all hard-coded. We had to call the developer and say, “Here’s what we want to do.””

**Effort:** Medium · **Confidence:** medium — The dependency is clear, but the frequency and operational cost of product-rule changes were not quantified.

**What it's worth:** Reduce waiting and developer calls when Lewis Cabinet adds a product, changes a dimension, or adjusts a cut rule.
  
*Basis: The transcript confirms that changes required the developer, but it does not state how often changes occurred or how long they waited. The claim is therefore limited to removing that dependency.*

**First slice:** Make the dimensions, part names, and cut formula for the first supported door family editable in an owner-only screen, with a preview and rollback before any change reaches production.

## What we'd say no to

Things that came up that we don't think are worth your money right now:

### N1 — Do not begin by rewriting Lewis Cabinet’s tools for every manufacturer

Brady saw demand from competitors and wanted to replace the shop-specific system with an open platform that could be sold to everyone doing similar work.

> “Oh, we should rewrite this and sell it to everyone that does this type of a business.”

> “He would have shut me down instantly if he knew that seven years later we’ve put $1.5 million into this.”

The outside demand was real: a competitor offered to buy the system, and the broader software eventually became a business. But that does not make a generalized platform the right first investment for Lewis Cabinet. Supporting different catalogues, variables, supplies, and production rules turned a shop tool into a seven-year undertaking. First finish O1 and O2 around Lewis Cabinet’s own work. Reconsider outside sales only after the shop can change its rules without developer help and onboarding another company no longer interrupts cabinet operations.

### N2 — Do not shut off fax ordering before a controlled customer pilot

Brady forced every customer onto the new website by refusing to accept any more faxes.

> “We were not going to accept any faxes ever again.”

> “We lost one customer for only a couple of weeks.”

> “He came back a couple of weeks later and he’s still one of our best customers today.”

The evidence cuts both ways: the hard cutoff worked, the lost customer returned, and customers eventually accepted the website. It also triggered furious arguments and put a major customer relationship against an unproven system. Lewis Cabinet does need a deadline, because Brady was right that customers prefer the old method. But first prove the form with repeat customers, compare its production output with the spreadsheet, and give the office a clear exception process. Then retire fax on a published date rather than gambling the family’s livelihood on launch day.

## Recommended path

**Start here:** Prove O1 within weeks: use shipment information to issue same-day invoices, add a payment link, and review one aging list daily for a selected customer group.

Then, in order:

1. Build the one-product-family pilot in O2, keeping the spreadsheet as a parallel check until the calculated parts consistently match.
2. Move a small group of repeat customers onto the order form, answer Q2, and set a gradual fax retirement plan rather than using N2.
3. Add O3 only for the orders already proven through the new intake path.
4. Add O4 so Lewis Cabinet can maintain that first product family without developer intervention.
5. After the shop’s own process is stable, revisit outside demand—but do not commit to N1 unless another company can be set up without custom development.

## Open questions

**Q1 — Which customers should pay at order, which should pay at shipment, and which genuinely require credit terms?**

> “They didn’t mind paying 3.5 percent to be able to accept payment immediately on a credit card.”

> “I watched my dad’s company go from accepting credit cards for maybe 20 percent of its payments to now to about 70 or 80 percent.”

*Our working assumption: Most new or higher-risk customers can pay by card at order or shipment, while a short list of proven cabinet shops keeps approved terms. This should be tested rather than forcing every customer into the same policy.*

**Q2 — What share of incoming orders follows standard product rules, and which modifications still require an employee to interpret the request?**

> “If there were any special modifications that had to happen, that was broken, blah, blah, blah.”

> “It captured the order. It was all hard-coded, though.”

*Our working assumption: A common door family supplies enough repeat volume to prove the new intake path, while special modifications remain in a manual exception queue during the first slice.*

**Q3 — Is the current stock count dependable enough to drive purchasing, or must material receiving and usage be recorded first?**

> “So, it was then my job to go around and figure out how much wood we needed for that order that came in and how much do we have.”

> “We got the order coming in. We’re doing calculations already, figure how much wood we need, figure out the waste yields and spit out the PO.”

*Our working assumption: The shop knows its material formulas and waste yields, but the on-hand quantity needs a manual baseline count before purchase orders can be trusted.*
