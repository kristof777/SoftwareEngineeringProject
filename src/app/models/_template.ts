export class TemplateModel{
    constructor(public field1: string,
                public field2: number
                // ...
                ){

    }

    setField1(value: string){
        this.field1 = value;
    }
}