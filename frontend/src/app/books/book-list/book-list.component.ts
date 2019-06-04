import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, HostListener } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { Book } from '../../shared/models/book.model';
import { Author } from '../../shared/models/author.model';
import { BookService } from '../../shared/services/book.service';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { fromEvent } from 'rxjs';
import { DEBOUNCE_TIME, PAGE_SIZES } from 'src/app/shared/parameters';
import { DefaultQuery } from 'src/app/shared/models/query.model';
import { ColumnModel } from '../../shared/models/column.model';
import { MatDialog } from '@angular/material/dialog';
import { BookAddComponent } from './book-add/book-add.component';
import { SelectionModel } from '@angular/cdk/collections';

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

  dataLength: number;
  pageLength = 30;
  columns: ColumnModel[];
  displayedColumns: string[];
  filterId = '';
  filterTitle = '';
  filterAuthor = '';

  defaultParameters = new DefaultQuery();
  selection = new SelectionModel<Book>(true, []);

  constructor(private bookService: BookService, public dialog: MatDialog) { }

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
      { columnDef: 'author_name', header: 'Author', cell: (row: Book) => `${row.author.name}` },
      {
        columnDef: 'series_title', header: 'Series', cell: (row: Book) => {
          return row.series ? `${row.series.title}` : 'No Series';
        }

      }
    ];
    this.displayedColumns = ['select', ...this.columns.map(x => x.columnDef), 'actions'];
  }

  loadData() {
    const queryParameters = {
      'id': this.filterId,
      'title': this.filterTitle,
      'author_name': this.filterAuthor
    };
    this.bookService.getAllWithParameters(this.defaultParameters, queryParameters)
      .subscribe(res => {
        this.selection.clear();
        this.dataSource.data = res.items;
        this.dataLength = res.total;
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
    this.paginator.page.pipe(
      tap(() => {
        this.defaultParameters.per_page = this.paginator.pageSize.toString();
        this.defaultParameters.page = (this.paginator.pageIndex + 1).toString();
        this.loadData();
      })
    ).subscribe();
  }

  startSort() {
    this.dataSource.sort = this.sort;
    this.sort.sortChange.subscribe(res => {
      if (res) {
        this.defaultParameters.sort_column = res.active;
        this.defaultParameters.direction = res.direction;
        this.paginator.firstPage();
        this.loadData();
      }
    });
  }

  openAddBookDialog(edit: boolean, row?) {
    this.bookService.editing = edit;
    if (row) {
      this.bookService.currentItem = row;
    }
    const dialogRef = this.dialog.open(BookAddComponent, { width: '50%' });
    dialogRef.afterClosed().subscribe(result => {
      this.loadData();
    });
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
      this.selection.clear() :
      this.dataSource.data.forEach(row => this.selection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: Book): string {
    if (row && row.id) {
      return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.id + 1}`;
    } else {
      return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
    }
  }

  // @HostListener('window:scroll', ['$event'])
  // onscroll(event) {
  //   const elem = event.currentTarget;
  //   if ((elem.innerHeight + elem.pageYOffset + 200) >= document.body.offsetHeight && this.pageLength <= this.dataLength) {
  //     this.pageLength += 30;
  //     this.paginator._changePageSize(this.pageLength);
  //   }
  // }

}
