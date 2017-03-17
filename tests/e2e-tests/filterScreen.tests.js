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

    //filter options
    let provDrop = element(by.id('flProv'));
    //The css is the generated css made by ionic copied from firefox inspect
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

    // This was the test for clicking outside the filter model it is no longer needed
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
    /*
    Fills in the filter model selections as described in the Filter Use Case
     */
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


        //select SK in Provinces Menu
        sleep();
        provDrop.click();
        sleep();

        //The province Drop menu

        let YTBtn = element(by.buttonText('Yukon'));
        browser.executeScript("arguments[0].scrollIntoView();", YTBtn); //Sask needs to be in view to click
        YTBtn.click();

        let okBtn = element(by.buttonText('OK'));
        okBtn.click();
        sleep();
        //These drag the sliders a certain distance X from the opposite end the slider started
        //for example the max will go to min and min towards max

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
    /*
    Puts the browser to sleep to allow the website to load before protractor performs an action
     */
    function sleep(){
        browser.driver.sleep(500);
    }
});
