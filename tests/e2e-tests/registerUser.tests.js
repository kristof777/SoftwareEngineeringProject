let originalTimeout;
beforeEach(function () {
    sleep();
    originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
    jasmine.DEFAULT_TIMEOUT_INTERVAL = 60000; //60 seconds
});

afterEach(function() {
    jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
});

describe('Registering new user as a user would', function() {
    browser.get('');

     it('Should register Page 1', function(done){

        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click().then(function(){
            let signInButton = element(by.buttonText('Sign In'));
            checkDisplayed(signInButton, "The 'Sign In' page ");
        });


        let registerButton = element(by.css('.register'));
        registerButton.click().then(function(){
            sleep();

            attemptSignUp('wrongFormatEmail', 'Password123', 'Password123');

            attemptSignUp('test1@test.ca', 'weakpassword', 'weakpassword');


            attemptSignUp('test1@test.ca', 'NotMatchingPassword123', 'DifferentPassword123');

            attemptSignUp('test1@test.ca', 'Password123', 'Password123');

            sleep();

        });

        done();
    });

    it('Should register Page 2', function(done){
        attemptSignUpInfo('John', 'Smith', '30655512341234');

        attemptSignUpInfo('John', 'Smith', '306555');

        attemptSignUpInfo('John', 'Smith', 'phoneNumbr');

        attemptSignUpInfo('John', 'Smith', '3065551234');

        sleep();
        done();
        });
    it('Should register Page 3', function(done){
        let province = element(by.id('signUpProvinceSelect'));
        province.click();
        sleep();

        let ABoption = element(by.buttonText('Alberta'));
        ABoption.click();
        sleep();

        let okButton = element(by.buttonText('OK'));
        okButton.click();
        sleep();

        let city = element(by.id('signUpCity')).all(by.tagName('input')).first();
        city.sendKeys('Edmonton');


         let finish = element(by.buttonText('Finish'));
         finish.click();

        // if still on register then go back to login and login with same username as this email has
        // already been registered in the database
        // else continue with my profile

        finish.isPresent().then(function(present) {
          if (present) {
                        let myProfileTab = element(by.id('tab-t0-2'));
                        myProfileTab.click();
                        sleep();
                        attemptIncorrectSignIn('test1@test.ca', '123abcABCc');
                        attemptSignIn('test1@test.ca', 'Password123');
                        sleep();
          } else {
            //
          }
        });

        done();
     });


    //TODO Fix to accomodate Browse Page changes

});

function sleep(){
    browser.driver.sleep(1000);
}

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

function attemptSignUp(email1, password1, confirmPassword1){
        let email = element(by.id('signUpEmail')).all(by.tagName('input')).first();
        let password = element(by.id('signUpPassword')).all(by.tagName('input')).first();
        let confirmPassword = element(by.id('signUpConfirmPassword')).all(by.tagName('input')).first();
        let nextButton = element(by.buttonText('Next'));
        sleep();

        email.sendKeys().clear();
        password.sendKeys().clear();
        confirmPassword.sendKeys().clear();
        email.sendKeys(email1).then(function(){
            checkAttribute(email, email1);
        });

        password.sendKeys(password1).then(function(){
            checkAttribute(password, password1);
        });
        confirmPassword.sendKeys(confirmPassword1).then(function(){
            checkAttribute(confirmPassword, confirmPassword1);
        });
        nextButton.click();
}

function attemptSignUpInfo(firstName1, lastName1, phoneNumber1){
        let nextButton = element(by.buttonText('Next'));
        let firstName = element(by.id('signUpFirstName')).all(by.tagName('input')).first();
        let lastName = element(by.id('signUpLastName')).all(by.tagName('input')).first();
        let phoneNumber = element(by.id('signUpPhoneNumber')).all(by.tagName('input')).first();

        firstName.sendKeys().clear();
        lastName.sendKeys().clear();
        phoneNumber.sendKeys().clear();

        firstName.sendKeys(firstName1).then(function(){
            checkAttribute(firstName, firstName1);
        });
        lastName.sendKeys(lastName1).then(function(){
            checkAttribute(lastName, lastName1);
        });
        phoneNumber.sendKeys(phoneNumber1).then(function(){
            checkAttribute(phoneNumber, phoneNumber1);
        });
        nextButton.click();
}

function attemptSignIn(emailInput, passwordInput){
    let email = element(by.id('email')).all(by.tagName('input')).first();
    let password = element(by.id('password')).all(by.tagName('input')).first();
    let signInButton = element(by.buttonText('Sign In'));

    email.sendKeys().clear();
    password.sendKeys().clear();
    email.sendKeys(emailInput).then(function(){
        checkAttribute(email, emailInput);
    });
    password.sendKeys(passwordInput).then(function(){
        checkAttribute(password, passwordInput);
    });
    signInButton.click();

}

function attemptIncorrectSignIn(emailInput1, passwordInput1){
    let email = element(by.id('email')).all(by.tagName('input')).first();
    let password = element(by.id('password')).all(by.tagName('input')).first();
    let signInButton = element(by.buttonText('Sign In'));

    email.sendKeys().clear();
    password.sendKeys().clear();
    email.sendKeys(emailInput1).then(function(){
        checkAttribute(email, emailInput1);
    });
    password.sendKeys(passwordInput1).then(function(){
        checkAttribute(password, passwordInput1);
    });
    signInButton.click();
    browser.driver.sleep(500);
    sleep();
    let enter = browser.actions().sendKeys(protractor.Key.ENTER);
    enter.perform();
    sleep();

}

function scrollAndFavourite(){
     let likeButton = element(by.id('likeButton'));
     let description = element(by.id('description'));
     browser.executeScript("arguments[0].scrollIntoView();", description);
     sleep();
     browser.executeScript("arguments[0].scrollIntoView();", likeButton);
     likeButton.click();
}


