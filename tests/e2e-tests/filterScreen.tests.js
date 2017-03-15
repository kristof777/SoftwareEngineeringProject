describe('Filter Listings',function(){
    let originalTimeout;

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
    let provDrop = element(by.id('flProv'));

    let priceSliderMin = element(by.id('flPrice')).element(by.css('#flPrice > div:nth-child(2) > div:nth-child(3)'));
    let priceSliderMax = element(by.id('flPrice'));

    let sqftSliderMin = element(by.id('flSqft')).element(by.css('#flSqft > div:nth-child(2) > div:nth-child(3)'));
    let sqftSliderMax = element(by.id('flSqft'));

    let bedSliderMin = element(by.id('flBed')).element(by.css('#flBed > div:nth-child(2) > div:nth-child(13)'));
    let bedSliderMax = element(by.id('flBed'));

    let bathSliderMin = element(by.id('flBath')).element(by.css('#flBath > div:nth-child(2) > div:nth-child(13)'));
    let bathSliderMax = element(by.id('flBath'));

    // apply and cancel filter
    let applyBtn = element(by.id('flApply'));
    let cancelBtn = element(by.id('flCancel'));


    it('should filter with nothing', function(done){

        sleep();
        filtersBtn.click();

        sleep();
        applyBtn.click();

        sleep();

        //TODO: when filter updates results add an expect that results have not changed
        done();
    });

    it('should filter then cancel', function (done) {
        //open filters
        sleep();
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
        sleep();
        filtersBtn.click();

        //select filter options
        selectFilterOptions();

        //click outside of popup
        browser.actions().mouseMove({x: 300, y: 100}).doubleClick().perform();
        sleep();

        //TODO: when filter updates results add an expect that results have not changed
        done();
    });
    */
    it('should filter then press apply filter', function(done){

        //open filters
        sleep();
        filtersBtn.click();

        //select filter options
        selectFilterOptions();

        //click apply filter
        applyBtn.click();

        //TODO: When filter updates results add an expect that results equal what is filtered
        done();
    });

    function selectFilterOptions (){
        //set up the x coord for sliders
        let priceMax =70;
        let priceMin =80;

        let sqftMax =60;
        let sqftMin =70;

        let bedMax =100;
        let bedMin =60;

        let bathMax =80;
        let bathMin =80;


        //select AB and SK in Provinces Menu
        sleep();
        provDrop.click();
        sleep();

        //The province Drop menu
        let ABBtn = element(by.buttonText('Alberta'));
        ABBtn.click();

        let SKBtn = element(by.buttonText('Saskatchewan'));
        browser.executeScript("arguments[0].scrollIntoView();", SKBtn); //Sask needs to be in view to click
        SKBtn.click();

        let okBtn = element(by.buttonText('OK'));
        okBtn.click();
        sleep();

        //select price range from 100k to 1.3Mil
        browser.actions().dragAndDrop(priceSliderMax,{x:priceMax,y:0}).perform();
        browser.actions().dragAndDrop(priceSliderMin,{x:priceMin,y:0}).perform();

        //select sqft range from 100 to 100000
        browser.actions().dragAndDrop(sqftSliderMax,{x:sqftMax,y:0}).perform();
        browser.actions().dragAndDrop(sqftSliderMin,{x:sqftMin,y:0}).perform();

        //select beds range from 2 to 8
        browser.actions().dragAndDrop(bedSliderMax,{x:bedMax,y:0}).perform();
        browser.actions().dragAndDrop(bedSliderMin,{x:bedMin,y:0}).perform();

        //select bath range from 3 to 7
        browser.actions().dragAndDrop(bathSliderMax,{x:bathMax,y:0}).perform();
        browser.actions().dragAndDrop(bathSliderMin,{x:bathMin,y:0}).perform();

        sleep();
    }
    function sleep(){
        browser.driver.sleep(500);
    }
});
