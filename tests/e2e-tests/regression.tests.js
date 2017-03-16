describe('Regression tests: functionality while not signed in', function() {
    browser.get('');
    let originalTimeout;

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function () {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    it('should test if multiple "My Profile" tab clicks removes all UI from the page', function(done) {
        let browseTab = element(by.id('tab-t0-0'));
        let myProfileTab = element(by.id('tab-t0-2'));

        browseTab.click().then(function(){
            let filterButton = element(by.id('goToFilters'));
            expect(filterButton.isDisplayed()).toBe(true, 'Expected the "Browse" page to be displayed, but was not');
            myProfileTab.click().then(function(){
                let registerButton = element(by.css('.register'));
                for(i = 0; i < 10; i++)
                    myProfileTab.click();
                expect(registerButton.isDisplayed()).toBe(true, 'Expected the "Register" page to be displayed, but was not');
            });
        });
        done();
    });

    it('should test if "Confirm Password" field on register page allows incorrect matches', function(done) {
        let registerButton = element(by.css('.register'));
        registerButton.click();

        let email, password, confirmPassword, nextButton;
        email = element(by.id('signUpEmail')).all(by.tagName('input')).first();
        password = element(by.id('signUpPassword')).all(by.tagName('input')).first();
        confirmPassword = element(by.id('signUpConfirmPassword')).all(by.tagName('input')).first();
        nextButton = element(by.buttonText('Next'));

        email.sendKeys('test@test.com').then(function(){
            expect(email.getAttribute('value')).toContain("test@test.com");
        });
        password.sendKeys('Password123').then(function(){
            expect(password.getAttribute('value')).toContain("Password123");
        });
        confirmPassword.sendKeys('Password1234').then(function(){
            expect(confirmPassword.getAttribute('value')).toContain("Password1234");
        });
        nextButton.click().then(function(){
            expect(nextButton.isDisplayed()).toBe(true, 'Expected the "Browse" page to be displayed, but was not');
            email.sendKeys().clear();
            password.sendKeys().clear();
            confirmPassword.sendKeys().clear();
        });

        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click().then(function(){
            expect(registerButton.isDisplayed()).toBe(true, 'Expected the "Register" page to be displayed, but was not');
        });
        done();
    });
});

describe('Regression tests: functionality while signed in', function(){
    it('should test if a prompt is given after an incorrect login', function(done) {
        let email = element(by.id('email')).all(by.tagName('input')).first();
        let password = element(by.id('password')).all(by.tagName('input')).first();
        let signInButton = element(by.buttonText('Sign In'));
        email.sendKeys('test@usask.ca').then(function(){
            expect(email.getAttribute('value')).toContain("test@usask.ca");
        });
        password.sendKeys('WrongPassword').then(function(){
            expect(password.getAttribute('value')).toContain("WrongPassword");
        });
        signInButton.click();

        //Dismiss invalid credentials alert
        browser.driver.sleep(1000);
        let enter = browser.actions().sendKeys(protractor.Key.ENTER).perform();
        browser.driver.sleep(1000);

        email.sendKeys().clear();
        password.sendKeys().clear();
        done();
    });

    it('should test if multiple "My Profile" tab clicks while signed-in returns user to Sign-In screen', function(done) {
        let email = element(by.id('email')).all(by.tagName('input')).first();
        let password = element(by.id('password')).all(by.tagName('input')).first();
        let signInButton = element(by.buttonText('Sign In'));
        expect(email.isDisplayed()).toBe(true, 'Expected the "Register" page to be displayed, but was not');

        email.sendKeys('test@usask.ca').then(function(){
            expect(email.getAttribute('value')).toContain("test@usask.ca");
        });
        password.sendKeys('Password123').then(function(){
            expect(password.getAttribute('value')).toContain("Password123");
        });

        signInButton.click().then(function(){
            let filterButton = element(by.id('goToFilters'));
            browser.driver.sleep(1000);
            expect(filterButton.isDisplayed()).toBe(true, 'Expected the "Browse" page to be displayed, but was not');
            let myProfileTab = element(by.id('tab-t0-2'));
            for(i = 0; i < 10; i++)
                myProfileTab.click();
            let profileEmail = element(by.id('settingsEmail')).all(by.tagName('input')).first();
            expect(profileEmail.isDisplayed()).toBe(true, 'Expected the "My Profile" page to be displayed, but was not');
        });
        done();
    });
});
