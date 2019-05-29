import { async, ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';

import { BookListComponent } from './book-list.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule, By, HAMMER_LOADER } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule } from '@angular/forms';
import { isFunction } from 'lodash';
import { DEBOUNCE_TIME } from '../../shared/parameters';

describe('BookListComponent', () => {
  let component: BookListComponent;
  let fixture: ComponentFixture<BookListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppRoutingModule, BrowserAnimationsModule, BrowserModule, HttpClientModule, SharedModule, FlexLayoutModule, FormsModule
      ],
      declarations: [BookListComponent],
      // providers: [{
      //   provide: HAMMER_LOADER,
      //   useValue: () => new Promise(() => { })
      // }]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BookListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });


  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have a dataSource initialized', () => {
    expect(component.dataSource).toBeDefined();
  });

  it('should have a paginator', () => {
    expect(component.paginator).toBeDefined();
  });

  it('should start paginator on AfterViewInit', () => {
    const paginatorSpy = spyOn(component, 'startPaginator').and.callThrough();
    component.ngAfterViewInit();
    expect(paginatorSpy).toHaveBeenCalled();
  });

  it('should have a sort', () => {
    expect(component.sort).toBeDefined();
    expect(component.dataSource.sort).toEqual(component.sort);
  });

  it('should start sort on AfterViewInit', () => {
    const paginatorSpy = spyOn(component, 'startSort').and.callThrough();
    component.ngAfterViewInit();
    expect(paginatorSpy).toHaveBeenCalled();
  });

  it('should instantiate the table paginator', () => {
    expect(component.dataSource.paginator).toBe(component.paginator);
  });

  it('should start filters', () => {
    const startFilterSpy = spyOn(component, 'startFilter').and.callThrough();
    component.ngAfterViewInit();
    expect(startFilterSpy).toHaveBeenCalledWith(component.inputFilterAll);
  });

  it('should call loadData when inputAll changes', fakeAsync(() => {
    spyOn(component, 'loadData');
    const input = fixture.debugElement.query(By.css('#iptFilterAll')).nativeElement;
    input.value = 'test';
    input.dispatchEvent(new Event('input'));
    tick(DEBOUNCE_TIME);
    expect(component.defaultParameters.query_all).toBe('test');
    expect(component.loadData).toHaveBeenCalled();
  }));

  it('should call loadData when page changes', fakeAsync(() => {
    spyOn(component, 'loadData');
    const paginator = component.dataSource.paginator;
    if (paginator) {
      paginator.pageIndex = 1;
      paginator.page.emit();
    }
    tick(DEBOUNCE_TIME);
    expect(component.loadData).toHaveBeenCalled();
  }));

  it('should call loadData when sort changes', fakeAsync(() => {
    spyOn(component, 'loadData');
    const sort = component.dataSource.sort;
    if (sort) {
      sort.sortChange.emit();
    }
    tick(DEBOUNCE_TIME);
    expect(component.loadData).toHaveBeenCalled();
  }));

  it('should return correct cell elements on table', () => {
    spyOn(component.columns[0], 'cell');
    const data = component.dataSource.data;
    const idColumn = component.columns[0];
    idColumn.cell({ id: '1' });
    component.columns.map(column => expect(isFunction(column.cell)).toBe(true));
    data.map(row => {
      expect(idColumn.cell(row)).toBe(`${row.id}`);
    });
    expect(component.columns[0].cell).toHaveBeenCalled();
  });

  it('should init columns and call loadData on ngOnInit', () => {
    const columns = ['id', 'title', 'author_name'];
    spyOn(component, 'initColumns');
    spyOn(component, 'loadData');
    component.ngOnInit();
    expect(component.initColumns).toHaveBeenCalled();
    expect(component.loadData).toHaveBeenCalled();
    expect(component.columns.length).toEqual(3);
    expect(component.displayedColumns).toEqual(columns);
    expect(component.displayedColumns.length).toEqual(3);
  });

});
