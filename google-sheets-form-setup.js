/**
 * =====================================================
 * Google Apps Script — Paste this in Google Sheets
 * =====================================================
 *
 * SETUP STEPS:
 * 1. Create a new Google Sheet (or use existing)
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code, paste this entire file
 * 4. Click Deploy → New deployment
 *    - Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Click Deploy → Copy the URL
 * 6. Paste the URL in build_bathroom_ceramic_cities.py
 *    (replace GOOGLE_SHEETS_URL placeholder)
 *
 * The sheet will auto-create headers on first submission.
 * =====================================================
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Create headers if sheet is empty
    if (sheet.getLastRow() === 0) {
      sheet.appendRow([
        'التاريخ والوقت',
        'الاسم',
        'الهاتف',
        'الخدمة',
        'المدينة',
        'الصفحة',
        'الحالة'
      ]);
      // Bold + freeze header row
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold').setBackground('#189F18').setFontColor('white');
      sheet.setFrozenRows(1);
    }

    var data = JSON.parse(e.postData.contents);

    // Add row
    sheet.appendRow([
      new Date().toLocaleString('ar-AE', { timeZone: 'Asia/Dubai' }),
      data.name || '',
      data.phone || '',
      data.service || '',
      data.city || '',
      data.page || '',
      'جديد'
    ]);

    // Auto-resize columns
    sheet.autoResizeColumns(1, 7);

    // Send email notification to info@rafeeg.ae
    try {
      var subject = '🚿 طلب جديد — سيراميك حمامات ' + (data.city || '');
      var htmlBody = '<div dir="rtl" style="font-family:Arial,sans-serif;max-width:500px">'
        + '<div style="background:#189F18;color:white;padding:12px 20px;border-radius:10px 10px 0 0">'
        + '<h3 style="margin:0">🚿 طلب جديد — تركيب سيراميك حمامات</h3></div>'
        + '<div style="background:#f8f9fa;padding:20px;border:1px solid #e5e7eb;border-radius:0 0 10px 10px">'
        + '<p><b>الاسم:</b> ' + data.name + '</p>'
        + '<p><b>الهاتف:</b> <a href="tel:' + data.phone + '">' + data.phone + '</a></p>'
        + '<p><b>الخدمة:</b> ' + data.service + '</p>'
        + '<p><b>المدينة:</b> ' + (data.city || '—') + '</p>'
        + '<p><b>الصفحة:</b> <a href="' + (data.page || '#') + '">الرابط</a></p>'
        + '<div style="margin-top:16px;text-align:center">'
        + '<a href="https://wa.me/' + (data.phone || '').replace(/[\s\-\+]/g, '') + '" style="background:#25D366;color:white;padding:10px 24px;border-radius:8px;text-decoration:none;font-weight:bold">💬 واتساب</a>'
        + '</div></div></div>';

      GmailApp.sendEmail('info@rafeeg.ae', subject, '', { htmlBody: htmlBody });
    } catch (emailErr) {
      // Email failed but sheet row was saved — that's OK
      Logger.log('Email error: ' + emailErr);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ success: true, message: 'تم الإرسال بنجاح' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Handle GET requests (for testing)
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', message: 'Rafeeg contact form endpoint is active' }))
    .setMimeType(ContentService.MimeType.JSON);
}
