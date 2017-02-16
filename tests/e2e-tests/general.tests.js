describe('Signing in, and using the app like a user would interact with it', function() {
    let originalTimeout;
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    it('Should login', function(done){
        let username, password, registerButton, signInButton;
        registerButton = element(by.css('.register'));
        signInButton = element(by.buttonText('Sign In'));
        username = element(by.id('email')).all(by.tagName('input')).first();
        password = element(by.id('password')).all(by.tagName('input')).first();
        username.sendKeys('test');
        password.sendKeys('somePassword');
        signInButton.click();
        browser.driver.sleep(500);
        done();
    });

    it('Should test the filter screen on the browse page', function (done) {
        let filtersButton, applyFilterButton, sqftRange, bedRange, provinceDropList, ykOption, abOption, bcOption, nbOption, nlOption, provFilterOK, cancelFilterButton;
        filtersButton = element(by.id('goToFilters'));
        filtersButton.click();
        browser.driver.sleep(500);
        applyFilterButton = element(by.buttonText('Apply Filter'));
        sqftRange = element(by.id('sqftRange'));
        bedRange = element(by.id('bedRange'));
        browser.actions().dragAndDrop(sqftRange,{x:50,y:0}).perform();
        browser.actions().dragAndDrop(sqftRange,{x:-70,y:0}).perform();
        browser.actions().dragAndDrop(bedRange,{x:40,y:0}).perform();
        browser.actions().dragAndDrop(bedRange,{x:-130, y:0}).perform(); // Unable to figure out how to move min slider
        browser.driver.sleep(500);

        provinceDropList = element(by.id('provinceSelect')).click();
        ykOption = element(by.buttonText('Yukon'));
        abOption = element(by.buttonText('Alberta'));
        bcOption = element(by.buttonText('British Columbia'));
        nbOption = element(by.buttonText('New Brunswick'));
        nlOption = element(by.buttonText('Newfoundland and Labrador'));
        provFilterOK = element(by.buttonText('OK'));
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
        cancelFilterButton = element(by.buttonText('Cancel'));
        cancelFilterButton.click();
        browser.driver.sleep(800);
        done();
    });

    it('Should test the next/previous property buttons, like/dislike buttons, and scrolling on browse page', function(done){
        let rightArrowButton = element(by.id('nextProperty'));
        let leftArrowButton = element(by.id('previousProperty'));
        let likeButton = element(by.id('likeButton'));
        let unlikeButton = element(by.id('unlikeButton'));
        let description = element(by.id('description'));
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
     let changePW = element(by.buttonText('Change Password'));
     changePW.click();
     browser.driver.sleep(500);
     let cancel = element(by.buttonText('Cancel'));
     cancel.click();
     done();
     });
     */

});
