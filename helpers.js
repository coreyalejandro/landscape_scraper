const Papa = require('papaparse');
const fs = require('fs-extra');
const path = require('path');
const { createObjectCsvWriter } = require('csv-writer');

function getRandomUserAgent() {
  return new UserAgent({ deviceCategory: 'desktop' }).toString();
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function randomDelay(config) {
  const min = config.requestDelay * 0.75;
  const max = config.requestDelay * 1.25;
  const delayTime = Math.floor(Math.random() * (max - min + 1)) + min;
  await delay(delayTime);
}

function log(message, type = 'info', config) {
  const timestamp = new Date().toISOString();
  const logFilePath = type === 'error' ? config.errorLogPath : config.logPath;
  const logDir = path.dirname(logFilePath);
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  fs.appendFileSync(logFilePath, `[${timestamp}] ${message}\n`, { encoding: 'utf8', flag: 'a' });
  console.log(`[${timestamp}] ${message}`);
}

function formatPhoneNumber(phone) {
  if (!phone) return '';
  const cleaned = phone.replace(/\D/g, '');
  if (cleaned.length === 10) {
    return `(${cleaned.substring(0, 3)}) ${cleaned.substring(3, 6)}-${cleaned.substring(6)}`;
  } else if (cleaned.length === 11 && cleaned.charAt(0) === '1') {
    return `(${cleaned.substring(1, 4)}) ${cleaned.substring(4, 7)}-${cleaned.substring(7)}`;
  }
  return phone;
}

function isValidEmail(email) {
  if (!email) return false;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.trim());
}

function extractContactInfo(text) {
  if (!text) return {};
  const result = {};
  const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g;
  const emails = text.match(emailRegex);
  if (emails && emails.length > 0) {
    result.email = emails[0].toLowerCase();
  }
  const phoneRegex = /(?:\+?1[-\s]?)?\(?([0-9]{3})\)?[-\s]?([0-9]{3})[-\s]?([0-9]{4})/g;
  const phones = text.match(phoneRegex);
  if (phones && phones.length > 0) {
    result.phone = formatPhoneNumber(phones[0]);
  }
  return result;
}

function determineEntityType(name, description = '') {
  const text = (name + ' ' + description).toLowerCase();
  const hoaIndicators = [
    'homeowners association', 'hoa', 'condominium association', 'condo association',
    'community association', 'property owners association', 'townhome association',
    'residential association', 'neighborhood association'
  ];
  const pmIndicators = [
    'property management', 'property manager', 'real estate management',
    'community management', 'rental management', 'property services',
    'realty management', 'rental services', 'leasing services',
    'landlord services', 'real estate services'
  ];
  const isHoa = hoaIndicators.some(indicator => text.includes(indicator));
  const isPm = pmIndicators.some(indicator => text.includes(indicator));
  if (isHoa && !isPm) return 'hoa';
  if (isPm && !isHoa) return 'propertyManagement';
  if (isHoa && isPm) return 'both';
  if (name.match(/\b(estates|village|community|garden|towers|lake|place|terrace|club|hills|palms)\b/i)) {
    return 'hoa';
  }
  if (name.match(/\b(realty|properties|management|services|rental|leasing)\b/i)) {
    return 'propertyManagement';
  }
  return 'unknown';
}

async function processResults(results) {
  // Remove duplicates by name + address (case-insensitive)
  const seen = new Set();
  const cleaned = [];
  for (const r of results) {
    const key = (r.name || '').toLowerCase() + '|' + (r.address || '').toLowerCase();
    if (!seen.has(key)) {
      seen.add(key);
      cleaned.push(r);
    }
  }
  return cleaned;
}

async function exportResults(results) {
  const config = require('./config');
  await fs.writeJson(config.outputPath, results, { spaces: 2 });
  // Export CSV
  const csvWriter = createObjectCsvWriter({
    path: config.exportCsvPath,
    header: [
      { id: 'name', title: 'Name' },
      { id: 'address', title: 'Address' },
      { id: 'phone', title: 'Phone' },
      { id: 'email', title: 'Email' },
      { id: 'website', title: 'Website' },
      { id: 'entityType', title: 'Entity Type' },
      { id: 'scrapedAt', title: 'Scraped At' },
      { id: 'sourceType', title: 'Source Type' },
      { id: 'sourceRegion', title: 'Source Region' }
    ]
  });
  await csvWriter.writeRecords(results);
}

async function saveProgress(results, processed, total) {
  const config = require('./config');
  const progress = {
    processed,
    total,
    timestamp: new Date().toISOString(),
    results
  };
  await fs.writeJson(config.tempDataPath + '/progress.json', progress, { spaces: 2 });
}

module.exports = {
  getRandomUserAgent,
  delay,
  randomDelay,
  log,
  formatPhoneNumber,
  isValidEmail,
  extractContactInfo,
  determineEntityType,
  processResults,
  exportResults,
  saveProgress
};
