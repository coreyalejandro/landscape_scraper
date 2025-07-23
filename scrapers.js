// Scraper functions module
const helpers = require('./helpers');

// Google Maps scraping implementation
async function scrapeGoogleMaps(browser, searchTerm, entityType, config) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1366, height: 768 });
  await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
  
  const results = [];
  
  try {
    helpers.log(`Navigating to Google Maps for: ${searchTerm}`, 'info', config);
    
    // Navigate to Google Maps with search term directly in URL
    const searchUrl = `https://www.google.com/maps/search/${encodeURIComponent(searchTerm)}`;
    await page.goto(searchUrl, { waitUntil: 'networkidle0', timeout: 60000 });
    
    // Wait a bit for page to load
    await helpers.delay(3000);
    
    // Try multiple selectors for results
    const resultSelectors = [
      'div[role="article"]',
      '.Nv2PK',
      '[data-result-index]',
      '.lI9IFe',
      'div[jsaction*="pane.resultGroup"]'
    ];
    
    let resultElements = null;
    for (const selector of resultSelectors) {
      try {
        await page.waitForSelector(selector, { timeout: 5000 });
        resultElements = await page.$$(selector);
        if (resultElements.length > 0) {
          helpers.log(`Found ${resultElements.length} results using selector: ${selector}`, 'info', config);
          break;
        }
      } catch (e) {
        helpers.log(`Selector ${selector} not found, trying next...`, 'info', config);
      }
    }
    
    if (!resultElements || resultElements.length === 0) {
      // Try text-based approach
      const pageContent = await page.content();
      if (pageContent.includes('property management') || pageContent.includes('hoa') || pageContent.includes('homeowner')) {
        helpers.log('Found relevant content but no structured results', 'info', config);
      } else {
        helpers.log('No relevant content found on page', 'info', config);
      }
      await page.close();
      return results;
    }
    
    // Process first 5 results
    const maxResults = Math.min(5, resultElements.length);
    
    for (let i = 0; i < maxResults; i++) {
      try {
        helpers.log(`Processing result ${i + 1}/${maxResults}`, 'info', config);
        
        // Re-get result elements before each click to ensure they're still valid
        resultElements = await page.$$(resultSelectors.find(s => s === '.Nv2PK') || resultSelectors[0]);
        
        // Check if we still have enough elements
        if (!resultElements[i]) {
          helpers.log(`Result ${i + 1} no longer available, skipping`, 'info', config);
          continue;
        }
        
        // Click on the result
        await resultElements[i].click();
        await helpers.delay(2000);
        
        // Extract business information
        const businessData = await page.evaluate(() => {
          const result = { name: '', address: '', phone: '', website: '' };
          
          // Try various selectors for business name
          const nameSelectors = [
            'h1',
            'h1[data-attrid="title"]', 
            '[data-attrid="title"]', 
            '.x3AX1-LfntMc-header-title-title',
            '.qBF1Pd',
            '.DUwDvf',
            '.SPZz6b'
          ];
          for (const selector of nameSelectors) {
            const element = document.querySelector(selector);
            if (element && element.textContent.trim() && element.textContent.trim() !== 'Results') {
              result.name = element.textContent.trim();
              break;
            }
          }
          
          // If no good name found, try to extract from URL or other sources
          if (!result.name || result.name === 'Results') {
            // Try to get name from page title
            const title = document.title;
            if (title && !title.includes('Google Maps')) {
              const titleParts = title.split(' - ');
              if (titleParts.length > 0 && titleParts[0].trim()) {
                result.name = titleParts[0].trim();
              }
            }
          }
          
          // Try to find address
          const addressSelectors = ['button[data-item-id="address"]', '[data-item-id="address"]', '.Io6YTe'];
          for (const selector of addressSelectors) {
            const element = document.querySelector(selector);
            if (element && element.textContent.trim()) {
              result.address = element.textContent.trim();
              break;
            }
          }
          
          // Try to find phone
          const phoneSelectors = ['button[data-item-id="phone"]', '[data-item-id="phone"]', '[aria-label*="phone"]'];
          for (const selector of phoneSelectors) {
            const element = document.querySelector(selector);
            if (element && element.textContent.trim()) {
              result.phone = element.textContent.trim();
              break;
            }
          }
          
          // Try to find website
          const websiteSelectors = ['a[data-item-id="authority"]', '[data-item-id="authority"]', 'a[aria-label*="website"]'];
          for (const selector of websiteSelectors) {
            const element = document.querySelector(selector);
            if (element && element.href) {
              result.website = element.href;
              break;
            }
          }
          
          return result;
        });
        
        if (businessData.name && businessData.name.length > 2) {
          businessData.entityType = helpers.determineEntityType(businessData.name);
          businessData.source = 'Google Maps';
          if (businessData.phone) {
            businessData.phone = helpers.formatPhoneNumber(businessData.phone);
          }
          results.push(businessData);
          helpers.log(`Extracted: ${businessData.name}`, 'info', config);
        }
        
        // Go back to results
        await page.goBack();
        await helpers.delay(1000);
        
        // Re-get result elements as DOM may have changed
        resultElements = await page.$$(resultSelectors.find(s => resultElements.length > 0) || resultSelectors[0]);
        
      } catch (error) {
        helpers.log(`Error processing result ${i + 1}: ${error.message}`, 'error', config);
        // Try to go back and continue
        try {
          await page.goBack();
          await helpers.delay(1000);
        } catch (navError) {
          // If navigation fails, break the loop
          break;
        }
      }
    }
    
    await page.close();
    return results;
    
  } catch (err) {
    helpers.log(`Google Maps scraping failed for "${searchTerm}": ${err.message}`, 'error', config);
    await page.close();
    return results;
  }
}

async function scrapeGoogleMapsSource(browser, source, config) {
  const results = [];
  const searchTerms = source.searchTerms[source.entityType] || source.searchTerms.hoa || source.searchTerms.propertyManagement;
  
  for (const searchTerm of searchTerms.slice(0, 2)) { // Limit to first 2 terms
    try {
      helpers.log(`Searching Google Maps for: ${searchTerm}`, 'info', config);
      const termResults = await scrapeGoogleMaps(browser, searchTerm, source.entityType, config);
      results.push(...termResults);
      await helpers.randomDelay(config);
    } catch (error) {
      helpers.log(`Error searching Google Maps for "${searchTerm}": ${error.message}`, 'error', config);
    }
  }
  
  return results;
}

// Standard source scraping - basic implementation
async function scrapeStandardSource(browser, source, config) {
  helpers.log(`Standard scraping not fully implemented for ${source.name}`, 'info', config);
  return []; // Return empty array for now
}

// Placeholder implementations that delegate to standard scraping
async function scrapeYelpSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeFindHoaSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeAllPropertyManagementSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeThumbTackSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeDbprLicenseSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeDirectSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

async function scrapeChamberSource(browser, source, config) {
  return await scrapeStandardSource(browser, source, config);
}

// Basic entity data extraction
async function extractEntityData(page, selectors, sourceConfig) {
  return []; // Basic implementation - return empty for now
}

module.exports = {
  scrapeGoogleMaps,
  scrapeGoogleMapsSource,
  scrapeStandardSource,
  scrapeYelpSource,
  scrapeFindHoaSource,
  scrapeAllPropertyManagementSource,
  scrapeThumbTackSource,
  scrapeDbprLicenseSource,
  scrapeDirectSource,
  scrapeChamberSource,
  extractEntityData
};