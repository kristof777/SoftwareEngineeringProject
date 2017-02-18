import {UserService} from "../../src/app/providers/login-service"
import {Listing} from '../../src/app/models/listing';
import {Location} from "../../src/app/models/location";
import {Province} from "../../src/app/models/province";

describe('Your test here', () => {
    it('true should be true', () => {
        expect(UserService.checkPass("aaaAAA1124")['strength']).toBe(4);
    });
});
