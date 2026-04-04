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

      const ghlRes = await fetch('https://api.leadconnectorhq.com/forms/submit', {
              method: 'POST',
              headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
              },
              body: JSON.stringify({
                        formId:                  body.formId                  || 'i09YaDFj0y66doJJlKCM',
                        location_id:             body.location_id             || '4HkogPO0ghTsjhHcnQBO',
                        first_name:              body.first_name              || '',
                        last_name:               body.last_name               || '',
                        email:                   body.email                   || '',
                        phone:                   body.phone                   || '',
                        pain_point:              body.pain_point              || '',
                        current_cpa_engagement:  body.current_cpa_engagement  || '',
                        tax_paid_range:          body.tax_paid_range          || '',
                        business_type:           body.business_type           || '',
                        last_year_income:        body.last_year_income        || '',
                        current_income:          body.current_income          || '',
                        tcpa_sms_consent:        body.tcpa_sms_consent        || false,
                        tcpa_marketing_consent:  body.tcpa_marketing_consent  || false,
              }),
      });

      const ghlText = await ghlRes.text();
        let ghlData;
        try { ghlData = JSON.parse(ghlText); }
        catch { ghlData = { raw: ghlText }; }

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
