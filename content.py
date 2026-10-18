"""Scenes for 'SAP Agents, part 2: when two systems disagree'. Each sentence: (on-screen caption, spoken text).
No auditor role is mentioned anywhere (by request)."""
VOICE = "Schedar"
SCENES = [
 dict(id="banner", nav="Intro", sentences=[
  ("An SAP agent should say so when two systems disagree.",) * 2,
  ("This follow-up shows an SAP agent that cross-checks its numbers against an independent ledger, and flags a mismatch instead of hiding it.",) * 2]),
 dict(id="recap", nav="Recap", sentences=[
  ("Where this started: the standard Joule Studio build from SAP's learning journey.",) * 2,
  ("One destination variable, one skill per service operation, and five tools attached to a single agent.",) * 2,
  ("The model did the arithmetic itself, and reported material 41 short by 1.2, although the data said 1.7 required and 500 available.",
   "The model did the arithmetic itself, and reported material forty-one short by one point two, although the data said one point seven required and five hundred available."),
  ("So the arithmetic moved into a governed SAP service, with an audit trail for every call.",) * 2]),
 dict(id="gap", nav="The gap", sentences=[
  ("But that service reconciled against a table in its own database.",) * 2,
  ("If the data were wrong at the source, both sides would agree, and the check would prove nothing.",) * 2,
  ("So this version adds an independent ledger: a separate app, with its own data and its own token check.",) * 2]),
 dict(id="workflow", nav="Workflow", sentences=[
  ("Here is the flow for one question.",) * 2,
  ("The model picks one governed tool. The service reads SAP HANA and computes the verdict in code.",) * 2,
  ("Then it asks the ledger, through a destination, for the same figure.",) * 2,
  ("If they agree, the answer says match. If not, it says mismatch and shows both numbers.",) * 2,
  ("Either way, one chained audit row is written.",) * 2]),
 dict(id="architecture", nav="Architecture", sentences=[
  ("The ledger is a second Cloud Foundry app, reached only through the Destination service.",) * 2,
  ("The chat app finds the stock service by name, and the stock service finds the ledger by name, each with its own OAuth token.",) * 2,
  ("The stock service reads SAP HANA, calls the ledger, and writes the audit row. The ledger never touches the stock database.",) * 2,
  ("Only the language model sits outside SAP, and it sees tool results, never the databases.",) * 2]),
 dict(id="built", nav="Built live", sentences=[
  ("Everything runs on a personal SAP BTP trial account: four Cloud Foundry apps in one space.",) * 2,
  ("The new destination, GovLedgerService, is registered in the cockpit next to the stock service.",) * 2,
  ("It was created by a one-off task inside the platform, so no secret was ever typed or shown.",) * 2]),
 dict(id="match", nav="Live: match", sentences=[
  ("Now the live agent, running on SAP BTP.",) * 2,
  ("Asked whether order 1000001 is ready, it reports a shortage: material 42 is short by 1.2.",
   "Asked whether order one million and one is ready, it reports a shortage: material forty-two is short by one point two."),
  ("At the bottom, reconciliation status match. The ledger agrees with the stock service.",) * 2]),
 dict(id="mismatch", nav="Live: mismatch", sentences=[
  ("Now we change one number in the ledger: material 42 becomes 9.1, and the ledger restarts.",
   "Now we change one number in the ledger: material forty-two becomes nine point one, and the ledger restarts."),
  ("Same question. The stock service still computes 8.8, but the answer now says reconciliation status mismatch.",
   "Same question. The stock service still computes eight point eight, but the answer now says reconciliation status mismatch."),
  ("It names the material and shows both figures, instead of silently picking one.",) * 2,
  ("Then we restore the ledger, and the next answer matches again.",) * 2]),
 dict(id="sequence", nav="Sequence", sentences=[
  ("This sequence shows one question, end to end.",) * 2,
  ("The chat app and the model choose the tool. The service reads HANA and computes the verdict.",) * 2,
  ("It asks the Destination service for a token, then calls the ledger with it.",) * 2,
  ("The service compares the two figures, writes one chained audit row, and returns both numbers to the model.",) * 2]),
 dict(id="baseline", nav="Legacy rows", sentences=[
  ("The first audit rows were written before the hash chain existed.",) * 2,
  ("A one-time baseline gave the early rows their missing fields, and sealed all 21 of them behind one attestation row.",) * 2,
  ("From there the chain verifies: ok true, eleven rows, legacy baseline covered.",) * 2,
  ("Edit any of those 21 rows later, and the check fails.",) * 2]),
 dict(id="verify", nav="Verify", sentences=[
  ("The trail also exports as a plain file, with a small offline verifier that needs no SAP system.",) * 2,
  ("Anyone holding the file can recompute the chain, and see the first edited or missing row.",) * 2]),
 dict(id="difference", nav="Difference", sentences=[
  ("How is this different from conventional SAP?",) * 2,
  ("Conventionally, a person compares screens or reports by eye, if anyone checks at all. The logic sits in transactions and in judgment, and the logs are not tied to the question that was asked.",) * 2,
  ("Here, you ask in plain language. A tested service computes the verdict, an independent ledger cross-checks it on every answer, and every call is chained into the audit trail.",) * 2,
  ("What stays the same is the SAP foundation: HANA, BTP and the SAP security model.",) * 2]),
 dict(id="limits", nav="Limits", sentences=[
  ("A few honest limits.",) * 2,
  ("The ledger is a second app with sample data. In production it would be a real system of record.",) * 2,
  ("The end-user name is asserted by the caller, not authenticated, and the chain detects tampering rather than preventing it.",) * 2,
  ("Next: a real SAP API behind the destination, HANA audit policies or an external anchor, and a model inside your approved boundary.",) * 2]),
 dict(id="about", nav="About", sentences=[
  ("I'm Yuvaraj Aravindan, founder of AI Agentic Enterprises. We build governed AI agents for regulated industries on enterprise platforms like SAP.",) * 2,
  ("This was an independent demonstration on an SAP BTP trial account, not an SAP product announcement.",) * 2]),
]
