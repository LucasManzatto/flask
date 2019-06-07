import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Author, AuthorDTO } from '../models/backend/author.model';
import { Observable } from 'rxjs';
import { Series } from '../models/backend/series.model';
import { asyncData, createQuery } from '../utils';

@Injectable({
  providedIn: 'root',
})
export class AuthorService extends BaseService<Author, AuthorDTO> {

  authorsArrayMock: Author[] = [{ id: 1, name: 'Author 1' }, { id: 2, name: 'Author 2' }];
  seriesArrayMock: Series[] = [{ id: 1, title: 'Series 1' }, { id: 2, title: 'Series 2' }];

  getSeriesUrl = id => `${this.baseUrl}${id}/series`;

  constructor(http: HttpClient) {
    super(http, 'authors');
  }

  getSeries(id: number): Observable<Series[]> {
    return this.http.get<Series[]>(this.getSeriesUrl(id));
  }
}

export class AuthorServiceStub extends AuthorService {
  getAll() {
    return asyncData(createQuery(this.authorsArrayMock));
  }
  getSeries(id: number) {
    return asyncData(this.seriesArrayMock);
  }
}
