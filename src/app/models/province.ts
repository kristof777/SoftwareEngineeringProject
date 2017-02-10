export class Province{

    static AB = { abbr: "AB", name: "Alberta"};
    static BC = { abbr: "BC", name: "British Columbia"};
    static MB = { abbr: "MB", name: "Manitoba"};
    static NB = { abbr: "NB", name: "New Brunswick"};
    static NL = { abbr: "NL", name: "Newfoundland and Labrador"};
    static NS = { abbr: "NS", name: "Nova Scotia"};
    static NU = { abbr: "NU", name: "Nunavut"};
    static NW = { abbr: "NW", name: "North West Territories"};
    static ON = { abbr: "ON", name: "Ontario"};
    static PE = { abbr: "PE", name: "Prince Edward Island"};
    static QC = { abbr: "QC", name: "Quebec"};
    static SK = { abbr: "SK", name: "Saskatchewan"};
    static YT = { abbr: "YT", name: "Yukon"};

    static asArray: Province[] = [
        Province.AB,
        Province.BC,
        Province.MB,
        Province.NB,
        Province.NL,
        Province.NS,
        Province.NU,
        Province.NW,
        Province.ON,
        Province.PE,
        Province.QC,
        Province.SK,
        Province.YT,
    ];

    static fromAbbr(abbr: string): Province{
        let provinces: Province[] = Province.asArray;

        for(let i=0; i<provinces.length; i++){
            if(provinces[i]['abbr'].toLowerCase() === abbr.toLowerCase()){
                return provinces[i];
            }
        }
        return null;
    }
}
