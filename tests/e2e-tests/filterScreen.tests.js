describe('Filter Listings',function(){
    let originalTimeout;
    //TODO don't need this boi
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    //Button to open the filters menu
    let filtersBtn = element(by.id('goToFilters'));
    //button to open myListings

    //filter options
    let provDrop = element(by.id('FlProv'));
    //TODO Use naming convention
    let priceSliderMin = element(by.id('FlPrice')).element(by.css('#FlPrice > div:nth-child(2) > div:nth-child(3)'));
    let priceSliderMax = element(by.id('FlPrice'));

    let SqftSliderMin = element(by.id('FlSqft')).element(by.css('#FlSqft > div:nth-child(2) > div:nth-child(3)'));
    let SqftSliderMax = element(by.id('FlSqft'));

    let BedSliderMin = element(by.id('FlBed')).element(by.css('#FlBed > div:nth-child(2) > div:nth-child(13)'));
    let BedSliderMax = element(by.id('FlBed'));
    //TODO fix id names to be all capitalized at first character
    let BathSliderMin = element(by.id('flBath')).element(by.css('#flBath > div:nth-child(2) > div:nth-child(13)'));
    let BathSliderMax = element(by.id('flBath'));

    // apply and cancel filter
    let applyBtn = element(by.id('flApply'));
    let cancelBtn = element(by.id('flCancel'));


    it('should filter with nothing', function(done){
        //TODO make macro for sleep time
        browser.driver.sleep(500);
        filtersBtn.click();

        browser.driver.sleep(500);
        applyBtn.click();

        browser.driver.sleep(500);

        //TODO: when filter updates results add an expect that results have not changed
        done();
    });

    it('should filter then cancel', function (done) {
        //open filters
        
        
        browser.driver.sleep(500);
        filtersBtn.click();

        selectFilterOptions();

        cancelBtn.click();

        //TODO: when filter updates results add an expect that results have not changed
        done();
    });

    // There is an issue with clicking outside of the filter screen
    /*
    it('should filter then click outside Filter Menu', function(done){

        //open filters
        browser.driver.sleep(500);
        filtersBtn.click();

        //select filter options
        selectFilterOptions();

        //click outside of popup
        browser.actions().mouseMove({x: 300, y: 100}).doubleClick().perform();
        browser.driver.sleep(500);

        //TODO: when filter updates results add an expect that results have not changed
        done();
    });
    */
    it('should filter then press apply filter', function(done){

        //open filters
        browser.driver.sleep(500);
        filtersBtn.click();

        //select filter options
        selectFilterOptions();

        //click apply filter
        applyBtn.click();

        //TODO: When filter updates results add an expect that results equal what is filtered
        done();
    });

    function selectFilterOptions (){
        //select AB and SK in Provinces Menu
        browser.driver.sleep(500);
        provDrop.click();
        browser.driver.sleep(500);

        //The province Drop menu
        let abBtn = element(by.buttonText('Alberta'));
        abBtn.click();

        let skBtn = element(by.buttonText('Saskatchewan'));
        browser.executeScript("arguments[0].scrollIntoView();", skBtn); //Sask needs to be in view to click
        skBtn.click();
        //TODO fix this name for "okaybtn" consistency
        let okaybtn = element(by.buttonText('OK'));
        okaybtn.click();
        browser.driver.sleep(500);
        // Make the x and y stuff macros
        //select price range from 100k to 1.3Mil
        browser.actions().dragAndDrop(priceSliderMax,{x:70,y:0}).perform();
        browser.actions().dragAndDrop(priceSliderMin,{x:80,y:0}).perform();

        //select sqft range from 100 to 100000
        browser.actions().dragAndDrop(SqftSliderMax,{x:60,y:0}).perform();
        browser.actions().dragAndDrop(SqftSliderMin,{x:70,y:0}).perform();

        //select beds range from 2 to 8
        browser.actions().dragAndDrop(BedSliderMax,{x:100,y:0}).perform();
        browser.actions().dragAndDrop(BedSliderMin,{x:60,y:0}).perform();

        //select bath range from 3 to 7
        browser.actions().dragAndDrop(BathSliderMax,{x:80,y:0}).perform();
        browser.actions().dragAndDrop(BathSliderMin,{x:80,y:0}).perform();

        browser.driver.sleep(500);
    }
});
