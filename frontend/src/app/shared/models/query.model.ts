export class Query {
    items: any[];
    total: Number;
    page: Number;
    per_page: Number;
}

export class DefaultQuery {
    direction: string;
    page: string;
    sort_column: string;
    query_all: string;

    constructor() {
        this.direction = 'ASC';
        this.page = '1';
        this.sort_column = 'id';
        this.query_all = '';
    }
}
