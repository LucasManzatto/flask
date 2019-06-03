import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Book } from '../models/book.model';
import { BaseService } from './base.service';

@Injectable({
  providedIn: 'root',
})
export class BookService extends BaseService<Book> {

  constructor(http: HttpClient) {
    super(http, 'books');
  }
}
