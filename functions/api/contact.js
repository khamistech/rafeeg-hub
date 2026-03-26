/**
 * Cloudflare Pages Function — Contact Form Handler
 * Sends email to info@rafeeg.ae via Brevo (Sendinblue) transactional API
 *
 * Environment variable required in Cloudflare Pages Dashboard:
 *   Settings → Environment Variables → Add:
 *   BREVO_API_KEY = your Brevo API key (free: 300 emails/day)
 *
 * Get your free key: https://app.brevo.com → Settings → SMTP & API → API Keys
 *
 * Endpoint: POST /api/contact
 */

const TO_EMAIL = 'info@rafeeg.ae';
const FROM_EMAIL = 'noreply@rafeeg.ae';
const FROM_NAME = 'رفيق — نموذج الموقع';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
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

    // Validate
    if (!name || !phone || !service) {
      return Response.json(
        { success: false, message: 'جميع الحقول مطلوبة' },
        { status: 400, headers: CORS_HEADERS }
      );
    }

    const cleanPhone = phone.replace(/[^\d+\s-]/g, '');
    if (cleanPhone.length < 7) {
      return Response.json(
        { success: false, message: 'رقم الهاتف غير صحيح' },
        { status: 400, headers: CORS_HEADERS }
      );
    }

    const timestamp = new Date().toLocaleString('ar-AE', { timeZone: 'Asia/Dubai' });
    const waLink = `https://wa.me/${cleanPhone.replace(/[\s\-\+]/g, '')}`;

    // Build email
    const emailHtml = `
<div dir="rtl" style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px">
  <div style="background:#189F18;color:white;padding:16px 24px;border-radius:12px 12px 0 0">
    <h2 style="margin:0;font-size:20px">🚿 طلب جديد — تركيب سيراميك حمامات في ${city || 'الإمارات'}</h2>
  </div>
  <div style="background:#f8f9fa;padding:24px;border:1px solid #e5e7eb;border-radius:0 0 12px 12px">
    <table style="width:100%;border-collapse:collapse;font-size:15px">
      <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280;width:100px">الاسم</td><td style="padding:10px 12px;font-size:17px;font-weight:bold">${name}</td></tr>
      <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الهاتف</td><td style="padding:10px 12px"><a href="tel:${cleanPhone}" style="color:#189F18;font-size:17px;font-weight:bold;text-decoration:none">${cleanPhone}</a></td></tr>
      <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الخدمة</td><td style="padding:10px 12px;font-weight:600">${service}</td></tr>
      <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">المدينة</td><td style="padding:10px 12px">${city || '—'}</td></tr>
      <tr><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الصفحة</td><td style="padding:10px 12px;font-size:13px"><a href="${page || '#'}" style="color:#2B5DF5">${page || '—'}</a></td></tr>
      <tr style="background:white"><td style="padding:10px 12px;font-weight:bold;color:#6b7280">الوقت</td><td style="padding:10px 12px">${timestamp}</td></tr>
    </table>
    <div style="margin-top:20px;text-align:center">
      <a href="${waLink}" style="display:inline-block;background:#25D366;color:white;padding:12px 32px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:16px">💬 واتساب</a>
      <a href="tel:${cleanPhone}" style="display:inline-block;background:#189F18;color:white;padding:12px 32px;border-radius:8px;font-weight:bold;text-decoration:none;font-size:16px;margin-right:10px">📞 اتصل</a>
    </div>
  </div>
  <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:12px">hub.rafeeg.ae — ${timestamp}</p>
</div>`;

    const BREVO_KEY = context.env.BREVO_API_KEY;

    if (!BREVO_KEY) {
      return Response.json(
        { success: false, message: 'Email service not configured. Set BREVO_API_KEY in Cloudflare Pages environment variables.' },
        { status: 500, headers: CORS_HEADERS }
      );
    }

    // Send via Brevo Transactional API
    const brevoRes = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'api-key': BREVO_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        sender: { name: FROM_NAME, email: FROM_EMAIL },
        to: [{ email: TO_EMAIL, name: 'Rafeeg' }],
        subject: `🚿 طلب جديد — سيراميك حمامات ${city || ''} — ${name}`,
        htmlContent: emailHtml,
        tags: ['hub-contact-form', 'bathroom-ceramic'],
      }),
    });

    if (brevoRes.ok || brevoRes.status === 201) {
      return Response.json(
        { success: true, message: 'تم الإرسال بنجاح' },
        { headers: CORS_HEADERS }
      );
    }

    const errBody = await brevoRes.text();
    console.error('Brevo error:', brevoRes.status, errBody);
    return Response.json(
      { success: false, message: 'فشل إرسال البريد، يرجى المحاولة لاحقاً' },
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
