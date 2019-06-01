export class Query {
    items: any[];
    total: number;
    page: number;
    per_page: number;
}

export class DefaultQuery {
    direction: string;
    page: string;
    per_page: string;
    sort_column: string;
    query_all: string;

    constructor() {
        this.direction = 'ASC';
        this.page = '1';
        this.per_page = '10';
        this.sort_column = 'id';
        this.query_all = '';
    }
}
