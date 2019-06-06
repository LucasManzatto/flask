import { TestBed } from '@angular/core/testing';
import { BookService, BookServiceStub } from './book.service';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { Book } from '../models/book.model';
import { HttpRequest } from '@angular/common/http';
import { isEqual, sortBy } from 'lodash';
import { Query } from '../models/query.model';
import { DEFAULT_PARAMETERS_KEYS, DEFAULT_PARAMETERS } from '../parameters';
import { AuthorService, AuthorServiceStub } from './author.service';

describe('AuthorService', () => {
  // We declare the variables that we'll use for the Test Controller and for our Service
  let backend: HttpTestingController;
  let service: AuthorService;
  let serviceStub: AuthorServiceStub;

  const defaultParams = DEFAULT_PARAMETERS;
  const defaultParamKeys = DEFAULT_PARAMETERS_KEYS;
  const bookQueryParamKeys = ['id', 'title', 'author_name'];
  const bookQuery = {
    'id': '',
    'title': '',
    'author_name': ''
  };
  const allQueryParams = sortBy(bookQueryParamKeys.concat(defaultParamKeys));
  const defaultQuery = DEFAULT_PARAMETERS;
  const items: Book[] = [{
    id: 1,
    title: 'Test 1',
    author: {
      name: 'Author 1'
    }
  },
  {
    id: 2,
    title: 'Test 2',
    author: {
      name: 'Author 2'
    }
  }];
  const query: Query = {
    items,
    page: 1,
    per_page: 10,
    total: items.length
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AuthorService, AuthorServiceStub],
      imports: [HttpClientTestingModule]
    });
    // We inject our service (which imports the HttpClient) and the Test Controller
    backend = TestBed.get(HttpTestingController);
    service = TestBed.get(AuthorService);
    serviceStub = TestBed.get(AuthorServiceStub);
  });

  afterEach(() => {
    backend.verify();
  });

  it('getSeries() should return series', () => {
    service.getSeries(1).subscribe(res => {
      expect(res).toEqual(service.seriesArrayMock);
    });
    backend.match(request => {
      return request.url === (service.getSeriesUrl(1)) &&
        request.method === 'GET';
    })[0].flush(service.seriesArrayMock);
  });


  describe('AuthorServiceStub', () => {
    it('should getAll()', () => {
      serviceStub.getAll().subscribe(res => {
        expect(res.items).toEqual(service.authorsArrayMock);
      });
      backend.expectNone(service.baseUrl);
    });
    it('should getSeries()', () => {
      serviceStub.getSeries(1).subscribe(res => {
        expect(res).toEqual(service.seriesArrayMock);
      });
      backend.expectNone(service.getSeriesUrl(1));
    });
  });

});
