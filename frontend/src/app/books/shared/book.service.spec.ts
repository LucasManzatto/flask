import { TestBed } from '@angular/core/testing';
import { BookService } from './book.service';
import {
    HttpClientTestingModule,
    HttpTestingController
} from '@angular/common/http/testing';
import { DefaultQuery } from 'src/app/shared/models/query.model';
import { Book } from '../../shared/models/book.model';
import { Author } from '../../shared/models/author.model';
import { HttpRequest } from '@angular/common/http';
import { isEqual, sortBy } from 'lodash';
import { Query } from '../../shared/models/query.model';

describe('BookService', () => {
    // We declare the variables that we'll use for the Test Controller and for our Service
    let backend: HttpTestingController;
    let service: BookService;

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [BookService],
            imports: [HttpClientTestingModule]
        });

        // We inject our service (which imports the HttpClient) and the Test Controller
        backend = TestBed.get(HttpTestingController);
        service = TestBed.get(BookService);
    });

    afterEach(() => {
        backend.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
    it('returned Observable should match the right data', () => {
        const params = sortBy(['page', 'direction', 'sort_column', 'query_all', 'id', 'title', 'author_name'])
        const items = [{
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
        const total = items.length;
        const query: Query = {
            items,
            page: 1,
            per_page: 10,
            total
        };

        const defaultQuery: DefaultQuery = {
            direction: 'ASC',
            page: '1',
            query_all: '',
            sort_column: 'id'
        };

        service.getAll(defaultQuery, '', '', '').subscribe(res => {
            expect(res.page).toEqual(1);
            expect(res.total).toBe(2);
            expect(res.items).toEqual(items);
        });

        backend.match((request: HttpRequest<any>) => {
            return request.url === service.url &&
                request.urlWithParams ===
                'http://localhost:5000/books/?page=1&direction=ASC&sort_column=id&query_all=&id=&title=&author_name=' &&
                request.method === 'GET' &&
                isEqual(sortBy(request.params.keys()), params) &&
                request.params.get('direction') === defaultQuery.direction &&
                request.params.get('page') === defaultQuery.page &&
                request.params.get('sort_column') === defaultQuery.sort_column &&
                request.params.get('query_all') === defaultQuery.query_all &&
                request.responseType === 'json';
        })[0].flush(query);
        backend.expectNone(service.url);
    });
});
