import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BookListComponent } from './book-list.component';
import { SharedModule } from 'src/app/shared/shared.module';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule } from '@angular/forms';

describe('BookListComponent', () => {
  let component: BookListComponent;
  let fixture: ComponentFixture<BookListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppRoutingModule, BrowserAnimationsModule, BrowserModule, HttpClientModule, SharedModule, FlexLayoutModule, FormsModule
      ],
      declarations: [BookListComponent]
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

  it('should have columns', () => {
    expect(component.displayedColumns).toEqual(['id', 'title', 'author_name']);
    expect(component.displayedColumns.length).toEqual(3);
  });

  it('should have a paginator', () => {
    expect(component.dataSource.paginator).toBe(component.paginator);
  });
  it('should have a sort', () => {
    expect(component.dataSource.sort).toEqual(component.sort);
  });
});
