import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Query } from '../../shared/models/query.model';

@Injectable({
    providedIn: 'root',
})
export class BookService {

    url = `http://localhost:5000/books/`;
    constructor(private http: HttpClient) {

    }
    public getAll(query_all = '', id = '', title = '', author = '') {
        return this.http.get<Query>(this.url, {
            params: {
                'query_all': query_all,
                'id': id,
                'title': title,
                'author': author
            }
        });
    }
}