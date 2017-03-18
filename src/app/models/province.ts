let assert = require('assert-plus');

export class Province{
    abbr: string;
    name: string;

    private constructor(abbr: string, name: string){
        this.abbr = abbr;
        this.name = name;
    }

    static AB = new Province("AB", "Alberta");
    static BC = new Province("BC", "British Columbia");
    static MB = new Province("MB", "Manitoba");
    static NB = new Province("NB", "New Brunswick");
    static NL = new Province("NL", "Newfoundland and Labrador");
    static NS = new Province("NS", "Nova Scotia");
    static NU = new Province("NU", "Nunavut");
    static NT = new Province("NT", "Northwest Territories");
    static ON = new Province("ON", "Ontario");
    static PE = new Province("PE", "Prince Edward Island");
    static QC = new Province("QC", "Quebec");
    static SK = new Province("SK", "Saskatchewan");
    static YT = new Province("YT", "Yukon");

    /**
     * Return an array of all of the provinces and territories
     *
     * @type {Province[]}
     */
    static asArray: Province[] = [
        Province.AB,
        Province.BC,
        Province.MB,
        Province.NB,
        Province.NL,
        Province.NS,
        Province.NU,
        Province.NT,
        Province.ON,
        Province.PE,
        Province.QC,
        Province.SK,
        Province.YT,
    ];

    /**
     * Returns a Province from the abbreviation provided
     *
     * @param abbr          the abbreviation of the province
     * @returns {Province}  the province with the specified abbreviation
     * @returns null        if the abbreviation provided was not valid
     */
    static fromAbbr(abbr: string): Province{
        if(!abbr) return null;

        let provinces: Province[] = Province.asArray;

        for(let i=0; i<provinces.length; i++){
            if(provinces[i]['abbr'].toLowerCase() === abbr.toLowerCase()){
                return provinces[i];
            }
        }
        return null;
    }
}
