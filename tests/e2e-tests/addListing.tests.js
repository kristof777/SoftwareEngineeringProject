  beforeEach(function () {
      originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
      jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds

  });

  afterEach(function() {
      jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
  });

  describe('Adding and saving a listing as a user would', function() {
      let originalTimeout;
      browser.get('/#/ionic-lab');

  it('Should sign in', function(){

      // testing "add listing" functionality
      sleep();

        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click().then(function(){
            let signInButton = element(by.buttonText('Sign In'));
            checkDisplayed(signInButton, "The 'Sign In' page ");

        });

        attemptSignIn('test1@test.com', '123abcABC');
        sleep();

        expect(element(by.id('goToFilters'))).isDisplayed;
   });

    it ('Should go to add listing page', function(){
        let myListings = element(by.id('tab-t0-3'));
        myListings.click();
        sleep();
        sleep();


        let addListingButton= element(by.id('addButton'));
        addListingButton.click();
        sleep();
        sleep();

        expect(element(by.buttonText('Add Image')).getText()).toEqual('ADD IMAGE');
    });

    it ('Should add a listing', function(done){
        let provinceDropList = element(by.id('alProvince'));
        provinceDropList.click();

        sleep();

        /*let skOption = element(by.buttonText('Saskatchewan'));
        browser.executeScript("arguments[0].scrollIntoView();", skOption);
        skOption.click();
        sleep();
        let okaybtn = element(by.buttonText('OK'));
        okaybtn.click();
      */  sleep();

      selectProvince('Saskatchewan');

        let bath = element(by.id('alBathroom')).all(by.tagName('input')).first();


        let city = element(by.id('alCityTown')).all(by.tagName('input')).first();
        city.sendKeys('Saskatoon');

        let address = element(by.id('alAddress')).all(by.tagName('input')).first();
        address.sendKeys('123 First Street East');

        let postalCode = element(by.id('alPostalCode')).all(by.tagName('input')).first();
        postalCode.sendKeys('f1s 9u8');

        browser.executeScript("arguments[0].scrollIntoView();", bath);

        let price = element(by.id('alPrice')).all(by.tagName('input')).first();
        price.sendKeys('13000000');

        let feet = element(by.id('alSqft')).all(by.tagName('input')).first();
        feet.sendKeys('600');

        let bed = element(by.id('alBedroom')).all(by.tagName('input')).first();
        bed.sendKeys('5');

        bath.sendKeys('2');

        sleep();

        let desc2 = element(by.id('alDesc')).all(by.tagName('textarea')).first();
        sleep();
        desc2.sendKeys('Nice trailer with a little dust. Fixer Upper.');

        let saveButton = element(by.id('alSave'));
        saveButton.click();

        sleep();
        done();

        });


});


/**
 * Check if the input value was entered properly.
 * @param {element} element - The element with the value.
 * @param {string} expectedValue - The expected value that should be contained in the element input.
 */
function checkAttribute(element, expectedValue){
    expect(element.getAttribute('value')).toContain(expectedValue);
}

/**
 * Check if the element is currently being displayed.
 * @param {element} element - The element to check.
 * @param {string} item - The item that should be displayed.
 */
function checkDisplayed(element, item){
    expect(element.isDisplayed()).toBe(true, "Expected " + item + " to be displayed, but was not");
}

function sleep(){
    browser.driver.sleep(1000);
}

function attemptSignIn(emailInput, passwordInput){
    let email = element(by.id('email')).all(by.tagName('input')).first();
    let password = element(by.id('password')).all(by.tagName('input')).first();
    let signInButton = element(by.buttonText('Sign In'));

    email.sendKeys().clear();
    password.sendKeys().clear();
    email.sendKeys(emailInput);
    password.sendKeys(passwordInput);
    signInButton.click();

}

function selectProvince(province){
        let provinceOption = element(by.buttonText(province));
        browser.executeScript("arguments[0].scrollIntoView();", provinceOption);
        provinceOption.click();
        sleep();
        let okButton = element(by.buttonText('OK'));
        okButton.click();
        sleep();

}
