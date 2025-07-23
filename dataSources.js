// Data sources module
// Extensive list of data sources for both HOAs and Property Management companies

const dataSources = [
  // County property appraiser sources
  {
    name: 'Broward County Property Appraiser',
    region: 'broward',
    type: 'propertyAppraisers',
    entityType: 'both',
    url: 'https://web.bcpa.net/BcpaClient/#/Record-Search',
    searchTerms: {
      hoa: [
        'HOA', 'Homeowners Association', 'Condominium Association', 
        'Community Association', 'Residential Association', 'Property Owners'
      ],
      propertyManagement: [
        'Property Management', 'Property Manager', 'Real Estate Management',
        'Rental Management', 'Community Management'
      ]
    },
    selectors: {
      searchInput: '#search-term',
      searchButton: '.search-button',
      resultsList: '.results-container',
      paginationNext: '.pagination-next',
      resultInfo: '.property-details'
    }
  },
  {
    name: 'Miami-Dade County Property Appraiser',
    region: 'dade',
    type: 'propertyAppraisers',
    entityType: 'both',
    url: 'https://www.miamidade.gov/propertysearch/',
    searchTerms: {
      hoa: [
        'HOA', 'Homeowners Association', 'Condominium Association',
        'Community Association', 'Residential Association', 'Property Owners'
      ],
      propertyManagement: [
        'Property Management', 'Property Manager', 'Real Estate Management',
        'Rental Management', 'Community Management'
      ]
    },
    selectors: {
      searchInput: '#search-term',
      searchButton: '.search-button',
      resultsList: '.results-list',
      paginationNext: '.next-page',
      resultInfo: '.property-record'
    }
  },
  
  // State regulatory bodies
  {
    name: 'Florida DBPR - Division of Condominiums',
    region: 'all',
    type: 'dbpr',
    entityType: 'both',
    url: 'http://www.myfloridalicense.com/DBPR/condos-timeshares-mobile-homes/',
    searchTerms: {
      hoa: [
        'Broward', 'Miami-Dade', 'Miami', 'Fort Lauderdale', 'Hollywood',
        'Pompano Beach', 'Coral Springs', 'Miramar', 'Pembroke Pines'
      ],
      propertyManagement: [
        'Property Management Broward', 'Property Management Miami-Dade',
        'Community Association Management Broward', 'Community Association Management Miami'
      ]
    },
    selectors: {
      searchInput: '#search-term',
      searchButton: '.search-submit',
      resultsList: '.search-results',
      paginationNext: '.next',
      resultInfo: '.entity-details'
    }
  },
  {
    name: 'Florida DBPR - Business & Professional Regulation',
    region: 'all',
    type: 'dbpr',
    entityType: 'propertyManagement',
    url: 'https://www.myfloridalicense.com/wl11.asp?mode=0&SID=&brd=&typ=',
    specialType: 'dbprLicense',
    searchTerms: {
      propertyManagement: [
        'Community Association Manager', 'Property Manager',
        'Property Management', 'Real Estate Management'
      ]
    }
  },
  
  // HOA Directories
  {
    name: 'CAI Directory',
    region: 'all',
    type: 'directories',
    entityType: 'both',
    url: 'https://www.caionline.org/pages/default.aspx',
    searchTerms: {
      hoa: ['Florida', 'Broward', 'Miami-Dade', 'Miami'],
      propertyManagement: ['Property Management Florida', 'CAM Florida']
    },
    selectors: {
      searchInput: '#search-directory',
      searchButton: '.search-btn',
      resultsList: '.directory-results',
      paginationNext: '.pagination-next',
      resultInfo: '.directory-listing'
    }
  },
  {
    name: 'FindHOA.com',
    region: 'all',
    type: 'thirdParty',
    entityType: 'hoa',
    url: 'https://www.findhoa.com',
    searchTerms: {
      hoa: ['Florida', 'Broward', 'Miami-Dade', 'Miami']
    },
    specialType: 'findHoa'
  },
  
  // Property Management Directories
  {
    name: 'All Property Management',
    region: 'all',
    type: 'thirdParty',
    entityType: 'propertyManagement',
    url: 'https://www.allpropertymanagement.com',
    searchTerms: {
      propertyManagement: [
        'Fort Lauderdale, FL', 'Miami, FL', 'Hollywood, FL',
        'Pompano Beach, FL', 'Coral Springs, FL', 'Miramar, FL'
      ]
    },
    specialType: 'allPropertyManagement'
  },
  {
    name: 'Thumbtack Property Managers',
    region: 'all',
    type: 'thirdParty',
    entityType: 'propertyManagement',
    url: 'https://www.thumbtack.com',
    searchTerms: {
      propertyManagement: [
        'Property Managers Fort Lauderdale', 'Property Managers Miami',
        'Property Managers Hollywood FL', 'Property Managers Pompano Beach'
      ]
    },
    specialType: 'thumbtack'
  },
  
  // Sunbiz (Florida Division of Corporations)
  {
    name: 'Florida Division of Corporations',
    region: 'all',
    type: 'sunbiz',
    entityType: 'both',
    url: 'https://dos.myflorida.com/sunbiz/search/',
    searchTerms: {
      hoa: [
        'Homeowners Association Broward', 'Homeowners Association Miami-Dade',
        'Condominium Association Broward', 'Condominium Association Miami',
        'Community Association Broward', 'Community Association Miami',
        'Property Owners Association Broward', 'Property Owners Association Miami'
      ],
      propertyManagement: [
        'Property Management Broward', 'Property Management Miami-Dade',
        'Community Management Broward', 'Community Management Miami',
        'Real Estate Management Broward', 'Real Estate Management Miami'
      ]
    },
    selectors: {
      searchInput: '#search-term',
      searchButton: '.search-button',
      resultsList: '.search-results',
      paginationNext: '.next-page',
      resultInfo: '.entity-details'
    }
  },
  
  // Google Maps (requires special handling)
  {
    name: 'Google Maps - HOAs',
    region: 'all',
    type: 'googleMaps',
    entityType: 'hoa',
    url: 'https://www.google.com/maps',
    searchTerms: {
      hoa: [
        'homeowners association broward county', 'hoa miami-dade county',
        'condominium association fort lauderdale', 'homeowners association miami',
        'community association pompano beach', 'hoa hollywood florida',
        'condominium association coral gables', 'homeowners association miramar',
        'homeowners association pembroke pines', 'condo association hialeah'
      ]
    },
    specialType: 'googleMaps'
  },
  {
    name: 'Google Maps - Property Management',
    region: 'all',
    type: 'googleMaps',
    entityType: 'propertyManagement',
    url: 'https://www.google.com/maps',
    searchTerms: {
      propertyManagement: [
        'property management companies broward county', 'property managers miami-dade county',
        'property management fort lauderdale', 'property management miami',
        'property managers coral springs', 'property management hollywood florida',
        'property management company boca raton', 'property managers pompano beach',
        'rental property management companies miami', 'condo management companies broward'
      ]
    },
    specialType: 'googleMaps'
  },
  
  // Yelp
  {
    name: 'Yelp - HOAs',
    region: 'all',
    type: 'yelpPages',
    entityType: 'hoa',
    url: 'https://www.yelp.com',
    searchTerms: {
      hoa: [
        'homeowners association broward', 'hoa miami-dade',
        'condominium association miami', 'hoa fort lauderdale'
      ]
    },
    specialType: 'yelp'
  },
  {
    name: 'Yelp - Property Management',
    region: 'all',
    type: 'yelpPages',
    entityType: 'propertyManagement',
    url: 'https://www.yelp.com',
    searchTerms: {
      propertyManagement: [
        'property management fort lauderdale', 'property management miami',
        'property managers broward county', 'property management companies miami-dade',
        'rental management companies south florida', 'property management coral springs'
      ]
    },
    specialType: 'yelp'
  },
  
  // Real estate boards
  {
    name: 'Miami Association of Realtors',
    region: 'dade',
    type: 'realEstateBoards',
    entityType: 'propertyManagement',
    url: 'https://www.miamirealtors.com/property-management/',
    specialType: 'directScrape'
  },
  {
    name: 'Greater Fort Lauderdale Realtors',
    region: 'broward',
    type: 'realEstateBoards',
    entityType: 'propertyManagement',
    url: 'https://gflr.com/find-a-member/',
    specialType: 'directScrape'
  },
  
  // Chambers of Commerce
  {
    name: 'Greater Miami Chamber of Commerce',
    region: 'miami',
    type: 'chamberOfCommerce',
    entityType: 'both',
    url: 'https://www.miamichamber.com/membership/member-directory',
    specialType: 'chamberScrape'
  },
  {
    name: 'Greater Fort Lauderdale Chamber of Commerce',
    region: 'broward',
    type: 'chamberOfCommerce',
    entityType: 'both',
    url: 'https://www.ftlchamber.com/membership/member-directory',
    specialType: 'chamberScrape'
  }
];

module.exports = dataSources;
