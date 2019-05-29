import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { Book } from '../../shared/models/book.model';
import { Author } from '../../shared/models/author.model';
import { BookService } from '../shared/book.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { fromEvent } from 'rxjs';
import { DEBOUNCE_TIME, PAGE_SIZES } from 'src/app/shared/parameters';
import { DefaultQuery } from 'src/app/shared/models/query.model';
import { ColumnModel } from '../../shared/models/column.model';

@Component({
  selector: 'app-book-list',
  templateUrl: './book-list.component.html',
  styleUrls: ['./book-list.component.scss']
})
export class BookListComponent implements OnInit, AfterViewInit {

  dataSource: MatTableDataSource<Book>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('iptFilterAll') inputFilterAll;
  totalPageElements: Number;


  columns: ColumnModel[];
  displayedColumns: string[];
  filterId = '';
  filterTitle = '';
  filterAuthor = '';

  defaultParameters = new DefaultQuery();

  constructor(private bookService: BookService) { }

  ngOnInit() {
    this.initColumns();
    this.dataSource = new MatTableDataSource<Book>();
    this.loadData();
  }
  ngAfterViewInit(): void {
    this.startSort();
    this.startPaginator();
    this.startFilter(this.inputFilterAll);
  }

  initColumns() {
    this.columns = [
      { columnDef: 'id', header: 'ID', cell: (row: Book) => `${row.id}` },
      { columnDef: 'title', header: 'Title', cell: (row: Book) => `${row.title}` },
      { columnDef: 'author_name', header: 'Author', cell: (row: Book) => `${row.author.name}` }
    ];
    this.displayedColumns = this.columns.map(x => x.columnDef);
  }

  loadData() {
    this.bookService.getAll(this.defaultParameters, this.filterId, this.filterTitle, this.filterAuthor)
      .subscribe(res => {
        this.dataSource.data = res.items;
        this.totalPageElements = res.total;
      });
  }
  startFilter(input: ElementRef) {
    fromEvent(input.nativeElement, 'input').pipe(
      debounceTime(DEBOUNCE_TIME),
      distinctUntilChanged(),
      tap(() => {
        this.paginator.firstPage();
        this.loadData();
      })
    ).subscribe();
  }

  startPaginator() {
    this.dataSource.paginator = this.paginator;
    this.paginator.page.pipe(
      tap(() => {
        this.loadData();
      })
    ).subscribe();
  }

  startSort() {
    this.dataSource.sort = this.sort;
    this.sort.sortChange.subscribe(res => {
      this.paginator.firstPage();
      this.loadData();
    });
  }

}
