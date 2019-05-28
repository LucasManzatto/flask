import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Query, DefaultQuery } from '../../shared/models/query.model';

@Injectable({
    providedIn: 'root',
})
export class BookService {

    url = `http://localhost:5000/books/`;
    constructor(private http: HttpClient) {

    }
    public getAll(defaultParameters: DefaultQuery, id = '', title = '', author = '') {
        return this.http.get<Query>(this.url, {
            params: {
                'page': defaultParameters.page,
                'direction': defaultParameters.direction,
                'sort_column': defaultParameters.sort_column,
                'query_all': defaultParameters.query_all,
                'id': id,
                'title': title,
                'author_name': author
            }
        });
    }
}