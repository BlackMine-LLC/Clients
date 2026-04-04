export default async function handler(req, res) {
      if (req.method === 'OPTIONS') {
              res.setHeader('Access-Control-Allow-Origin', '*');
              res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
              res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
              return res.status(200).end();
      }

  res.setHeader('Access-Control-Allow-Origin', '*');
      res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
      res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method !== 'POST') {
          return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
          const body = req.body;

        // GHL API v2 — server-to-server, no Cloudflare WAF issues
        const GHL_API_KEY = 'pit-3e1dcd27-51f1-4319-99c8-6e28625b7d6d';
          const LOCATION_ID = '4HkogPO0ghTsjhHcnQBO';

        // Build custom fields array using verified GHL field keys
        // "Survey | Survey 0" group: short keys (confirmed working)
        // "Form | Quiz Lead capture" group: long verbose keys (from GHL form)
        const customFields = [];

        // pain_point → "What's your biggest frustration...?" (Form | Quiz Lead capture)
        if (body.pain_point) {
                  customFields.push({ key: 'whats_your_biggest_frustration_when_it_comes_to_taxes_and_your_finances_right_now', field_value: body.pain_point });
        }

        // current_cpa_engagement → "Current CPA?" (Survey | Survey 0)
        // Also maps to the longer form field
        if (body.current_cpa_engagement) {
                  customFields.push({ key: 'current_cpa', field_value: body.current_cpa_engagement });
                  customFields.push({ key: 'when_did_your_cpa_last_reach_out_to_you_about_lowering_your_tax_bill', field_value: body.current_cpa_engagement });
        }

        // tax_paid_range → "Taxes paid last year" (Survey | Survey 0)
        // Also maps to "How much did you pay in taxes last year?" (Form)
        if (body.tax_paid_range) {
                  customFields.push({ key: 'taxes_paid_last_year', field_value: body.tax_paid_range });
                  customFields.push({ key: 'how_much_did_you_pay_in_taxes_last_year', field_value: body.tax_paid_range });
        }

        // business_type → "Business Type" (Survey | Survey 0) + Form duplicate
        if (body.business_type) {
                  customFields.push({ key: 'business_type', field_value: body.business_type });
                  customFields.push({ key: 'what_best_describes_how_you_make_your_money', field_value: body.business_type });
        }

        // last_year_income → "Last Year Income" (Survey | Survey 0) + Form duplicate
        if (body.last_year_income) {
                  customFields.push({ key: 'last_year_income', field_value: body.last_year_income });
                  customFields.push({ key: 'what_was_your_total_income_last_year', field_value: body.last_year_income });
        }

        // current_income → "Current Income" (Survey | Survey 0) + Form duplicate
        if (body.current_income) {
                  customFields.push({ key: 'current_income', field_value: body.current_income });
                  customFields.push({ key: 'what_was_your_total_income_last_year_bi4_copy', field_value: body.current_income });
        }

        // TCPA consent fields — stored as strings in the note; no matching GHL field keys found
        // (these are captured in the backup note below)

        // Determine qualification tag based on current_income
        const income = (body.current_income || '').trim();
          let qualificationTags = [];
          if (income === '$400,000+') {
                    qualificationTags = ['Qualified', 'Qualified-C'];
          } else if (income.includes('100,000') && income.includes('399,999')) {
                    qualificationTags = ['Non-Qualified'];
          } else if (income) {
                    qualificationTags = ['Disqualified'];
          }

        const tags = ['quiz-lead', ...qualificationTags];

        const contactPayload = {
                  locationId: LOCATION_ID,
                  firstName:  body.first_name || '',
                  lastName:   body.last_name  || '',
                  email:      body.email      || '',
                  phone:      body.phone      || '',
                  source:     'Quiz Funnel',
                  tags,
                  customFields,
        };

        // Step 1: Try to create the contact
        let ghlRes = await fetch('https://services.leadconnectorhq.com/contacts/', {
                  method: 'POST',
                  headers: {
                              'Authorization': `Bearer ${GHL_API_KEY}`,
                              'Version':       '2021-07-28',
                              'Content-Type':  'application/json',
                              'Accept':        'application/json',
                  },
                  body: JSON.stringify(contactPayload),
        });

        let ghlText = await ghlRes.text();
          let ghlData;
          try { ghlData = JSON.parse(ghlText); } catch { ghlData = { raw: ghlText }; }

        // Step 2: Handle duplicate contact — upsert via PUT
        if (!ghlRes.ok && ghlData?.message?.toLowerCase().includes('duplicate')) {
                  console.log('Duplicate contact — looking up by email to upsert...');

            const lookupRes = await fetch(
                        `https://services.leadconnectorhq.com/contacts/?locationId=${LOCATION_ID}&email=${encodeURIComponent(body.email)}`,
                {
                              headers: {
                                              'Authorization': `Bearer ${GHL_API_KEY}`,
                                              'Version':       '2021-07-28',
                                              'Accept':        'application/json',
                              },
                }
                      );
                  const lookupData = await lookupRes.json();
                  const existingId = lookupData?.contacts?.[0]?.id;

            if (existingId) {
                        console.log('Patching existing contact:', existingId);
                        ghlRes = await fetch(`https://services.leadconnectorhq.com/contacts/${existingId}`, {
                                      method: 'PUT',
                                      headers: {
                                                      'Authorization': `Bearer ${GHL_API_KEY}`,
                                                      'Version':       '2021-07-28',
                                                      'Content-Type':  'application/json',
                                                      'Accept':        'application/json',
                                      },
                                      body: JSON.stringify(contactPayload),
                        });
                        ghlText = await ghlRes.text();
                        try { ghlData = JSON.parse(ghlText); } catch { ghlData = { raw: ghlText }; }
            } else {
                        console.error('Could not find existing contact by email for upsert.');
            }
        }

        // Step 3: Add a note as a backup record of the full quiz answers
        const contactId = ghlData?.contact?.id;
          if (contactId && ghlRes.ok) {
                    const noteBody = [
                                'Quiz Funnel Submission',
                                '',
                                `Pain point: ${body.pain_point || '-'}`,
                                `Current CPA engagement: ${body.current_cpa_engagement || '-'}`,
                                `Tax paid range: ${body.tax_paid_range || '-'}`,
                                `Business type: ${body.business_type || '-'}`,
                                `Last year income: ${body.last_year_income || '-'}`,
                                `Current income: ${body.current_income || '-'}`,
                                `SMS consent: ${body.tcpa_sms_consent}`,
                                `Marketing consent: ${body.tcpa_marketing_consent}`,
                                `Qualification: ${qualificationTags.join(', ') || 'none'}`,
                              ].join('\n');

            fetch(`https://services.leadconnectorhq.com/contacts/${contactId}/notes`, {
                        method: 'POST',
                        headers: {
                                      'Authorization': `Bearer ${GHL_API_KEY}`,
                                      'Version':       '2021-07-28',
                                      'Content-Type':  'application/json',
                        },
                        body: JSON.stringify({ body: noteBody, userId: '' }),
            }).catch(err => console.error('Note creation failed:', err));
          }

        return res.status(ghlRes.status).json({
                  success: ghlRes.ok,
                  status:  ghlRes.status,
                  ghl:     ghlData,
        });

  } catch (err) {
          console.error('Proxy error:', err);
          return res.status(500).json({ error: err.message });
  }
}
