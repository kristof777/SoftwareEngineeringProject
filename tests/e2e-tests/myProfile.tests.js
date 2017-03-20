  beforeEach(function () {
      originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
      jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds

  });

  afterEach(function() {
      jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
  });

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
    });
    it ('Should go to myProfile page', function(done){
        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click();
        sleep();

        let email = element(by.id('settingsEmail')).all(by.tagName('input')).first();
        let firstName = element(by.id('settingsFirstName')).all(by.tagName('input')).first();
        let lastName = element(by.id('settingsLastName')).all(by.tagName('input')).first();
        let phoneNumber = element(by.id('settingsPhoneNumber')).all(by.tagName('input')).first();
        let secondPhoneNumber = element(by.id('settingsSecondPhoneNumber')).all(by.tagName('input')).first();
        let provinces = element(by.id('settingsProvince'));


        let city = element(by.id('settingsCity')).all(by.tagName('input')).first();

        email.sendKeys('test1@test.com');
        firstName.sendKeys('Tester #1');
        lastName.sendKeys('lastName');
        phoneNumber.sendKeys('3633126691');
        secondPhoneNumber.sendKeys('3065551234');
        provinces.click();
        sleep();

        selectProvince('Saskatchewan');

        city.sendKeys('Saskatoon');
        let saveButton = element(by.id('settingsSave'));
        saveButton.click();
        sleep();

        //let okButton2 = element(by.id('Ok'));
        //okButton2.click();
        //sleep();

        done();
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


/**
 * Force the browser to sleep for a specified amount of time.
 * @param {number} time - The amount of time to sleep (in milliseconds)
 */
function sleep(){
    browser.driver.sleep(1000);
}

/**
* Try to sign in with the expectation of a correct username and password
* @param {string} emailInput - the email field to input
* @param {string} passwordInput - the password field to input
*/
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

/**
* select a province from the dropdown list
* @param {String} province - the province to select
*/
function selectProvince(province){
        let provinceOption = element(by.buttonText(province));
        browser.executeScript("arguments[0].scrollIntoView();", provinceOption);
        provinceOption.click();
        sleep();
        let okButton = element(by.buttonText('OK'));
        okButton.click();
        sleep();

}
