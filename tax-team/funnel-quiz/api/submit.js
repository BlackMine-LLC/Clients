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

      // Build custom fields array for all 8 quiz answer fields
      const customFields = [];
        if (body.pain_point)             customFields.push({ key: 'pain_point',             field_value: body.pain_point });
        if (body.current_cpa_engagement) customFields.push({ key: 'current_cpa_engagement', field_value: body.current_cpa_engagement });
        if (body.tax_paid_range)         customFields.push({ key: 'tax_paid_range',          field_value: body.tax_paid_range });
        if (body.business_type)          customFields.push({ key: 'business_type',           field_value: body.business_type });
        if (body.last_year_income)       customFields.push({ key: 'last_year_income',        field_value: body.last_year_income });
        if (body.current_income)         customFields.push({ key: 'current_income',          field_value: body.current_income });
        if (body.tcpa_sms_consent !== undefined)       customFields.push({ key: 'tcpa_sms_consent',       field_value: String(body.tcpa_sms_consent) });
        if (body.tcpa_marketing_consent !== undefined) customFields.push({ key: 'tcpa_marketing_consent', field_value: String(body.tcpa_marketing_consent) });

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
