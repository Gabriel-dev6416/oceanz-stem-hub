# OCEANZ STEM HUB - Decisions on top of the SRS

The baseline is **SRS v3.3 (13 November 2026)**. These decisions were agreed with the Project
Owner during development. Where a decision still adds to or differs from v3.3, this file takes
precedence; decisions that v3.3 now contains or replaced are marked as such.

## Curriculum basis

All class, subject and topic seed data follows the standard Nigerian school curriculum
(NERDC Basic Education Curriculum for Primary and JSS; NERDC Senior Secondary curriculum for
SS 1-3), mapped to Common Entrance, BECE, WAEC, NECO and JAMB. Seed data stays editable by the
Admin from the back-office.

## D-01 Curriculum explorer in R1 (still applies)

FR-ENG-01 ships in R1. A simple curriculum topics table (class, subject, term, week, topic,
learning objectives) is built in R1 and edited by the Admin. R3 extends the same table with
syllabus mapping, teacher proposals and the curriculum tracker (FR-ACD-05, FR-PRG-05).

## D-02 Free trial button before R3 (now in v3.3, FR-ENG-02)

Until trial booking (FR-ENG-02) ships in R3, every "Book a Free Trial Class" button opens the
enquiry form with the enquiry type "Free trial class" pre-selected, with WhatsApp beside it.
R3 replaces the target with the booking flow; the buttons themselves do not change.

## D-03 Homepage blocks hidden until real content exists

"Meet our teachers", teacher intro videos, testimonials, results statistics, partners and the
"Built at OCEANZ" showcase render only when the Admin has published at least one real item.
No placeholder content is ever shown.

## D-04 Weekly report day (withdrawn 13 November 2026)

Withdrawn by the Project Owner: the weekly report goes out on Friday as in v3.3 FR-PRG-03
(configurable). It shows the previous week's quiz, because the current week's quiz is open from
Friday 08:00 to Sunday 20:00.

## D-05 Strict exam mode grace period

FR-CBT-15 default grace period changes from 0 seconds to 3 seconds (configurable 0-5 s per
exam), so a notification, incoming call or screen dimming on a low-end phone does not suspend
the attempt.

## D-06 Strict exam mode on iOS

Safari on iPhone cannot put a web page into full screen. On iOS the full-screen requirement is
dropped; leaving the page is detected through page visibility, page hide and window blur,
with the same grace period. All other Strict rules apply unchanged.

## D-07 Junior Primary small groups by year

Junior Primary (Primary 1-3) remains one class with one dashboard. The "Split class" proposal
(FR-GRP-02) forms small groups by year (Primary 1, 2 and 3) by default; mixing years in a
group needs a recorded reason. Curriculum topics and weekly quizzes are set per year.

## D-08 Sibling discount order

For each guardian and term, enrolments are ordered by fee, highest first. The highest pays
full price; the sibling discount (default 10%) applies to every other enrolment.

## D-09 Senior Secondary Commercial stream (withdrawn 13 November 2026)

Withdrawn by the Project Owner: Senior Secondary has two streams, Science and Art, as in v3.3.
The Admin can add a stream later from the back-office if needed.

## D-10 On-site drop-off and pick-up

New requirement FR-SAF-09 (Must, R3; v3.3 uses FR-SAF-08 for home lessons): for on-site
sessions with minors, the guardian registers
approved pick-up persons. Drop-off is recorded on the register; at pick-up the collecting
adult gives the guardian's pick-up PIN, which is checked and logged. A failed check alerts the
Safeguarding Lead and the guardian.

## D-11 Teacher earnings module

New later module (R6): teacher earnings, computed from attendance-verified sessions,
allocations and private tutoring hours, with payslips and Finance Officer approval. Pay rates
and rules need a separate Owner decision before design.

## D-12 Technical notes adopted

- Zoom: every learner joins with their platform ID as the Meeting SDK `customerKey`, so
  attendance webhooks map to learners without relying on display names.
- Watermarks are a deterrent and make leaks traceable; Bunny Stream DRM is an option if leaks
  occur.
- Notes conversion (Word, PowerPoint to watermarked page images) uses LibreOffice inside the
  Docker image, so the application is deployed to Render as a Docker image.
- A monthly running-cost budget (Render, Zoom licences, Bunny, email, SMS, AI) is agreed in R0.

## D-13 Corrections (now in v3.3)

- FR-PRG-03: "topics covered topics for next week" reads "topics covered and topics for next
  week".

## D-14 Editing website content in R1

Until the branded staff back-office (/staff/) and the Admin and staff roles arrive in R2, the
owner edits site settings and homepage content in the Django admin at the private admin path.
R2 moves this editing into /staff/ and limits the Django admin to Super Admins (FR-ADM-01).

## D-15 Logo (updated for v3.3)

The header and footer use the interim ~R logo mark from SRS v3.3 Section 8.2 (transparent,
served as an 8.5 KB WebP with a PNG fallback), beside the "OCEANZ STEM HUB" name. It is replaced
when the original high-resolution transparent file is supplied (v3.3 Appendix B item 19).

## D-16 SRS review fixes (12 November 2026; all now in v3.3)

1. **Class place, not "group".** Parents buy a Class place or Private tutoring; small groups sit
   inside a class. FR-PAY-01, FR-PVT-09, FR-WEB-05 and the Section 17 enrolment scenario read
   "class place" (or "Class/Private") wherever they say "group". Fee structures, the pricing
   page and enrolment screens use this wording.
2. **No class capacity.** The "capacity" field is removed from classes (FR-ACD-02). Classes have
   a minimum to open (default 12, FR-ACD-09) and no maximum. Capacity exists only on tertiary
   cohorts, holiday programmes and the on-site venue, which drive the waitlist (FR-ENR-09).
3. **Finance conflict of interest is Must, R2.** SEC-ACL-04 is split: a Finance Officer cannot
   verify payments or approve refunds for themselves or for families of learners they teach
   (Must, R2, same as FR-STF-04 and the Section 14.1 test case). The second approver for a
   teacher's own learners' term results stays Should, R4.
4. **Free trial button before R3.** Already decided in D-02: it opens the enquiry form with
   "Free trial class" pre-selected until trial booking ships in R3.
5. **Recordings follow retention; notes and lesson videos are archived.** FR-PRT-08 applies to
   notes and uploaded lesson videos: archived, never deleted, when learners lose access. Live
   class recordings follow FR-LIV-11 and SEC-LIV-04: deleted after the retention period
   (default 12 months).
6. **FR-PRG-03 wording.** Already corrected in D-13: "teacher comment, topics covered, topics
   for next week".

## D-17 Contact form attachment

The optional attachment on the contact form (FR-COM-01) is added together with private file
storage (Cloudflare R2 with signed URLs, type and size checks, virus scan; SEC-INP-02). Until
then the form has no upload, so no visitor file is ever stored insecurely.

## D-18 Enquiry emails before background workers

Until Celery arrives (R2), the acknowledgement, staff notification and back-office replies are
sent directly by the web request. A failed send is logged and never loses the enquiry. R2 moves
all email to background jobs with retries and delivery logs (FR-NTF-04).

## D-19 Moving to SRS v3.3 (13 November 2026)

Corrections made to the work already built:

- Font: Manrope (headings 800, body 400-600) replaces Rubik and Inter; JetBrains Mono stays.
- Navigation bar (FR-WEB-17): logo to Home, Light/Dark/System theme switcher, Enrol Now; the
  menu collapses below 1200 px; on phones a bar with Enrol Now, WhatsApp and Call stays fixed at
  the bottom. Menu items appear as their pages are built (Contact now; Programmes, Pricing,
  About, Teach with us and Log in later).
- Footer (FR-WEB-20): logo and brand line, quick links, contacts, social links shown only when
  filled in (including a WhatsApp channel), the C³ words and copyright.
- Contacts: one WhatsApp number, three call lines, hub address #5 Gunning Rd, Abakaliki.
- Colours: WhatsApp buttons are WhatsApp green; Sunrise Orange is kept for the main action.
- Enquiry form: Primary 1-6 listed separately, SS Science and Art only, home lessons as a
  delivery format, country of residence, and five ways in (enrol, free trial, private tutoring
  quote, tertiary package, family abroad). Families abroad are saved as international enquiries,
  because their fees are quoted (FR-PAY-13). Contact topics follow FR-COM-01.
- Loading: the site is server-rendered, so pages arrive complete. Skeleton placeholders
  (NFR-22) are used for parts that load afterwards: the map now, and photos, the carousel and
  dashboard panels as they are added.

## D-20 Homepage bands in step 2c

The homepage follows the 14-band order of FR-WEB-01. Built in step 2c: header, hero, trust strip
with the C³ values (feature cards until real stats are published), who we teach, subjects, how
we teach, the four enrolment steps, testimonials (only when consented and published), ready to
learn online with the families-abroad strip, FAQ (only published questions) and the final call
to action. Added in step 2d with the pages they link to: the curriculum explorer, programmes
and pricing, and "More than coding" tertiary packages. Hidden until real content exists:
results and the project showcase, teachers, and the hero photo carousel, which also needs the
private media storage set up with R2.

The FAQ starts with five unpublished drafts written from SRS v3.3 facts for the Project Owner
to review and publish (v3.3 Appendix B item 25).

## D-21 Programmes, Subjects and Pricing in step 2d

- A `programmes` app holds the public catalogue: levels with subjects and Term Classes fees,
  the STEM pathway, Holiday Tuition sessions and fees, tertiary packages, and curriculum topics
  and termly projects. All of it is seeded from SRS v3.3 and edited in the admin. R2's academic
  structure (sections, classes, streams, terms) links to it rather than replacing it.
- Prices published: registration fee, Term Classes per level, Holiday Tuition per session,
  sibling discount, and bank details with copy buttons. Private tutoring, tertiary packages
  and families abroad show "Contact the Admin" cards and never a price (FR-PAY-13); their
  internal guide prices are not stored in the website until the quotes module (R2).
- Online card payment (Paystack) is not offered yet, so the Pricing page shows bank transfer
  details and says to pay only after the class is confirmed. Paystack arrives with registration
  in R2.
- Curriculum explorer: until the weekly topics for a class are entered, it says so and shows the
  class's subjects and the STEM pathway skills from the SRS, never invented topics.
