# Allmoxy — Brady Lewis — What we heard, and what we'd do about it

*Cloud software that runs ordering, production, inventory, and payments for custom manufacturers, rooted in the cabinet industry.*

Brady, you built Allmoxy by removing work you had personally done: first the eight-hour order-entry job, then purchasing and inventory. The commercial model now depends on the same principle. Customers get the software free; Allmoxy earns when their customers pay through Stripe. That makes O1 the first move: show each manufacturer where checks still delay payment, then test one better payment request. Lewis Cabinet’s shift from 20 percent cards to 70 or 80 percent is the clearest evidence that behavior can change.

Next, finish measuring the setup path in O2. Implementation used to consume the year between trade shows, and although you have automated most of it, the remaining delay determines when Allmoxy gets paid. Then put a consistent follow-up process behind the one trade show that already produces paying customers through O3.

We would not build the large sales team you once planned in N1, chase every industry that could technically use the product in N2, or take marketplace payment risk in N3. All three have real upside. None is as close to revenue as helping existing manufacturers collect more payments through the system they already chose.

*Everything below carries a code (O = opportunity, N = not worth doing, Q = open question). Reply with the codes — "O2 yes, but N1 worries me" is a complete answer.*

---

## What we heard

In your words, ranked by how much they seem to cost you:

### 1. Finding customers has been the struggle, not proving the product works

> “It’s been a struggle from the beginning.”

> “We go to one tradeshow a year.”

Allmoxy has strong proof inside Lewis Cabinet and among trade-show buyers, but customer acquisition still rests heavily on one annual event. That leaves Brady carrying the sales problem he explicitly does not enjoy, while growth depends on a small number of high-value accounts.

### 2. Customer setup has historically consumed the capacity needed for growth

> “So, we realized early on that’s what’s going to limit this company’s growth, all the time that it takes to do that.”

> “There’s a lot of work to get their custom cabinet catalogue up and running.”

The workaround worked: Allmoxy accepted a trade-show cohort, set those customers up, and returned for another cohort the next year. The cost was that implementation, rather than demand, set the pace. Brady says much of this has since been automated, so the remaining issue is finding exactly where new accounts still stall.

### 3. Customers resisted paying for business-management software even when they willingly paid for card acceptance

> “So, it was a hard sell.”

> “But yet, they wouldn’t pay me 1 percent to run the whole business? This was just appalling to me.”

The original one-percent software fee made customers feel they had acquired a partner taking part of their business. The free-software, paid-processing workaround is working, but it ties Allmoxy’s revenue to whether each manufacturer actually moves customer payments through the product.

### 4. A long-running developer relationship carries both product knowledge and recurring conflict

> “My developer and I have had a very rocky go at things.”

> “He’s been with us since the beginning, not the very first hard-coded version.”

The relationship has survived and Brady describes the developer as brilliant, so replacing him would discard years of knowledge. The cost is the headache and business risk created when critical product knowledge sits inside a relationship that periodically blows up.

## Opportunity map

### O1 — Help each manufacturer move more customers from checks to payment links

**Where this comes from:** Brady explained that Lewis Cabinet moved from mostly checks to mostly cards because customers preferred receiving an email, clicking, and being done.

> “I watched my dad’s company go from accepting credit cards for maybe 20 percent of its payments to now to about 70 or 80 percent.”

> “People just like getting an email that says, “You owe this much. Click here to pay it.” They click. They pay. Done.”

**Effort:** Small · **Confidence:** high — The behavior change already happened inside the founding customer, and Brady directly tied the free model to Stripe referral payments.

**What it's worth:** At an account behaving like Lewis Cabinet, the immediate opportunity is the remaining 20–30 percent of payments not yet made by card. Moving even part of that share means faster cash for the manufacturer and more processing revenue for Allmoxy.
  
*Basis: Brady said Lewis Cabinet moved from about 20 percent card acceptance to about 70 or 80 percent. The remaining 20–30 percent is derived from that statement. It is an assumption that other active manufacturers have a similar remaining share.*

**First slice:** For a small group of active manufacturers, show check versus card share, flag unpaid invoices, and test one payment-link email that states the amount due and offers immediate payment. Compare payment use before and after the message.

### O2 — Measure and remove the last delays before a new account takes its first paid order

**Where this comes from:** Trade-show customers once required extensive catalogue setup, but Brady later said most of that work had been automated.

> “So, we’ve seen automated most of that and eliminated a lot of it.”

> “Not anymore. But yes, that’s how it was back then.”

**Effort:** Medium · **Confidence:** medium — The historical constraint is clear, but Brady explicitly said it no longer takes as long. Current activation data could show that another issue now matters more.

**What it's worth:** Protect Allmoxy from returning to the old pattern where setup work filled the year between annual trade shows, while bringing forward the first transaction that can generate processing revenue.
  
*Basis: Brady said the company attended one trade show a year and spent the period between shows getting customers running. He also said most setup work has now been automated. The remaining delay and its revenue effect need to be measured.*

**First slice:** Record five dates for each new account: signup, catalogue started, first product ready, first order, and first processed payment. Review the first cohort manually and fix the single step where the most accounts stop.

### O3 — Turn the proven annual trade show into a documented sales process

**Where this comes from:** Brady described a booth full of interested woodworkers and said a typical show produced a small but meaningful group of customers who signed up and paid.

> “We have a bunch of people sign up. By a bunch, I mean maybe ten, which is very small.”

> “They were actual signups. They were handing us checks.”

**Effort:** Small · **Confidence:** high — This is the only acquisition channel in the conversation with direct evidence of people paying at the point of contact.

**What it's worth:** Get more value from the roughly ten signups Brady associated with a trade show, while reducing the amount of follow-up that depends on him personally.
  
*Basis: Brady described about ten signups from a show and clarified that they were paying signups rather than leads. The current number, retention, and processing revenue per show cohort are not given and must be checked.*

**First slice:** Before the next show, define the booth demonstration, capture the manufacturer’s catalogue complexity and payment setup, and schedule a setup session before the prospect leaves. Send the same short follow-up sequence to every attendee.

### O4 — Preserve product knowledge without discarding the developer who built it

**Where this comes from:** Brady described a seven-year developer relationship that had produced the product but also repeated personal blowups.

> “Things are actually really good right now, knock on wood.”

> “My developer and I have had a very rocky go at things.”

**Effort:** Medium · **Confidence:** medium — The relationship risk is explicit, but the transcript does not show whether documentation, code ownership, deployment access, or backup coverage are currently missing.

**What it's worth:** Reduce the headache and interruption caused by another blowup while keeping the developer whose knowledge has helped carry Allmoxy from its early rewrite to the current product.
  
*Basis: The transcript establishes recurring conflict and long tenure, but gives no outage history or cost. The impact is therefore stated as reduced operational headache rather than a dollar amount.*

**First slice:** Choose one revenue-critical path—order through payment—and have someone other than the primary developer document how it is deployed, monitored, restored, and changed. Confirm that a second person can follow the document.

## What we'd say no to

Things that came up that we don't think are worth your money right now:

### N1 — Do not build the large sales and implementation team Brady once planned

After the cabin retreat, Brady concluded that long sales cycles and difficult implementations required exceptional salespeople and implementation staff.

> “I’ve got to hire amazing sales people.”

> “We went free. We went to a freemium model.”

That team could help close large, hesitant manufacturers, and the product still may need humans for complex accounts. But Brady moved away from this path for a reason: he is not passionate about managing a heavy sales process, and the processing model reduced the price objection. First prove that active accounts can be moved to their first transaction faster through O2 and that payment use can grow through O1. Add a salesperson only when the recorded funnel shows a repeatable step that a new hire can own.

### N2 — Do not market Allmoxy to every custom business yet

Brady deliberately kept features open enough for service companies and manufacturers beyond woodworking, and the product has been tried across very different products.

> “We’ve done a little bit of everything, everything from ChapStick to hamburgers, custom–anything that’s custom and that’s more of a business to business type thing, it just really shines for that.”

> “Obviously other wood workers would use this, but there’s a whole world of service companies and other types of manufacturing companies that I think need this.”

The product’s range is genuinely valuable and may become a major source of growth. The argument against doing it now is commercial, not technical: woodworking is where Allmoxy has a founding customer, recognizable workflows, a proven trade show, and paying buyers. Broad positioning would multiply catalogue examples, setup paths, support language, and sales messages before the current payment model is fully measured. Prove O1 and O3 in the home market first, then enter one adjacent manufacturing category with the closest order and catalogue structure.

### N3 — Do not become the payment marketplace or take transaction risk yet

Brady said Allmoxy might eventually move from receiving Stripe referral fees to taking a deeper marketplace role.

> “They’re more of a marketplace model, where they’re actually taking on–and we may go to that eventually once we figure out the risk and we want to get into that business a little deeper.”

> “So, we just have a partnership with Stripe. Stripe pays us a check separately.”

Owning more of the payment flow could improve economics and give Allmoxy more control. It also adds risk that Brady himself acknowledged, while the current Stripe partnership already pays Allmoxy separately. The next unanswered problem is not whether Allmoxy can become a marketplace; it is how much of each customer’s payment volume still sits outside the existing flow. Answer Q2 before taking on more responsibility.

### N4 — Do not spend time rescuing the paid chat add-on

Allmoxy offered paid in-app access to a dedicated representative because many customers wanted personal help, but Brady said the add-on was not selling.

> “I’m actually thinking about taking that down because no one buys it.”

> “A lot of people in this industry just want like, “I want you to hold my hand.” So, that’s what that is.”

The desire for handholding is real, so support should not disappear. But a separate chat charge is solving the wrong problem if customers will not buy it. Use human help at the specific activation step found in O2; do not make selling a small support add-on another sales job.

## Recommended path

**Start here:** Start O1 with a small active-customer cohort: record card versus check share, send one clearer payment-link request, and measure whether more invoices are paid through Allmoxy.

Then, in order:

1. Add O2: record the path from signup to first processed payment and remove the single largest delay.
2. Document O3 around the next woodworking show, including the booth demonstration, qualification notes, scheduled setup, and consistent follow-up.
3. Complete the first continuity exercise in O4 for the order-to-payment path.
4. Revisit N2 only after one woodworking cohort shows repeatable activation and payment behavior; then test one adjacent manufacturing category rather than a general business audience.

## Open questions

**Q1 — How long does a new account currently take to reach its first real order and first processed payment, and where does it stop?**

> “So, we’ve seen automated most of that and eliminated a lot of it.”

> “There’s a lot of work to get their custom cabinet catalogue up and running.”

*Our working assumption: Most catalogue setup has been automated, as Brady said, but one or two remaining steps probably still require personal help. The best guess is that this—not software capability—sets the time until Allmoxy earns from a new free account.*

**Q2 — For each active account, what payment volume runs through Stripe, what share still arrives by check or another processor, and what does Allmoxy receive?**

> “Stripe pays us a check separately.”

> “It’s working wonders for us.”

*Our working assumption: The processing model is attractive enough to keep because Brady said it was working well. The likely growth opportunity is increasing payment adoption inside existing accounts, but the transcript does not provide Stripe economics or current account-level payment shares.*

**Q3 — Do current trade shows still produce paying signups, and how many of those accounts reach a first transaction and remain active?**

> “They were actual signups. They were handing us checks.”

> “We have a bunch of people sign up. By a bunch, I mean maybe ten, which is very small.”

*Our working assumption: The woodworking trade show remains Allmoxy’s strongest acquisition channel because it produced customers who handed over checks, but the roughly ten-signup result is historical and should not be treated as the current benchmark without checking.*

**Q4 — How much current revenue comes from Lewis Cabinet and the next largest accounts?**

> “They pay about $4,500 a month.”

> “We do about a half a million a year.”

*Our working assumption: Lewis Cabinet was about one-tenth of revenue at the time of the conversation, based on the stated monthly payment and annual revenue. The best guess is that concentration has fallen as Allmoxy added customers, but that needs confirmation before changing pricing or payment terms.*
