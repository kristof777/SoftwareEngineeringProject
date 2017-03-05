describe('Registering new user as a user would', function() {
    let originalTimeout;
    browser.get('/#/ionic-lab');

    beforeEach(function () {
        originalTimeout = jasmine.DEFAULT_TIMEOUT_INTERVAL;
        jasmine.DEFAULT_TIMEOUT_INTERVAL = 20000; //20 seconds
    });

    afterEach(function() {
        jasmine.DEFAULT_TIMEOUT_INTERVAL = originalTimeout;
    });

    it('Should register', function(done){

        let myProfileTab = element(by.id('tab-t0-2'));
        myProfileTab.click();
        browser.driver.sleep(1500);
        let registerButton;
        registerButton = element(by.css('.register'));
        registerButton.click();
        browser.driver.sleep(1500);
        let email, password, confirmPassword;
        email = element(by.id('signUpEmail')).all(by.tagName('input')).first();
        password = element(by.id('signUpPassword')).all(by.tagName('input')).first();
        confirmPassword = element(by.id('signUpConfirmPassword')).all(by.tagName('input')).first();

        email.sendKeys('testEmail@email.ca');
        password.sendKeys('Password123');
        confirmPassword.sendKeys('Password123');

        let nextButton;
        nextButton = element(by.buttonText('Next'));
        nextButton.click();

        browser.driver.sleep(1500);

        let firstName, lastName, phoneNumber;
        firstName = element(by.id('signUpFirstName')).all(by.tagName('input')).first();
        lastName = element(by.id('signUpLastName')).all(by.tagName('input')).first();
        phoneNumber = element(by.id('signUpPhoneNumber')).all(by.tagName('input')).first();
        firstName.sendKeys('John');
        lastName.sendKeys('Smith');
        phoneNumber.sendKeys('3065551234');
        nextButton = element(by.buttonText('Next'));
        nextButton.click();
        browser.driver.sleep(1500);

        let province, city, ABoption;

        province = element(by.id('signUpProvinceSelect')).click();
        browser.driver.sleep(500);
        ABoption = element(by.buttonText('Alberta'));
        ABoption.click();
        browser.driver.sleep(500);
        let okButton;
        okButton = element(by.buttonText('OK'));
        okButton.click();
        browser.driver.sleep(500);
        city = element(by.id('signUpCity')).all(by.tagName('input')).first();
            city.sendKeys('Edmonton');


         let finish = element(by.buttonText('Finish'));
         finish.click();

        // if still on register then go back to login and login with same username
        // else continue with my profile screen
        if(finish.isDisplayed()){
            myProfileTab.click();
            browser.driver.sleep(500);
            email = element(by.id('email')).all(by.tagName('input')).first();;
            email.sendKeys('test');
            password = element(by.id('password')).all(by.tagName('input')).first();
           // password.sendKeys('Pasword123');
            let signInButton = element(by.buttonText('Sign In'));
            signInButton.click();
            browser.driver.sleep(500);


        }
        done();
     });

    it('Should browse listings', function(done){

        let browseButton = element(by.id('tab-t0-0'));
        browseButton.click();
        browser.driver.sleep(500);

        let browseImage;
        browseImage = element(by.id('image'));
        // drag and drop not working
       // browser.actions().dragAndDrop(browseImage,{x:50,y:0}).perform();
        browseImage.click();
        browser.driver.sleep(500);
        let rightArrowButton = element(by.id('nextProperty'));
        let leftArrowButton = element(by.id('previousProperty'));
        let likeButton = element(by.id('likeButton'));
        let unlikeButton = element(by.id('unlikeButton'));
        let description = element(by.id('description'));

        for(i=0; i<5; i++)
                 {
                    try{
                     rightArrowButton.click();
                     if(i%2 == 0)
                     {
                         browser.executeScript("arguments[0].scrollIntoView();", description);
                         browser.driver.sleep(100);
                         browser.executeScript("arguments[0].scrollIntoView();", likeButton);
                         likeButton.click();
                     }
                     else
                     {
                        unlikeButton.click();
                     }
                     }
                     catch(NoSuchElementError){
                        console.err("ran out of listings to browse");
                     }
                 }
        done();

     });

    it('Should add listing', function(done){

      // testing "add listing" functionality
        let myListings = element(by.id('tab-t0-3'));
                                          myListings.click();
                                          browser.driver.sleep(500);
        let addListingButton;
        addListingButton= element(by.id('addButton'));
        addListingButton.click();
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
                browser.driver.sleep(500);

                                let bath = element(by.id('alBathRoom')).all(by.tagName('input')).first();


                let city = element(by.id('alCityTown')).all(by.tagName('input')).first();
                city.sendKeys('Saskatoon');

                let address = element(by.id('alAddress')).all(by.tagName('input')).first();
                address.sendKeys('123 First Street East');

                let postalCode = element(by.id('alPostalCode')).all(by.tagName('input')).first();
                postalCode.sendKeys('f1s 9u8');

                browser.executeScript("arguments[0].scrollIntoView();", bath);

                let price = element(by.id('alPrice')).all(by.tagName('input')).first();
                price.sendKeys('13000000');

                let feet = element(by.id('alSqFeet')).all(by.tagName('input')).first();
                feet.sendKeys('600');

                let bed = element(by.id('alBed')).all(by.tagName('input')).first();
                bed.sendKeys('5');

                bath.sendKeys('2');

                browser.driver.sleep(500);

                let desc2 = element(by.id('alDesc')).all(by.tagName('textarea')).first();
                browser.driver.sleep(500);
                desc2.sendKeys('Nice trailer with a little dust. Fixer Upper.');


                browser.driver.sleep(500);
                done();

        });

});
