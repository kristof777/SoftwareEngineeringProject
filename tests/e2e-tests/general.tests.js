describe('Signing in, and using the app like a user would interact with it', function() {
    var username, password, registerButton, signInButton;
    var originalTimeout;
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    it('Should login', function(done){
        registerButton = element(by.css('.register'));
        signInButton = element(by.buttonText('Sign In'));
        username = element(by.id('emailLogin'));
        browser.driver.sleep(5000);
        username.click();
        //username = element(by.css('[id="emailLogin"]'));
        browser.driver.sleep(1000);
        //username.sendKeys('test');
        //browser.driver.sleep(1000);
        //username.evaluate("email = 'test';");
        //username.clear().sendKeys('test');
        browser.driver.sleep(1000);
        signInButton.click();
        browser.driver.sleep(500);
        done();
    });

    it('Should test the filter screen on the browse page', function (done) {
        var filtersButton = element(by.id('goToFilters'));
        filtersButton.click();
        browser.driver.sleep(500);
        var applyFilterButton = element(by.buttonText('Apply Filter'));
        var sqftRange = element(by.id('sqftRange'));
        var bedRange = element(by.id('bedRange'));
        browser.actions().dragAndDrop(sqftRange,{x:50,y:0}).perform();
        browser.actions().dragAndDrop(sqftRange,{x:-70,y:0}).perform();
        browser.actions().dragAndDrop(bedRange,{x:40,y:0}).perform();
        browser.actions().dragAndDrop(bedRange,{x:-130, y:0}).perform(); // Unable to figure out how to move min slider
        browser.driver.sleep(500);

        var provinceDropList = element(by.id('provinceSelect')).click();
        var ykOption = element(by.buttonText('Yukon'));
        var abOption = element(by.buttonText('Alberta'));
        var bcOption = element(by.buttonText('British Columbia'));
        var nbOption = element(by.buttonText('New Brunswick'));
        var nlOption = element(by.buttonText('Newfoundland and Labrador'));
        var provFilterOK = element(by.buttonText('OK'));
        browser.executeScript("arguments[0].scrollIntoView();", ykOption);
        //expect(abOption.isPresent()).toBe(true);
        browser.driver.sleep(500);
        ykOption.click();
        //browser.driver.sleep(800);
        browser.executeScript("arguments[0].scrollIntoView();", abOption);
        browser.driver.sleep(500);
        abOption.click();
        bcOption.click();
        nbOption.click();
        provFilterOK.click();
        browser.driver.sleep(500);
        provinceDropList.click();
        browser.driver.sleep(500);
        bcOption.click();
        abOption.click();
        nlOption.click();
        provFilterOK.click(); // Used in place of the provFilterCancel until fixed
        browser.driver.sleep(500);
        applyFilterButton.click();
        browser.driver.sleep(500);
        filtersButton.click();
        browser.driver.sleep(500);
        var cancelFilterButton = element(by.buttonText('Cancel')).click();
        browser.driver.sleep(800);
        done();
    });

    it('Should test the next/previous property buttons, like/dislike buttons, and scrolling on browse page', function(done){
        var rightArrowButton = element(by.id('nextProperty'));
        var leftArrowButton = element(by.id('previousProperty'));
        var likeButton = element(by.id('likeButton'));
        var unlikeButton = element(by.id('unlikeButton'));
        var description = element(by.id('description'));
        for(i=0; i<50; i++)
        {
            rightArrowButton.click();
            if(i%5 == 0)
            {
                browser.executeScript("arguments[0].scrollIntoView();", description);
                browser.driver.sleep(100);
                browser.executeScript("arguments[0].scrollIntoView();", likeButton);
                likeButton.click();
            }
        }
        for(i=0; i<50; i++)
        {
            leftArrowButton.click();
            if(i%10 == 0)
            {
                browser.executeScript("arguments[0].scrollIntoView();", description);
                browser.driver.sleep(100);
                browser.executeScript("arguments[0].scrollIntoView();", likeButton);
                unlikeButton.click();
            }
        }
        done();
    });

    /* If you uncomment this, remember to click on the settings tab during the test
    it('Should test the settings page', function(done){
        browser.driver.sleep(5000);
        var changePW = element(by.buttonText('Change Password'));
        changePW.click();
        browser.driver.sleep(500);
        var cancel = element(by.buttonText('Cancel'));
        cancel.click();
        done();
    });
    */

});
