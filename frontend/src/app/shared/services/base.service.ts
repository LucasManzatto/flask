import { HttpClient } from '@angular/common/http';
import { Query } from '../models/application/query.model';
import { API } from 'src/app/shared/api';
import { DEFAULT_PARAMETERS } from 'src/app/shared/parameters';
import { Observable } from 'rxjs';
import { GlobalService } from './global.service';

export abstract class BaseService<T, V> {

  currentItem: T;
  editing: boolean;

  baseUrl: string;
  getOneUrl: string;
  constructor(protected http: HttpClient,
    endpoint: string,
    private globalService: GlobalService) {
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

  public post(item: V): Observable<any> {
    this.globalService.reloadData = true;
    return this.http.post(this.baseUrl, item);
  }

  public put(item: V): Observable<any> {
    this.globalService.reloadData = true;
    return this.http.put(this.baseUrl, item);
  }

  public delete(id: number): Observable<any> {
    this.globalService.reloadData = true;
    return this.http.delete(this.baseUrl + id);
  }
}
