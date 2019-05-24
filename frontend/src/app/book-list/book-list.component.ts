import { Component, OnInit } from '@angular/core';
import { Book } from '../models/book.model';
import { Author } from '../models/author.model';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-book-list',
  templateUrl: './book-list.component.html',
  styleUrls: ['./book-list.component.scss']
})
export class BookListComponent implements OnInit {

  author: Author = { id: 1, name: 'Author 1' };
  books: Book[] = [{ id: 1, title: 'Book 1', description: 'Description 1', author: this.author }];
  dataSource: MatTableDataSource<Book>;

  columns = [
    { columnDef: 'id', header: 'ID', cell: (row: Book) => `${row.id}` },
    { columnDef: 'title', header: 'Title', cell: (row: Book) => `${row.title}` },
    { columnDef: 'author', header: 'Author', cell: (row: Book) => `${row.author.name}` }
  ];

  /** Column definitions in order */
  displayedColumns = this.columns.map(x => x.columnDef);

  constructor() { }

  ngOnInit() {
    this.dataSource = new MatTableDataSource(this.books);
  }

}
