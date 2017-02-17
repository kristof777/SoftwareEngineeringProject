describe('Add Listing Test',function(){
    let originalTimeout;
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });
    //hello 
    it('Should login', function(done){
        let username, password, registerButton, signInButton;
        registerButton = element(by.css('.register'));
        signInButton = element(by.buttonText('Sign In'));
        username = element(by.id('email')).all(by.tagName('input')).first();
        password = element(by.id('password')).all(by.tagName('input')).first();
        username.sendKeys('test');
        password.sendKeys('Password1');
        signInButton.click();
        browser.driver.sleep(500);
        done();
    });

    it('Should Go to My Listings', function(done){
     let myListings = element(by.id('tab-t0-1'));
     myListings.click();
     browser.driver.sleep(500);

     done();
    });
    it('Add a New Listing', function(done){

        let btnNewListing = element(by.id('addButton'));
        btnNewListing.click();

        browser.driver.sleep(500);

        let provinceDropList = element(by.id('alProvince'));
        provinceDropList.click();

        browser.driver.sleep(500);

        let skOption = element(by.buttonText('Saskatchewan'));
        browser.executeScript("arguments[0].scrollIntoView();", skOption);
        skOption.click();
        browser.driver.sleep(500);
        let okaybtn = element(by.buttonText('OK'));
        okaybtn.click();
        browser.driver.sleep(5000);

        let city = element(by.id('alCityTown')).all(by.tagName('input')).first();
        city.sendKeys('Saskatoon');

        let address = element(by.id('alAddress')).all(by.tagName('input')).first();
        address.sendKeys('123 First Street East');

        let postalCode = element(by.id('alPostalCode')).all(by.tagName('input')).first();
        postalCode.sendKeys('f1s 9u8');

        let price = element(by.id('alPrice')).all(by.tagName('input')).first();
        price.sendKeys('13000000');

        let feet = element(by.id('alSqFeet')).all(by.tagName('input')).first();
        feet.sendKeys('600');

        let bed = element(by.id('alBed')).all(by.tagName('input')).first();
        bed.sendKeys('5');

        let bath = element(by.id('alBathRoom')).all(by.tagName('input')).first();
        bath.sendKeys('2');

        let desc = element(by.id('alDesc')).all(by.tagName('input')).first();
        desc.sendKeys('Nice trailer with a little dust. Fixer Upper.');


        browser.driver.sleep(500);
        done();
    });
});
