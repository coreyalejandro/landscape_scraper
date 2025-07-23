// Configuration module
module.exports = {
  regions: {
    broward: true,
    dade: true,
    miami: true
  },
  entityTypes: {
    hoa: true,
    propertyManagement: true
  },
  sources: {
    propertyAppraisers: false,
    dbpr: false,
    directories: true,
    sunbiz: false,
    googleMaps: true,
    yelpPages: true,
    thirdParty: true,
    realEstateBoards: false,
    chamberOfCommerce: false
  },
  requestDelay: 2000,
  maxPages: 30,
  useProxies: false,
  proxies: [],
  maxRetries: 3,
  retryDelay: 5000,
  browserInstances: 2,
  headless: "new",
  outputPath: './results/data.json',
  exportCsvPath: './results/data.csv',
  exportDocPath: './results/data.doc',
  tempDataPath: './temp_data',
  logPath: './logs/scraper_log.txt',
  errorLogPath: './logs/error_log.txt',
  saveProgressInterval: 300000,
  disableImages: true,
  disableCSS: true,
  disableJavascript: false
};