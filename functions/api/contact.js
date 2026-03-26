/**
 * Cloudflare Pages Function — Contact Form Handler
 * Receives form submissions and sends email via Resend API
 *
 * Environment variable required in Cloudflare Dashboard:
 *   RESEND_API_KEY = your Resend.com API key
 *
 * Endpoint: POST /api/contact
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': 'https://hub.rafeeg.ae',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS_HEADERS });
}

export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const { name, phone, service, city, page } = body;

    // Validate required fields
    if (!name || !phone || !service) {
      return Response.json(
        { success: false, message: 'جميع الحقول مطلوبة' },
        { status: 400, headers: CORS_HEADERS }
      );
    }

    // Sanitize phone (only digits, +, spaces)
    const cleanPhone = phone.replace(/[^\d+\s-]/g, '');
    if (cleanPhone.length < 7) {
      return Response.json(
        { success: false, message: 'رقم الهاتف غير صحيح' },
        { status: 400, headers: CORS_HEADERS }
      );
    }

    // Build email HTML
    const emailHtml = `
      <div dir="rtl" style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
        <div style="background:#189F18;color:white;padding:16px 24px;border-radius:12px 12px 0 0">
          <h2 style="margin:0;font-size:20px">🚿 طلب جديد — تركيب سيراميك حمامات</h2>
        </div>
        <div style="background:#f8f9fa;padding:24px;border:1px solid #e5e7eb;border-radius:0 0 12px 12px">
          <table style="width:100%;border-collapse:collapse;font-size:15px">
            <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280;width:120px">الاسم</td><td style="padding:10px 12px;font-size:17px;font-weight:bold">${name}</td></tr>
            <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الهاتف</td><td style="padding:10px 12px"><a href="tel:${cleanPhone}" style="color:#189F18;font-size:17px;font-weight:bold;text-decoration:none">${cleanPhone}</a></td></tr>
            <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الخدمة</td><td style="padding:10px 12px">${service}</td></tr>
            <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">المدينة</td><td style="padding:10px 12px">${city || '—'}</td></tr>
            <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الصفحة</td><td style="padding:10px 12px"><a href="${page || '#'}" style="color:#2B5DF5;font-size:13px">${page || '—'}</a></td></tr>
            <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الوقت</td><td style="padding:10px 12px">${new Date().toLocaleString('ar-AE', { timeZone: 'Asia/Dubai' })}</td></tr>
          </table>
          <div style="margin-top:20px;text-align:center">
            <a href="https://wa.me/${cleanPhone.replace(/[\s-]/g, '')}" style="display:inline-block;background:#25D366;color:white;padding:12px 32px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:16px">💬 تواصل عبر واتساب</a>
            <a href="tel:${cleanPhone}" style="display:inline-block;background:#189F18;color:white;padding:12px 32px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:16px;margin-right:10px">📞 اتصل الآن</a>
          </div>
        </div>
        <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px">تم الإرسال من hub.rafeeg.ae</p>
      </div>
    `;

    // Send via Resend API
    const RESEND_KEY = context.env.RESEND_API_KEY;

    if (!RESEND_KEY) {
      // Fallback: if no Resend key, use Cloudflare Email (MailChannels)
      const emailRes = await fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: 'info@rafeeg.ae', name: 'Rafeeg' }] }],
          from: { email: 'noreply@hub.rafeeg.ae', name: 'رفيق — نموذج الموقع' },
          subject: `🚿 طلب جديد — تركيب سيراميك حمامات في ${city || 'الإمارات'}`,
          content: [{ type: 'text/html', value: emailHtml }],
        }),
      });

      if (emailRes.status === 202 || emailRes.ok) {
        return Response.json({ success: true, message: 'تم الإرسال بنجاح' }, { headers: CORS_HEADERS });
      }

      const errText = await emailRes.text();
      console.error('MailChannels error:', errText);
      return Response.json(
        { success: false, message: 'فشل إرسال البريد' },
        { status: 500, headers: CORS_HEADERS }
      );
    }

    // Primary: Resend API
    const resendRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Rafeeg Hub <noreply@hub.rafeeg.ae>',
        to: ['info@rafeeg.ae'],
        subject: `🚿 طلب جديد — تركيب سيراميك حمامات في ${city || 'الإمارات'}`,
        html: emailHtml,
        reply_to: `${name} <noreply@hub.rafeeg.ae>`,
      }),
    });

    if (resendRes.ok) {
      return Response.json({ success: true, message: 'تم الإرسال بنجاح' }, { headers: CORS_HEADERS });
    }

    const resendErr = await resendRes.text();
    console.error('Resend error:', resendErr);
    return Response.json(
      { success: false, message: 'فشل إرسال البريد' },
      { status: 500, headers: CORS_HEADERS }
    );

  } catch (err) {
    console.error('Contact form error:', err);
    return Response.json(
      { success: false, message: 'خطأ في الخادم' },
      { status: 500, headers: CORS_HEADERS }
    );
  }
}
