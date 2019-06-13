import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book, BookDTO } from '../models/backend/book.model';
import { BaseService } from './base.service';
import { asyncData, createQuery } from '../utils';
import { GlobalService } from './global.service';

@Injectable({
  providedIn: 'root',
})
export class BookService extends BaseService<Book, BookDTO> {

  booksArrayMock: Book[] = [{ id: 1, title: 'Book 1', description: 'Description 1', author: { name: 'Author 1' } },
  { id: 2, title: 'Book 2', description: 'Description 2', author: { name: 'Author 2' }, series: { title: 'Series 1' } }];
  constructor(http: HttpClient, globalService: GlobalService) {
    super(http, 'books', globalService);
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
