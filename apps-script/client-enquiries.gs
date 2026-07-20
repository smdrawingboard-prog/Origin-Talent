/**
 * Origin Talent — Client Staffing Enquiries
 * Paste into: Extensions > Apps Script (inside this Google Sheet) > Code.gs
 * Then: Deploy > New deployment > type "Web app" > Execute as "Me" >
 *       Who has access "Anyone" > Deploy. Copy the Web App URL into
 *       SHEETS_ENDPOINTS.client in the website's <script> block.
 */
function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var data = JSON.parse(e.postData.contents);

  sheet.appendRow([
    new Date(),
    data.name || '',
    data.company || '',
    data.email || '',
    data.mobile || '',
    data.altPhone || '',
    data.contactMethod || '',
    data.address || '',
    data.role || '',
    data.employmentType || '',
    data.arrangement || '',
    data.hours || '',
    data.urgency || '',
    data.salary || '',
    data.driving || '',
    data.languages || '',
    data.days || '',
    data.duties || '',
    data.notes || '',
    data.popia ? 'Yes' : 'No'
  ]);

  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok' }))
    .setMimeType(ContentService.MimeType.JSON);
}
