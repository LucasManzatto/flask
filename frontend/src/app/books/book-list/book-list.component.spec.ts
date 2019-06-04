import { async, ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';

import { BookListComponent } from './book-list.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule, By, HAMMER_LOADER } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { isFunction, isEqual } from 'lodash';
import { DEBOUNCE_TIME } from '../../shared/parameters';
import { MatDialog, MatDialogRef } from '@angular/material/dialog';
import { BookAddComponent } from './book-add/book-add.component';
import { BrowserDynamicTestingModule } from '@angular/platform-browser-dynamic/testing';
import { of } from 'rxjs';
import { ScrollingModule } from '@angular/cdk/scrolling';

describe('BookListComponent', () => {
  let component: BookListComponent;
  let fixture: ComponentFixture<BookListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [AppRoutingModule,
        BrowserAnimationsModule,
        BrowserModule,
        ScrollingModule,
        HttpClientModule,
        SharedModule,
        FlexLayoutModule,
        FormsModule,
        ReactiveFormsModule
      ],
      declarations: [BookListComponent, BookAddComponent],
      providers: [
        { provide: MatDialogRef, useValue: {} }
      ]
    }).overrideModule(BrowserDynamicTestingModule, {
      set: {
        entryComponents: [BookAddComponent],
      }
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

  describe('AfterViewInit', () => {
    it('should start paginator', () => {
      const paginatorSpy = spyOn(component, 'startPaginator');
      component.ngAfterViewInit();
      expect(paginatorSpy).toHaveBeenCalled();
    });
    it('should start sort', () => {
      const sortSpy = spyOn(component, 'startSort');
      component.ngAfterViewInit();
      expect(sortSpy).toHaveBeenCalled();
    });
    it('should start filters', () => {
      const startFilterSpy = spyOn(component, 'startFilter');
      component.ngAfterViewInit();
      expect(startFilterSpy).toHaveBeenCalledWith(component.inputFilterAll);
    });
  });

  describe('should call loadData on', () => {
    beforeEach(() => {
      spyOn(component, 'loadData');
    });
    afterEach(fakeAsync(() => {
      tick(DEBOUNCE_TIME);
      fixture.whenStable().then(() => {
        expect(component.loadData).toHaveBeenCalled();
      });
    }));
    it('inputAll change', () => {
      const input = fixture.debugElement.query(By.css('#iptFilterAll')).nativeElement;
      input.value = 'test';
      input.dispatchEvent(new Event('input'));
      expect(component.defaultParameters.query_all).toBe('test');
    });
    it('page change', () => {
      const paginator = component.paginator;
      if (paginator) {
        paginator.pageIndex = 1;
        paginator.page.emit();
      }
    });
    it('sort change', () => {
      const sort = component.dataSource.sort;
      if (sort) {
        sort.sort({ start: 'asc', id: 'id', disableClear: false });
        sort.sortChange.emit();
      }
    });
    it('ngOnInit', () => {
      component.ngOnInit();
    });
  });

  it('should return correct cell elements on table', () => {
    spyOn(component.columns[0], 'cell');
    const data = component.dataSource.data;
    const idColumn = component.columns[0];
    idColumn.cell({ id: 1, title: 'Test', author: { name: 'Test Author' } });
    component.columns.map(column => expect(isFunction(column.cell)).toBe(true));
    data.map(row => {
      expect(idColumn.cell(row)).toBe(`${row.id}`);
    });
    expect(component.columns[0].cell).toHaveBeenCalled();
  });

  describe('ngOnInit', () => {
    it('should call initColumns', () => {
      spyOn(component, 'initColumns');
      component.ngOnInit();
      expect(component.initColumns).toHaveBeenCalled();
    });
    it('should call loadData', () => {
      spyOn(component, 'loadData');
      component.ngOnInit();
      expect(component.loadData).toHaveBeenCalled();
    });
  });

  describe('initColumns', () => {
    const columns = ['id', 'title', 'author_name', 'series_title'];
    const displayedColumns = ['select', 'id', 'title', 'author_name', 'series_title', 'actions'];

    beforeAll(() => {
      component.initColumns();
    });
    it('should init columns array', () => {
      expect(component.columns.length).toEqual(columns.length);
    });
    it('should init displayedColumns array with select as first column', () => {
      expect(component.displayedColumns).toEqual(displayedColumns);
      expect(component.displayedColumns.length).toEqual(displayedColumns.length);
    });
  });

  it('should open BookAddComponent when add button is clicked', () => {
    spyOn(component, 'openAddBookDialog');
    const button = fixture.debugElement.query(By.css('#add-button')).nativeElement;
    button.click();

    fixture.whenStable().then(() => {
      expect(component.openAddBookDialog).toHaveBeenCalled();
    });
  });

  describe('openAddBookDialog', () => {
    let dialogSpy: jasmine.Spy;
    const dialogRefSpyObj = jasmine.createSpyObj({ afterClosed: of({}), close: null });
    beforeEach(() => {
      dialogSpy = spyOn(TestBed.get(MatDialog), 'open').and.returnValue(dialogRefSpyObj);
      spyOn(component, 'loadData');
      component.openAddBookDialog(false);
    });
    it('should open the BookAddComponent', () => {
      expect(dialogSpy).toHaveBeenCalledWith(BookAddComponent, { width: '50%' });
    });
    it('should call loadData when dialog closes', () => {
      expect(component.loadData).toHaveBeenCalled();
    });
  });

  describe('table', () => {
    it('should have a sort', () => {
      expect(component.sort).toBeDefined();
      expect(component.dataSource.sort).toEqual(component.sort);
    });
    it('should toggle all and untoggle all', async(() => {
      spyOn(component, 'masterToggle');
      const checkBoxToggleAll = fixture.debugElement.nativeElement.querySelector('#toggle-all');
      checkBoxToggleAll.click();
      fixture.whenStable().then(() => {
        expect(checkBoxToggleAll.checked).toBe(true);
        expect(component.selection.selected.length).toEqual(component.dataSource.data.length);
        expect(component.masterToggle).toHaveBeenCalled();

        checkBoxToggleAll.click();

        fixture.whenStable().then(() => {
          expect(checkBoxToggleAll.checked).toBe(false);
          expect(component.selection.selected.length).toEqual(0);
        });
      });
    }));
    it('should change data when page changes', fakeAsync(() => {
      const oldData = component.dataSource.data;
      component.paginator.pageIndex++;
      component.paginator.page.emit();
      tick(DEBOUNCE_TIME);
      fixture.whenStable().then(() => {
        const newData = component.dataSource.data;
        expect(isEqual(oldData, newData)).toBe(false);
      });
    }));
  });
});
