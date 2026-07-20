/**
 * Origin Talent — Candidate Applications
 * Paste into: Extensions > Apps Script (inside this Google Sheet) > Code.gs
 * Then: Deploy > New deployment > type "Web app" > Execute as "Me" >
 *       Who has access "Anyone" > Deploy. Copy the Web App URL into
 *       SHEETS_ENDPOINTS.candidate in the website's <script> block.
 */
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date(),
    data.name || '',
    data.dob || '',
    data.idNumber || '',
    data.nationality || '',
    data.address || '',
    data.province || '',
    data.mobile || '',
    data.email || '',
    data.kinName || '',
    data.kinNumber || '',
    data.role || '',
    data.positionType || '',
    data.licence || '',
    data.transport || '',
    data.availability || '',
    data.skills || '',
    data.quals || '',
    data.languages || '',
    data.legal || '',
    data.able || '',
    data.screening || '',
    data.declare ? 'Yes' : 'No',
    data.popia ? 'Yes' : 'No'
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
