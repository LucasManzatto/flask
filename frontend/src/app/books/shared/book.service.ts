import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Query, DefaultQuery } from '../../shared/models/query.model';
import { Book } from '../../shared/models/book.model';
import { API } from 'src/app/shared/api';

@Injectable({
  providedIn: 'root',
})
export class BookService {

  defaultQuery: DefaultQuery = {
    direction: 'ASC',
    page: '1',
    per_page: '10',
    query_all: '',
    sort_column: 'id'
  };

  booksUrl = `${API}/books`;
  getAllBooksUrl = `${this.booksUrl}/`;
  constructor(private http: HttpClient) {

  }
  public getAll(defaultParameters = this.defaultQuery, id = '', title = '', author_name = '') {
    return this.http.get<Query>(this.getAllBooksUrl, {
      params: {
        'page': defaultParameters.page,
        'per_page': defaultParameters.per_page,
        'direction': defaultParameters.direction,
        'sort_column': defaultParameters.sort_column,
        'query_all': defaultParameters.query_all,
        'id': id,
        'title': title,
        'author_name': author_name
      }
    });
  }

  public getBook(id) {
    return this.http.get<Book>(`${this.booksUrl}/${id}`);
  }
}
