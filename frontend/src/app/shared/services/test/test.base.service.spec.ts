import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { HttpRequest } from '@angular/common/http';
import { isEqual, sortBy } from 'lodash';
import { TestService } from './test.base.service';
import { DEFAULT_PARAMETERS, DEFAULT_PARAMETERS_KEYS } from '../../parameters';
import { Test } from '../../models/test.model';
import { Query } from '../../models/query.model';

describe('TestBaseService', () => {
  // We declare the variables that we'll use for the Test Controller and for our Service
  let backend: HttpTestingController;
  let service: TestService;

  const defaultParams = DEFAULT_PARAMETERS;
  const defaultParamKeys = DEFAULT_PARAMETERS_KEYS;
  const bookQueryParamKeys = ['id', 'name'];
  const bookQuery = {
    'id': '',
    'name': '',
  };
  const allQueryParams = sortBy(bookQueryParamKeys.concat(defaultParamKeys));
  const defaultQuery = DEFAULT_PARAMETERS;
  const items: Test[] = [{
    id: 1,
    name: 'Test 1',
  },
  {
    id: 2,
    name: 'Test 2',
  }];
  const query: Query = {
    items,
    page: 1,
    per_page: 10,
    total: items.length
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [TestService],
      imports: [HttpClientTestingModule]
    });

    // We inject our service (which imports the HttpClient) and the Test Controller
    backend = TestBed.get(HttpTestingController);
    service = TestBed.get(TestService);
  });

  afterEach(() => {
    backend.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  describe('getAllWithParameters()', () => {
    afterEach(() => {
      backend.match((request: HttpRequest<any>) => {
        return request.url === service.baseUrl &&
          request.method === 'GET' &&
          isEqual(sortBy(request.params.keys()), allQueryParams) &&
          request.params.get('direction') === defaultQuery.direction &&
          request.params.get('page') === defaultQuery.page &&
          request.params.get('sort_column') === defaultQuery.sort_column &&
          request.params.get('query_all') === defaultQuery.query_all &&
          request.params.get('per_page') === defaultQuery.per_page &&
          request.responseType === 'json';
      })[0].flush(query);
    });
    it('should get data with defaultParams', () => {
      service.getAllWithParameters(defaultParams, bookQuery).subscribe(res => {
        expect(res.page).toEqual(query.page);
        expect(res.total).toBe(query.total);
        expect(res.items).toEqual(items);
      });
    });
    it('should get data with no defaultParams', () => {
      service.getAllWithParameters(undefined, bookQuery).subscribe(res => {
        expect(res.page).toEqual(query.page);
        expect(res.total).toBe(query.total);
        expect(res.items).toEqual(items);
      });
    });
  });

  it('should getAll() without mask', () => {
    service.getAll().subscribe(res => {
      expect(res.page).toEqual(query.page);
      expect(res.total).toBe(query.total);
      expect(res.items).toEqual(query.items);
    });
    backend.match(request => {
      return request.url === (service.baseUrl) &&
        request.method === 'GET';
    })[0].flush(query);
  });

  it('should getAll() with mask', () => {
    const mask = '{items{id}}';
    const itemsArrayWithMask = [{ id: 1 }, { id: 2 }];
    service.getAll(mask).subscribe(res => {
      expect(res.page).toBeUndefined();
      expect(res.total).toBeUndefined();
      expect(res.items).toBe(itemsArrayWithMask);
    });
    backend.match(request => {
      return request.url === (service.baseUrl) &&
        request.method === 'GET';
    })[0].flush({ items: itemsArrayWithMask });
  });


  it('should return book from getOne()', () => {
    const item = items[0];
    service.getOne(item.id ? item.id : '0').subscribe(res => {
      expect(res).toEqual(item);
    });
    backend.expectOne(service.baseUrl + item.id).flush(item);
  });

  it('should return not found from getOne()', () => {
    service.getOne(-1).subscribe();
    backend.expectOne(service.baseUrl + '-1');
  });


  it('should post data', () => {
    service.post(items[0]);
    backend.expectNone(service.baseUrl);
  });

  it('should update data', () => {
    service.put(items[0]);
    backend.expectNone(service.baseUrl);
  });

  it('should delete data', () => {
    service.delete(items[0].id);
    backend.expectNone(service.baseUrl);
  });
});
