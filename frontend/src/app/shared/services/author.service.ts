import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Author } from '../models/author.model';
import { Observable } from 'rxjs';
import { Series } from '../models/series.model';
import { asyncData, createQuery } from '../utils';

@Injectable({
  providedIn: 'root',
})
export class AuthorService extends BaseService<Author> {

  authorsArrayMock: Author[] = [{ id: 1, name: 'Author 1' }, { id: 2, name: 'Author 2' }];
  seriesArrayMock: Series[] = [{ id: 1, title: 'Series 1' }, { id: 2, title: 'Series 2' }]

  constructor(http: HttpClient) {
    super(http, 'authors');
  }

  getSeries(id: number): Observable<Series[]> {
    return this.http.get<Series[]>(`${this.baseUrl}${id}/series`);
  }
}

export class AuthorServiceStub extends AuthorService {
  getAll() {
    return asyncData(createQuery(this.authorsArrayMock));
  }
  getSeries() {
    return asyncData(this.seriesArrayMock);
  }
}
