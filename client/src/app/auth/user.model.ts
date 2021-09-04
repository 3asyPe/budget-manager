export class User {
    constructor(public email: string,
                public id: number,
                public firstName: string,
                public secondName: string,
                private _token: string) {

    }

    get token() {
        return this._token
    }
}