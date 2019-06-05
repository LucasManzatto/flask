import { HttpClient } from '@angular/common/http';
import { Query } from '../models/query.model';
import { API } from 'src/app/shared/api';
import { DEFAULT_PARAMETERS } from 'src/app/shared/parameters';
import { Observable } from 'rxjs';

export abstract class BaseService<T> {

  currentItem: T;
  editing: boolean;

  baseUrl: string;
  getOneUrl: string;
  constructor(protected http: HttpClient, endpoint: string) {
    this.baseUrl = `${API}/${endpoint}/`;
  }

  public getOne(id: string | number): Observable<T> {
    return this.http.get<T>(this.baseUrl + id);
  }

  public getAll(mask: string = ''): Observable<Query> {
    return this.http.get<Query>(this.baseUrl, { headers: { 'X-Fields': mask } });
  }
  public getAllWithParameters(defaultParameters = DEFAULT_PARAMETERS, queryParameters) {
    const params = {
      'page': defaultParameters.page,
      'per_page': defaultParameters.per_page,
      'direction': defaultParameters.direction,
      'sort_column': defaultParameters.sort_column,
      'query_all': defaultParameters.query_all,
      ...queryParameters
    };
    return this.http.get<Query>(this.baseUrl, {
      params
    });
  }

  public post(item: T): void {
    this.http.post(this.baseUrl, item);
  }

  public put(item: T): void {
    this.http.put(this.baseUrl, item);
  }

  public delete(id: number): void {
    this.http.delete(this.baseUrl + id);
  }
}
