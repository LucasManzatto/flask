import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from 'src/app/shared/models/book.model';

@Injectable({
    providedIn: 'root',
})
export class BookService {

    url = `http://localhost:5000/books/`
    constructor(private http: HttpClient) {

    }
    public getAll() {
        return this.http.get<Book[]>(this.url);
    }
}