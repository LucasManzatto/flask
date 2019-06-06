import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../models/book.model';
import { BaseService } from './base.service';
import { asyncData, createQuery } from '../utils';

@Injectable({
  providedIn: 'root',
})
export class BookService extends BaseService<Book> {

  booksArrayMock: Book[] = [{ id: 1, title: 'Book 1', author: { name: 'Author 1' } },
  { id: 2, title: 'Book 2', author: { name: 'Author 2' }, series: { title: 'Series 1' } }];
  constructor(http: HttpClient) {
    super(http, 'books');
  }
}

export class BookServiceStub extends BookService {
  getAll() {
    return asyncData(createQuery(this.booksArrayMock));
  }
  getAllWithParameters() {
    return asyncData(createQuery(this.booksArrayMock));
  }
}
