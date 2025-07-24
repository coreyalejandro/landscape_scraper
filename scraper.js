/**
 * South Florida HOA & Property Management Scraper
 * Main execution file using modular architecture
 */

// Required imports
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const AdblockerPlugin = require('puppeteer-extra-plugin-adblocker');
const AnonymizeUAPlugin = require('puppeteer-extra-plugin-anonymize-ua');
const UserAgent = require('user-agents');
const fs = require('fs-extra');
const path = require('path');
const Papa = require('papaparse');
const axios = require('axios');
const cheerio = require('cheerio');
const { createObjectCsvWriter } = require('csv-writer');

// Apply plugins
puppeteer.use(StealthPlugin());
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));
puppeteer.use(AnonymizeUAPlugin());

// Import modules
const config = require('./config');
const helpers = require('./helpers');
const dataSources = require('./dataSources');
const scrapers = require('./scrapers');

// Create required directories
fs.ensureDirSync(path.dirname(config.outputPath));
fs.ensureDirSync(path.dirname(config.logPath));
fs.ensureDirSync(config.tempDataPath);

// Main entry point
async function main() {
  helpers.log('South Florida HOA & Property Management Scraper started.', 'info', config);

  const allResults = [];
  const processedSources = new Set();
  let totalProcessed = 0;
  let totalErrors = 0;

  // Create browser instances based on config
  const browsers = [];
  try {
    for (let i = 0; i < config.browserInstances; i++) {
      helpers.log(`Launching browser instance ${i + 1}/${config.browserInstances}`, 'info', config);
      const browser = await puppeteer.launch({
        headless: config.headless,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--no-zygote',
          '--disable-gpu',
          '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows',
          '--disable-renderer-backgrounding'
        ]
      });
      browsers.push(browser);
    }

    // Filter data sources based on configuration
    const enabledSources = dataSources.filter(source => {
      // Check if source type is enabled
      if (!config.sources[source.type]) return false;

      // Check if region matches
      if (source.region !== 'all' && !config.regions[source.region]) return false;

      // Check if entity type is enabled
      if (source.entityType === 'hoa' && !config.entityTypes.hoa) return false;
      if (source.entityType === 'propertyManagement' && !config.entityTypes.propertyManagement) return false;

      return true;
    });

    helpers.log(`Found ${enabledSources.length} enabled data sources to process`, 'info', config);

    // Process each data source
    for (let sourceIndex = 0; sourceIndex < enabledSources.length; sourceIndex++) {
      const source = enabledSources[sourceIndex];
      const browserIndex = sourceIndex % browsers.length;
      const browser = browsers[browserIndex];

      helpers.log(`Processing source ${sourceIndex + 1}/${enabledSources.length}: ${source.name}`, 'info', config);

      try {
        let sourceResults = [];

        // Handle different types of sources
        switch (source.specialType) {
        case 'googleMaps':
          sourceResults = await scrapers.scrapeGoogleMapsSource(browser, source, config);
          break;
        case 'yelp':
          sourceResults = await scrapers.scrapeYelpSource(browser, source, config);
          break;
        case 'findHoa':
          sourceResults = await scrapers.scrapeFindHoaSource(browser, source, config);
          break;
        case 'allPropertyManagement':
          sourceResults = await scrapers.scrapeAllPropertyManagementSource(browser, source, config);
          break;
        case 'thumbtack':
          sourceResults = await scrapers.scrapeThumbTackSource(browser, source, config);
          break;
        case 'dbprLicense':
          sourceResults = await scrapers.scrapeDbprLicenseSource(browser, source, config);
          break;
        case 'directScrape':
          sourceResults = await scrapers.scrapeDirectSource(browser, source, config);
          break;
        case 'chamberScrape':
          sourceResults = await scrapers.scrapeChamberSource(browser, source, config);
          break;
        default:
          // Generic scraping for standard sources
          sourceResults = await scrapers.scrapeStandardSource(browser, source, config);
          break;
        }

        if (sourceResults && sourceResults.length > 0) {
          // Add source metadata
          sourceResults.forEach(result => {
            result.scrapedAt = new Date().toISOString();
            result.sourceType = source.type;
            result.sourceRegion = source.region;
          });

          allResults.push(...sourceResults);
          helpers.log(`Collected ${sourceResults.length} results from ${source.name}`, 'info', config);
        } else {
          helpers.log(`No results found for ${source.name}`, 'info', config);
        }

        processedSources.add(source.name);
        totalProcessed++;

        // Save progress periodically
        if (totalProcessed % 5 === 0) {
          await helpers.saveProgress(allResults, totalProcessed, enabledSources.length);
        }

        // Random delay between sources
        await helpers.randomDelay(config);

      } catch (error) {
        totalErrors++;
        helpers.log(`Error processing ${source.name}: ${error.message}`, 'error', config);

        // Continue with next source
        continue;
      }
    }

    // Process and clean results
    helpers.log('Processing and cleaning collected data...', 'info', config);
    const cleanedResults = await helpers.processResults(allResults);

    // Export results
    await helpers.exportResults(cleanedResults);

    // Generate summary report
    const summary = {
      totalSources: enabledSources.length,
      processedSources: processedSources.size,
      totalResults: cleanedResults.length,
      totalErrors: totalErrors,
      hoaCount: cleanedResults.filter(r => r.entityType === 'hoa').length,
      propertyManagementCount: cleanedResults.filter(r => r.entityType === 'propertyManagement').length,
      bothCount: cleanedResults.filter(r => r.entityType === 'both').length,
      unknownCount: cleanedResults.filter(r => r.entityType === 'unknown').length,
      withEmail: cleanedResults.filter(r => r.email).length,
      withPhone: cleanedResults.filter(r => r.phone).length,
      withWebsite: cleanedResults.filter(r => r.website).length,
      processedAt: new Date().toISOString()
    };

    helpers.log('\n=== SCRAPING SUMMARY ===', 'info', config);
    helpers.log(`Sources processed: ${summary.processedSources}/${summary.totalSources}`, 'info', config);
    helpers.log(`Total entities found: ${summary.totalResults}`, 'info', config);
    helpers.log(`HOAs: ${summary.hoaCount}`, 'info', config);
    helpers.log(`Property Management: ${summary.propertyManagementCount}`, 'info', config);
    helpers.log(`Both types: ${summary.bothCount}`, 'info', config);
    helpers.log(`Unknown type: ${summary.unknownCount}`, 'info', config);
    helpers.log(`With email: ${summary.withEmail}`, 'info', config);
    helpers.log(`With phone: ${summary.withPhone}`, 'info', config);
    helpers.log(`With website: ${summary.withWebsite}`, 'info', config);
    helpers.log(`Errors encountered: ${summary.totalErrors}`, 'info', config);

    // Save summary
    const summaryPath = './results/summary.json';
    await fs.writeJson(summaryPath, summary, { spaces: 2 });
    helpers.log(`Summary saved to ${summaryPath}`, 'info', config);

  } catch (error) {
    helpers.log(`Fatal error in main execution: ${error.message}`, 'error', config);
    throw error;
  } finally {
    // Close all browser instances
    helpers.log('Closing browser instances...', 'info', config);
    for (const browser of browsers) {
      try {
        await browser.close();
      } catch (closeError) {
        helpers.log(`Error closing browser: ${closeError.message}`, 'error', config);
      }
    }
  }

  helpers.log('South Florida HOA & Property Management Scraper completed successfully.', 'info', config);
}

// Run main if this file is executed directly
if (require.main === module) {
  main().catch(e => helpers.log(`Fatal error: ${e.message}`, 'error', config));
}
