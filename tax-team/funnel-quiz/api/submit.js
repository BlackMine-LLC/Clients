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

    // Build custom fields array for quiz answers
    const customFields = [];
    if (body.pain_point)              customFields.push({ key: 'pain_point',              field_value: body.pain_point });
    if (body.current_cpa_engagement)  customFields.push({ key: 'current_cpa_engagement',  field_value: body.current_cpa_engagement });
    if (body.tax_paid_range)          customFields.push({ key: 'tax_paid_range',           field_value: body.tax_paid_range });
    if (body.business_type)           customFields.push({ key: 'business_type',            field_value: body.business_type });
    if (body.last_year_income)        customFields.push({ key: 'last_year_income',         field_value: body.last_year_income });
    if (body.current_income)          customFields.push({ key: 'current_income',           field_value: body.current_income });

    const contactPayload = {
      locationId:  LOCATION_ID,
      firstName:   body.first_name   || '',
      lastName:    body.last_name    || '',
      email:       body.email        || '',
      phone:       body.phone        || '',
      source:      'Quiz Funnel',
      tags:        ['quiz-lead'],
      customFields,
    };

    // Step 1: Create (or update) the contact
    const ghlRes = await fetch('https://services.leadconnectorhq.com/contacts/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${GHL_API_KEY}`,
        'Version':        '2021-07-28',
        'Content-Type':   'application/json',
        'Accept':         'application/json',
      },
      body: JSON.stringify(contactPayload),
    });

    const ghlText = await ghlRes.text();
    let ghlData;
    try { ghlData = JSON.parse(ghlText); }
    catch { ghlData = { raw: ghlText }; }

    // Step 2: If contact was created/found, add a note with the full quiz answers
    const contactId = ghlData?.contact?.id;
    if (contactId && ghlRes.ok) {
      const noteBody = [
        '📋 Quiz Funnel Submission',
        '',
        `Pain point: ${body.pain_point || '—'}`,
        `Current CPA engagement: ${body.current_cpa_engagement || '—'}`,
        `Tax paid range: ${body.tax_paid_range || '—'}`,
        `Business type: ${body.business_type || '—'}`,
        `Last year income: ${body.last_year_income || '—'}`,
        `Current income: ${body.current_income || '—'}`,
        `SMS consent: ${body.tcpa_sms_consent}`,
        `Marketing consent: ${body.tcpa_marketing_consent}`,
      ].join('\n');

      // Fire-and-forget note creation (don't block the response)
      fetch(`https://services.leadconnectorhq.com/contacts/${contactId}/notes`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${GHL_API_KEY}`,
          'Version':        '2021-07-28',
          'Content-Type':   'application/json',
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
