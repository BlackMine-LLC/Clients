def build_privacy():
    body = f"""
<section class="banner">{navy_layers()}<div class="wrap"><h1 data-split>Privacy Policy &amp; Terms of Service</h1><p class="lead">How Moments With Mrs. T collects, uses, and protects your information — in plain language.</p></div></section>
<section class="section"><div class="wrap"><div class="article prose">
<p><em>Last updated: {LEGAL_UPDATED}</em></p>
<p>Jump to: <a href="#privacy">Privacy Policy</a> · <a href="#cookies">Cookies &amp; analytics</a> · <a href="#sms">Text messages</a> · <a href="#terms">Terms of Service</a></p>

<h2 id="privacy">Privacy Policy</h2>
<p>This policy explains how <strong>Moments With Mrs. T</strong> (“we,” “us”), a life coaching and case management practice founded by Tieshia Henry and serving Lorain County, Cuyahoga County, and virtual clients, handles information when you visit this website or contact us.</p>

<h3>1. Information you give us</h3>
<p>When you request a consultation or contact us, we collect what you choose to share: your name, phone number, email address, the best time to reach you, the service you're interested in, any message you write, and whether you opted in to appointment text messages.</p>
<p>Please don't include detailed medical or mental-health information in the website form. You can share that privately during your consultation.</p>

<h3>2. Information collected automatically</h3>
<ul>
<li><strong>Hosting logs.</strong> Our hosting provider (Vercel) records basic technical data such as IP address, browser type, and pages requested. This is used to deliver the site, keep it secure, and prevent abuse.</li>
<li><strong>Analytics — only with your permission.</strong> If you choose “Allow analytics,” we use Microsoft Clarity to understand how visitors use the site: pages viewed, time on page, clicks, scrolling, device and browser type, and approximate location. Clarity may create session replays and heatmaps. Form fields are masked and never recorded. If you decline, Clarity does not load. See <a href="#cookies">Cookies &amp; analytics</a>.</li>
</ul>

<h3>3. How we use your information</h3>
<ul>
<li>To respond to your request and schedule, confirm, or reschedule appointments</li>
<li>To send reminders or updates about your sessions</li>
<li>To answer questions you send us</li>
<li>To keep the website secure and, if you allow analytics, to improve it</li>
</ul>
<p>We <strong>do not sell</strong> your personal information, share it for targeted advertising, or use it to send marketing messages.</p>

<h3>4. Who helps us run the site</h3>
<p>We share information only with service providers that help us operate, and only as needed:</p>
<ul>
<li><strong>Vercel</strong> — website hosting and security.</li>
<li><strong>FormSubmit</strong> — delivers your consultation request from the website to our email inbox.</li>
<li><strong>Google</strong> — our email inbox (Gmail). Google Maps loads only if you click “Show map.”</li>
<li><strong>Microsoft Clarity</strong> — website analytics, only if you allow it.</li>
</ul>
<p>We may also disclose information if required by law, or to protect someone's safety in an emergency.</p>

<h3>5. How long we keep it</h3>
<p>We keep consultation requests and contact details only as long as needed to respond and to provide services, and we delete them when you ask (unless we're required to keep them). Clarity keeps analytics data according to Microsoft's retention policy (recordings for about 30 days, aggregated data for up to about 13 months).</p>

<h3>6. How we protect it</h3>
<p>The site is served only over encrypted HTTPS with modern security settings, access to your information is limited to Moments With Mrs. T, and we never sell or rent it. No method of transmission or storage is 100% secure, but we take reasonable steps to protect your information.</p>

<h3>7. Children and teens</h3>
<p>We work with children (4th grade and up), teens, and families, but services for anyone under 18 are arranged by a parent or legal guardian. This website is not directed to children under 13, and we do not knowingly collect personal information online from children under 13. If you believe a child has sent us information through this site, contact us and we'll delete it.</p>

<h3>8. Your choices and rights</h3>
<ul>
<li>Ask to see, correct, or delete the information we have about you.</li>
<li>Stop appointment texts any time by replying STOP, or contact us.</li>
<li>Change your analytics choice any time with the <a href="#cookies" data-privacy-choices>Privacy choices</a> link in the footer.</li>
<li>We honor the Global Privacy Control (GPC) browser signal as a request to opt out of analytics.</li>
</ul>
<p>To make a request, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="tel:{PHONE_TEL}">{PHONE}</a>. We'll respond within 30 days.</p>

<h2 id="cookies">Cookies &amp; analytics</h2>
<p>This site uses no advertising cookies. We store your privacy choice in your browser so we don't ask again. If, and only if, you choose “Allow analytics,” Microsoft Clarity sets these first-party cookies:</p>
<ul>
<li><code>_clck</code> — keeps a random Clarity user ID (up to 1 year)</li>
<li><code>_clsk</code> — connects page views into one session (1 day)</li>
</ul>
<p>Microsoft may also use its own cookies when processing Clarity data. Learn more in the <a href="https://privacy.microsoft.com/privacystatement" target="_blank" rel="noopener">Microsoft Privacy Statement</a> and the <a href="https://learn.microsoft.com/clarity/setup-and-installation/cookie-list" target="_blank" rel="noopener">Clarity cookie list</a>.</p>
<p><button type="button" class="btn small ghost" data-privacy-choices>Change my privacy choices</button></p>

<h2 id="sms">Text messages (SMS)</h2>
<p>Texting is optional. If you check the box on our booking form, you agree to receive text messages from Moments With Mrs. T <strong>only</strong> about your appointments (confirmations, reminders, and rescheduling). Consent is not required to book.</p>
<ul>
<li>Message frequency varies. Message and data rates may apply.</li>
<li>Reply <strong>STOP</strong> to opt out at any time, or <strong>HELP</strong> for help.</li>
<li>We do not send promotional or marketing texts.</li>
<li>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Text-messaging opt-in data and consent are never shared with any third party.</li>
</ul>

<h3>Changes to this policy</h3>
<p>If we update this policy, we'll change the “Last updated” date above. Significant changes will be noted on this page.</p>

<h2 id="terms">Terms of Service</h2>
<p>By using this website or scheduling services with Moments With Mrs. T, you agree to these terms.</p>

<h3>1. What we offer</h3>
<p>Moments With Mrs. T provides life coaching, case management, family coaching, and skills workshops. <strong>These services are not therapy, counseling, medical care, or legal advice</strong>, and they are not a substitute for care from a licensed professional. Coaching works best alongside any clinical care you already receive.</p>

<h3>2. Not for emergencies</h3>
<p>This website and our services are not for emergencies. If you or someone else is in crisis or thinking about self-harm, call or text <a href="tel:988">988</a> (Suicide &amp; Crisis Lifeline) or dial 911.</p>

<h3>3. Website content</h3>
<p>Articles and other content on this site are for general information and encouragement. Every person's situation is different, and results from coaching vary.</p>

<h3>4. Booking and communication</h3>
<p>Submitting the website form is a request for a consultation, not a confirmed appointment. We'll contact you by phone, email, or (if you opted in) text to confirm. Program details, fees, payment, and cancellation terms are provided separately before services begin.</p>

<h3>5. Using this site</h3>
<p>Please don't misuse the site: no attempts to disrupt or hack it, send spam or harmful code, or submit false information.</p>

<h3>6. Ownership</h3>
<p>The Moments With Mrs. T name, logo, text, and images on this site belong to Moments With Mrs. T or are used with permission. Please don't copy or reuse them without written permission.</p>

<h3>7. Links to other sites</h3>
<p>We may link to other websites, like Facebook or Google Maps. We're not responsible for their content or privacy practices.</p>

<h3>8. Disclaimers and limitation of liability</h3>
<p>This website is provided “as is.” To the fullest extent allowed by law, Moments With Mrs. T is not liable for indirect or consequential damages arising from your use of the website.</p>

<h3>9. Governing law</h3>
<p>These terms are governed by the laws of the State of Ohio.</p>

<h3>10. Contact</h3>
<p>Questions about these terms or your privacy: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:{PHONE_TEL}">{PHONE}</a></p>
</div></div></section>
"""
    page("/privacy-policy-terms-and-agreements", "Privacy Policy & Terms | Moments With Mrs. T",
         "How Moments With Mrs. T collects, uses, and protects your information, our cookie and text-message policies, and the terms for using this website.", body)
