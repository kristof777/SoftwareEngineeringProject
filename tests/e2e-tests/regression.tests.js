let originalTimeout;
beforeEach(function () {
    sleep(2000);
    originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
    jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
});

afterEach(function () {
    jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
});

describe('Regression tests: functionality while not signed in', function() {
    browser.get('');

    it('should test if multiple "My Profile" tab clicks removes all UI from the page', function(done) {
        let browseTab = element(by.id('tab-t0-0'));
        let myProfileTab = element(by.id('tab-t0-2'));

        browseTab.click().then(function(){
            let filterButton = element(by.id('goToFilters'));
            checkDisplayed(filterButton, "the 'Browse' page");
            myProfileTab.click().then(function(){
                let registerButton = element(by.css('.register'));
                for(i = 0; i < 10; i++)
                    myProfileTab.click();
                checkDisplayed(registerButton, "the 'Sign-In' page");
            });
        });
        done();
    });

    //TODO: Test if using Browse and Filter functionality allows a non-logged-in user to use My Profile or My Listings pages

    it('should test if "Confirm Password" field on register page allows incorrect matches', function(done) {
        let registerButton = element(by.css('.register'));
        registerButton.click().then(function(){
            sleep(1000);
            let email, password, confirmPassword, nextButton;
            email = element(by.id('signUpEmail')).all(by.tagName('input')).first();
            password = element(by.id('signUpPassword')).all(by.tagName('input')).first();
            confirmPassword = element(by.id('signUpConfirmPassword')).all(by.tagName('input')).first();
            nextButton = element(by.buttonText('Next'));
            email.sendKeys('test@test.com').then(function(){
                checkAttribute(email, "test@test.com");
            });
            password.sendKeys('Password123').then(function(){
                checkAttribute(password, "Password123");
            });
            confirmPassword.sendKeys('Password1234').then(function(){
                checkAttribute(confirmPassword, "Password1234");
            });
            nextButton.click().then(function(){
                checkDisplayed(nextButton, "the 'Browse' page");
                email.sendKeys().clear();
                password.sendKeys().clear();
                confirmPassword.sendKeys().clear();
            });

            let myProfileTab = element(by.id('tab-t0-2'));
            myProfileTab.click().then(function(){
                checkDisplayed(registerButton, "the 'Register' page");
            });
        });
        done();
    });
});

describe('Regression tests: functionality while signed in', function(){
    it('should test if a prompt is given after an incorrect login', function(done) {
        let email = element(by.id('email')).all(by.tagName('input')).first();
        let password = element(by.id('password')).all(by.tagName('input')).first();
        let signInButton = element(by.buttonText('Sign In'));
        email.sendKeys('test1@test.com').then(function(){
            checkAttribute(email, "test1@test.com");
        });
        password.sendKeys('WrongPassword').then(function(){
            checkAttribute(password, "WrongPassword");
        });
        signInButton.click();

        //Dismiss invalid credentials alert
        sleep(1000);
        let enter = browser.actions().sendKeys(protractor.Key.ENTER);
        enter.perform();
        sleep(1000);

        email.sendKeys().clear();
        password.sendKeys().clear();
        done();
    });

    it('should test if multiple "My Profile" tab clicks while signed-in returns user to Sign-In screen', function(done) {
        let email = element(by.id('email')).all(by.tagName('input')).first();
        let password = element(by.id('password')).all(by.tagName('input')).first();
        let signInButton = element(by.buttonText('Sign In'));
        checkDisplayed(signInButton, "the 'Register' page");
        email.sendKeys('test1@test.com').then(function(){
           checkAttribute(email, "test1@test.com");
        });

        password.sendKeys('123abcABC').then(function(){
            checkAttribute(password, "123abcABC");
            signInButton.click().then(function(){
                let filterButton = element(by.id('goToFilters'));
                sleep(1000);
                //todo Fix smoke test
                checkDisplayed(filterButton, "the 'Browse' page");
                let myProfileTab = element(by.id('tab-t0-2'));
                for(i = 0; i < 10; i++)
                    myProfileTab.click();
                let profileEmail = element(by.id('settingsEmail')).all(by.tagName('input')).first();
                checkDisplayed(profileEmail, "the 'My Profile' page");
            });
        });
        done();
    });
});

/**
 * Force the browser to sleep for a specified amount of time.
 * @param {number} time - The amount of time to sleep (in milliseconds)
 */
function sleep(time){
    browser.driver.sleep(time);
}

/**
 * Check if the input value was entered properly.
 * @param {element} element - The element with the value.
 * @param {string} expectedValue - The expected value that should be contained in the element input.
 */
function checkAttribute(element, expectedValue){
    sleep(1000);
    expect(element.getAttribute('value')).toContain(expectedValue);
}

/**
 * Check if the element is currently being displayed.
 * @param {element} element - The element to check.
 * @param {string} item - The item that should be displayed.
 */
function checkDisplayed(element, item){
    sleep(1000);
    expect(element.isDisplayed()).toBe(true, "Expected " + item + " to be displayed, but was not");
}
